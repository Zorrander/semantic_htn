import time
from cobowl.world import DigitalWorld
from cmd import Cmd
from cobowl import world
import copy


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
        return self.planning_world.find_satisfied_method(current_task)

    def search(self, final_plan, tasks_to_process):
        if not tasks_to_process:
            return final_plan
        else:
            current_task = tasks_to_process.pop(0)
            type = self.planning_world.find_type(current_task)
            if type == "CompoundTask":
                new_tasks = self.explore_compound_task(current_task)
                print("new_tasks {}".format(new_tasks))
                for t in new_tasks:
                    print(t.actsOn)
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
                if self.explore_cond_primitive_task(current_task):
                    print("good primitive")
                    self.planning_world.apply_effects(current_task)
                    self.search(final_plan, tasks_to_process)
                    final_plan.insert(0, current_task)
                else:
                    if not self.explore_effects_primitive_task(current_task):
                        print("cancel move")
                        tasks_to_process.append(current_task)
                    self.search(final_plan, tasks_to_process)
            return final_plan


    def create_plan(self, current_world, root_task=None):
        try:
            final_plan = list()
            self.planning_world = current_world.clone()
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
            print("RUN:")
            original_plan = copy.copy(plan)
            with world.onto:
                #while plan and not world.check_state(goal_state):
                while plan:
                    primitive = plan.pop(0)
                    if primitive.is_a[0].name == "State":
                        pass
                        #goal_state = primitive
                        #plan.extend(self.inverse_planning(primitive))
                    else:
                        if world.are_preconditions_met(primitive):
                            self.execute(primitive, world)
                        else:
                            raise DispatchingError(primitive)
                world.dismiss_command()
        except DispatchingError as e:
            print("Dispatching Error: {} ".format(e.primitive))
            new_plan = self.create_plan(world, [e.primitive])
            self.run(new_plan, goal_state)

    def execute(self, primitive, world):
        try:
            world.apply_effects(primitive)
            time.sleep(1)
        except:
            raise DispatchingError(primitive)
