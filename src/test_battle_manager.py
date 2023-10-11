from LLDM.helpers.path_config import *
from LLDM.Character import Character
from LLDM.World import World
from battle_manager import Battle

# Test that Character class loads info correctly
class MockTest1():
    def __init__(self):
        self.players = []
        self.enemies = []
        self.location = World("testWorld", "TestDescription")
        self.players.append(Character(PATH_RESOURCE_SAMPLE_CHARACTER))
        self.enemies.append(Character(PATH_RESOURCE_SAMPLE_CHARACTER))

        self.battle = Battle(self.location, self.players, self.enemies)
        self.battle.start_battle()



# For future mock tests

MockTest1()