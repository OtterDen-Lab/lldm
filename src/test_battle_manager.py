import unittest

from LLDM.Core.Scene import *
from battle_manager import Battle

# Test that Character class loads info correctly
class Mock_test_1(unittest.TestCase):
    def setUp(self):
        self.players = []
        self.enemies = []
        self.location = Location("testName", "TestDescription")

        self.players.append(Character("Warrior1", 100, 10, 10, 0, "party"))
        self.enemies.append(Character("Goblin1", 20, 10, 10, 0, "enemy"))

        self.battle = Battle(self.location, self.players, self.enemies)

    # Check that Battle object is created correctly
    def test_battle_init(self):
        print("Test 1")
        self.assertEqual(1, self.battle._party_alive_count)
        self.assertEqual(1, self.battle._enemy_alive_count)
        self.assertEqual("testName", self.battle._location.name)

    # Check that Battle object can run to completion
    def test_battle_finish(self):
        print("Test 2")
        self.battle.start_battle()
        self.assertEqual("unknown", self.battle._battle_result)
        self.assertEqual(2, self.battle._turn)

    # TODO SECTION: 
    # [Unfinished] Check that Battle object resets properly
    # def test_battle_repeat(self):
    #     print("Test 3")
    #     self.battle.start_battle()
    #     self.assertEqual("unknown", self.battle._battle_result)
    #     self.assertEqual(2, self.battle._turn)
    #
    #     print ("Test 3 part 2")
    #     self.battle.start_battle()
    #     self.assertEqual("unknown", self.battle._battle_result)
    #     self.assertEqual(2, self.battle._turn)

    # Check that initiative rolls run to completion
    def test_initiative(self):
        pass

    # Check that initiative rolls correctly decide who goes first if equal
    def test_initiative_equal(self):
        pass


# For future mock tests
if __name__ == '__main__':
    unittest.main()