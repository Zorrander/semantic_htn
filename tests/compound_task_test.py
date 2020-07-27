import unittest
from cobowl import world
from semantic_htn import planner
import os.path
from os.path import expanduser

home = expanduser("~")

RESOURCE_PATH  = os.path.join(home, "ros2", "src", "tuni-semweb", "cobot_knowledge", "resource", "database")
# RESOURCE_PATH  = os.path.join(home, "Downloads", "tuni-semweb", "cobot_knowledge", "resource", "database")

class TestPrimitiveTasks(unittest.TestCase):
    def setUp(self):
        self.world = world.DigitalWorld(base=os.path.join(RESOURCE_PATH, 'handover.owl'))
        self.world.add_object("peg")
        self.planner = planner.Planner(self.world)

    def test_pick_with_reach(self):
        print("===TEST PICK ===        ")
        plan, goal = self.planner.create_plan(command = ("pick", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    def test_pick_without_reach(self):
        print("===TEST PICK ===        ")
        print("REACHING...")
        plan, goal = self.planner.create_plan(command = ("reach", ["peg"]))
        self.planner.run(self.world, plan, goal)
        print("PICK...")
        plan, goal = self.planner.create_plan(command = ("pick", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    def test_place_without_drop(self):
        print("===TEST PLACE ===        ")
        print("PICK")
        plan, goal = self.planner.create_plan(command = ("pick", ["peg"]))
        self.planner.run(self.world, plan, goal)
        print("PLACE")
        plan, goal = self.planner.create_plan(command = ("place", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    def test_place_with_drop(self):
        print("===TEST PLACE ===        ")
        print("PICK")
        plan, goal = self.planner.create_plan(command = ("pick", ["peg"]))
        self.planner.run(self.world, plan, goal)
        print("LIFT")
        plan, goal = self.planner.create_plan(command = ("lift", ["peg"]))
        self.planner.run(self.world, plan, goal)
        print("PLACE")
        plan, goal = self.planner.create_plan(command = ("place", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    '''
    def test_handover_robot_to_human(self):
        print("===TEST HANDOVER FROM ROBOT TO HUMAN ===        ")
        plan, goal = self.planner.create_plan(command = ("give", ["peg"]))
        self.planner.run(self.world, plan, goal)
        plan, goal = self.planner.create_plan()
        self.planner.run(self.world, plan, goal)
        plan, goal = self.planner.create_plan()
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    def test_handover_human_to_robot(self):
        print("===TEST HANDOVER FROM HUMAN TO ROBOT ===        ")
        plan, goal = self.planner.create_plan(command = ("take", ["peg"]))
        self.planner.run(self.world, plan, goal)
        #self.assertEqual(plan[0].name, "reachtask1")
        print()


    def format_data_for_display(people):
        ...  # Implement this!

    def test_format_data_for_display():
        people = [
            {
                "given_name": "Alfonsa",
                "family_name": "Ruiz",
                "title": "Senior Software Engineer",
            },
            {
                "given_name": "Sayid",
                "family_name": "Khan",
                "title": "Project Manager",
            },
        ]

        assert format_data_for_display(people) == [
            "Alfonsa Ruiz: Senior Software Engineer",
            "Sayid Khan: Project Manager",
        ]
    '''

if __name__ == '__main__':
    unittest.main()
