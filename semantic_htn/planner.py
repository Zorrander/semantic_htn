import time
from cobowl.world import DigitalWorld
from cmd import Cmd
from cobowl import world

class MyPrompt(Cmd):
    def __init__(self):
        super(MyPrompt, self).__init__()
        self.world = DigitalWorld()
        self.planner = Planner()
        self.prompt = 'Panda> '
        self.intro = """
Collaborative Robotics Planning
-------------------------------

Commands:
     add (obj)
     workspace_status
     plan - to reason about the current status of the world
     handover (obj) - to send the corresponding command and plan
     pick (obj)
     reach (obj)
     grasp (obj)
     take - to simulate a human taking something from the robot
     assembly - to plan for the Cranfield Assembly benchmark
     packaging - to try cleaning the workspace putting all the objects in a box
     status - to show the robot properties
     help
"""

    def do_exit(self, inp):
        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        self.planner.destroy_node()
        return True

    def do_plan(self, inp):
        plan = self.planner.create_plan(self.world)
        self.run(plan)

    def do_add(self, inp):
        self.world.add_object(inp)

    def do_workspace_status(self, inp):
        self.world.workspace.print_status()
        if self.world.is_workspace_empty():
            print("Workspace is empty")
        else:
            print("Workspace is not empty")

    def do_take(self, inp):
        self.world.send_command('release')
        plan = self.planner.create_plan(self.world)
        self.run(plan)

    def do_pick(self, inp):
        self.world.send_command('pick', inp)
        plan = self.planner.create_plan(self.world)
        self.run(plan)

    def do_grasp(self, inp):
        self.world.send_command('grasp', inp)
        plan = self.planner.create_plan(self.world)
        self.run(plan)

    def do_reach(self, inp):
        try:
            print("Reaching {}".format(inp))
            self.world.send_command('reach', inp)
            plan = self.planner.create_plan(self.world)
            self.run(plan)
        except AnchoringError as e:
            print("Could not understand {}".format(e.object))

    def do_leads_to(self, inp):
        self.world.leads_to(inp)

    def do_handover(self, inp):
        self.world.send_command('give', inp)
        plan = self.planner.create_plan(self.world)
        self.run(plan)

    def do_packaging(self, inp):
        self.world.send_command('clean')
        plan = self.planner.create_plan(self.world)
        self.run(plan)

    def do_assembly(self, inp):
        print("Coming soon")

    def do_status(self, inp):
        self.world.robot.print_status()

class DispatchingError(Exception):
   def __init__(self, primitive):
      self.primitive = primitive

class Planner():

    def __init__(self):
        pass

    def explore_cond_primitive_task(self, current_task):
        print("exploring prim task({})".format(current_task))
        return True if self.planning_world.are_preconditions_met(current_task) else False

    def explore_effects_primitive_task(self, current_task):
        print("exploring effects({})".format(current_task))
        return True if self.planning_world.are_effects_satisfied(current_task) else False

    def explore_compound_task(self, current_task):
        print("exploring compound task({})".format(current_task))
        method = self.planning_world.find_satisfied_method(current_task)
        print("chosen method {}".format(method))
        if method:
            new_tasks = [task for task in self.planning_world.find_subtasks(method)]
            return new_tasks

    def search(self, final_plan, tasks_to_process):
        print("Creating plan about")
        print(tasks_to_process)
        if not tasks_to_process:
            return final_plan
        else:
            current_task = tasks_to_process.pop(0)
            parent, type = self.planning_world.find_type(current_task)
            if type == "CompoundTask":
                new_tasks = self.explore_compound_task(parent)
                print("new_tasks {}".format(new_tasks))
                if len(new_tasks) == 1 and new_tasks[0].is_a[0].name == "State":
                    final_plan.insert(0, new_tasks[0])
                elif new_tasks:
                    tasks_to_process.extend(new_tasks)
                    self.search(final_plan, tasks_to_process)
                    #del tasks_to_process[:-len(new_tasks)]
                else:
                    tasks_to_process.append(current_task)
                    self.search(final_plan, tasks_to_process)
            else:  # Primitive task
                if self.explore_cond_primitive_task(parent):
                    print("good primitive")
                    self.planning_world.apply_effects(parent)
                    self.search(final_plan, tasks_to_process)
                    final_plan.insert(0, parent)
                else:
                    if not self.explore_effects_primitive_task(parent):
                        print("cancel move")
                        tasks_to_process.append(parent)
                    self.search(final_plan, tasks_to_process)
            return final_plan


    def create_plan(self, current_world, root_task=None):
        try:
            final_plan = list()
            print("create_plan {}".format(current_world))
            self.planning_world = current_world.clone()
            print("copy created")
            tasks_to_process = self.planning_world.root_task if not root_task else root_task
            final_plan = self.search(final_plan, tasks_to_process)
            print("PLAN: {}".format(final_plan))
            return final_plan
        except Exception as e:
            print(e)

    def inverse_planning(self, primitive, final_plan=None):
        print(primitive.is_a[1].__dict__)
        constraint = primitive.is_a[1]
        fun = getattr(self.planning_world.workspace, "test_"+constraint.property.name)
        comparator = getattr(properties, constraint.property.name)
        diff = comparator.compare(fun(), constraint)
        return self.planning_world.resolve_conflicts(diff)

    def run(self, world, plan, goal_state = False):
        try:
            original_plan = copy.deepcopy(plan)
            with world.onto:
                #while plan and not world.check_state(goal_state):
                while plan:
                    primitive = plan.pop(0)()
                    print("running..{}".format(primitive))
                    if primitive.is_a[0].name == "State":
                        pass
                        #goal_state = primitive
                        #plan.extend(self.inverse_planning(primitive))
                    else:
                        if world.are_preconditions_met(primitive):
                            self.execute(primitive, world)
                        else:
                            raise DispatchingError(primitive)
        except DispatchingError as e:
            print("Dispatching Error: {} ".format(e.primitive))
            new_plan = self.create_plan(world, [e.primitive])
            self.run(new_plan, goal_state)

    def execute(self, primitive, world):
        try:
            world.apply_effects(primitive)
            print("RUN:{}".format(primitive))
            time.sleep(2)
            #self.sem_controller.interpret(primitive)
        except:
            raise DispatchingError(primitive)
