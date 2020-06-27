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
        self.planner = planner.Planner()

    def test_explore_cond(self):
        current_task = self.world.ReachTask()
        #self.planner.explore_effects_primitive_task(current_task)

    def test_explore_cond(self):
        current_task = self.world.onto.ReachTask()
        #self.planner.explore_cond_primitive_task(current_task)

    def test_grasp(self):
        self.world.send_command("grasp", [])
        self.planner.create_plan(self.world)

    def test_reach(self):
        self.world.send_command("reach", [])
        self.planner.create_plan(self.world)

    def test_wait_for(self):
        self.world.send_command("wait", [])
        self.planner.create_plan(self.world)

if __name__ == '__main__':
    unittest.main()
