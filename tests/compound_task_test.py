import unittest
from cobowl import world
from semantic_htn import planner
import os.path
from os.path import expanduser

home = expanduser("~")

RESOURCE_PATH  = os.path.join(home, "ros2", "src", "tuni-semweb", "cobot_knowledge", "resource", "database")

class TestPrimitiveTasks(unittest.TestCase):
    def setUp(self):
        self.world = world.DigitalWorld(base=os.path.join(RESOURCE_PATH, 'handover.owl'))
        self.world.add_object("peg")
        self.planner = planner.Planner(self.world)

    def test_pick(self):
        print("===TEST PICK ===        ")
        plan = self.planner.create_plan(command = ("pick", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    def test_place(self):
        print("===TEST PLACE ===        ")
        plan = self.planner.create_plan(command = ("pick", ["peg"]))
        self.planner.run(self.world, plan)
        plan = self.planner.create_plan(command = ("place", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    def test_handover_robot_to_human(self):
        print("===TEST HANDOVER FROM ROBOT TO HUMAN ===        ")
        plan = self.planner.create_plan(command = ("give", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

    def test_handover_human_to_robot(self):
        print("===TEST HANDOVER FROM HUMAN TO ROBOT ===        ")
        plan = self.planner.create_plan(command = ("take", ["peg"]))
        #self.assertEqual(plan[0].name, "reachtask1")
        print()

if __name__ == '__main__':
    unittest.main()
