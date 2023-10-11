import unittest

from LLDM.helpers.path_config import *
from LLDM.Character import Character
from LLDM.World import World
from battle_manager import Battle

# Test that Character class loads info correctly
class Mock_test_1(unittest.TestCase):
    def setUp(self):
        self.players = []
        self.enemies = []
        self.location = World("testWorld", "TestDescription")
        self.players.append(Character(PATH_RESOURCE_SAMPLE_CHARACTER))
        self.enemies.append(Character(PATH_RESOURCE_SAMPLE_CHARACTER))

        self.battle = Battle(self.location, self.players, self.enemies)

    # Check that Battle object is created correctly
    def test_battle_init(self):
        self.assertEqual(1, self.battle.player_alive_count)
        self.assertEqual(1, self.battle.enemy_alive_count)
        self.assertEqual("testWorld", self.battle.location_obj.name)

    # Check that Battle object can run to completion
    def test_battle_finish(self):
        self.battle.start_battle()
        self.assertEqual("unknown", self.battle.battle_result)
        self.assertEqual(2, self.battle.turn)

    # TODO SECTION: 
    # [Unfinished] Check that Battle object resets properly
    def test_battle_repeat(self):
        self.battle.start_battle()
        self.assertEqual("unknown", self.battle.battle_result)
        self.assertEqual(2, self.battle.turn)

        self.battle.start_battle()
        self.assertEqual("unknown", self.battle.battle_result)
        self.assertEqual(2, self.battle.turn)

    # Check that initiative rolls run to completion
    def test_initiative(self):
        pass

    # Check that initiative rolls correctly decide who goes first if equal
    def test_initiative_equal(self):
        pass


# For future mock tests
if __name__ == '__main__':
    unittest.main()