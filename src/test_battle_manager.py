import unittest

from LLDM.Core.Scene import *  # safe
from LLDM.Core.BattleManager import Battle




# Test 1: Test on functions that don't use GPT calls
class Mock_test_1(unittest.TestCase):
    def setUp(self):
        Character.reset()
        self.players = []
        self.enemies = []

        self.warrior = Character("Warrior1", 100, 10, 10, 0, "party")
        self.goblin = Character("Goblin1", 20, 10, 10, 0, "enemy", True)
        self.fastWarrior = Character("Warrior2", 100, 10, 10, 30, "party")
        self.fastGoblin = Character("Goblin2", 20, 10, 10, 30, "enemy", True)

        self.scene = Scene(fake_init_map())

    # Check that Battle object is created correctly
    def test_battle_1_init(self):
        print("\n[NEW TEST]: Battle Init")
        self.scene.add_character(self.warrior)
        self.scene.add_character(self.goblin)
        battle = Battle(self.scene, turnLimit=1, TESTMODE=True)

        self.assertEqual(1, battle._party_alive_count)
        self.assertEqual(1, battle._enemy_alive_count)
        self.assertEqual("testName", battle._location.name)
        self.assertEqual(1, battle._turnLimit)
        self.assertEqual(2, len(battle._order))
        self.assertEqual(0, len(battle._dead))
        self.assertEqual(0, len(battle._ran_away))

    # Check that initative function works correctly
    def test_battle_2_initiative_ordering_Warrior(self):
        print("\n[NEW TEST]: Initiative Ordering Warrior")
        self.scene.add_character(self.fastWarrior)
        self.scene.add_character(self.goblin)

        battle = Battle(self.scene, turnLimit=1, TESTMODE=True)
        for _ in range(50):
            battle._assign_initiative_()

            firstInfo = battle._order[0]
            secondInfo = battle._order[1]

            self.assertLessEqual(31, firstInfo[0])
            self.assertGreaterEqual(50, firstInfo[0])
            self.assertLessEqual(1, secondInfo[0])
            self.assertGreaterEqual(20, secondInfo[0])

            self.assertEqual(self.fastWarrior, firstInfo[1])
            self.assertEqual(self.goblin, secondInfo[1])

    # Check that initiative function works correctly
    def test_battle_3_initiative_ordering_Goblin(self):
        print("\n[NEW TEST]: Initiative Ordering Goblin")
        self.scene.add_character(self.warrior)
        self.scene.add_character(self.fastGoblin)

        battle = Battle(self.scene, turnLimit=1, TESTMODE=True)
        for _ in range(50):
            battle._assign_initiative_()

            firstInfo = battle._order[0]
            secondInfo = battle._order[1]

            self.assertLessEqual(31, firstInfo[0])
            self.assertGreaterEqual(50, firstInfo[0])
            self.assertLessEqual(1, secondInfo[0])
            self.assertGreaterEqual(20, secondInfo[0])

            self.assertEqual(self.fastGoblin, firstInfo[1])
            self.assertEqual(self.warrior, secondInfo[1])


# Test 2: Battle testing with GPT calls
class Mock_test_2(unittest.TestCase):
    def setUp(self):
        Character.reset()
        self.players = []
        self.enemies = []

        self.warrior = Character("Warrior1", 100, 10, 10, 0, "party")
        self.goblin = Character("Goblin1", 20, 10, 10, 0, "enemy", True)
        self.fastWarrior = Character("Warrior2", 100, 10, 10, 30, "party")
        self.fastGoblin = Character("Goblin2", 20, 10, 10, 30, "enemy", True)

        self.scene = Scene(fake_init_map())
        self.scene.add_character(self.fastWarrior)
        self.scene.add_character(self.fastGoblin)
        self.scene.add_character(self.goblin)

    # Check that Battle object can run to completion
    def test_battle_1_finish(self):
        print("\n[NEW TEST]: Battle Start -> Complete")
        battle = Battle(self.scene, turnLimit=1, TESTMODE=True)

        battle.start_battle()
        self.assertEqual("unknown", battle._battle_result)
        self.assertEqual(2, battle._turn)

        for info in battle._order:
            if info[1].id == 1:
                self.assertEqual(95, info[1].health)
                break
            else:
                self.assertEqual(15, info[1].health)

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


# Test 3: Manual Battle Test
class Mock_test_3(unittest.TestCase):
    def setUp(self):
        Character.reset()
        self.players = []
        self.enemies = []

        self.sword = Item("Sword", "A sturdy blade crafted from the finest steel.", damage=15, amount=1)
        self.potion = Item("Health Potion", "A small vial of red liquid.", healing=10, amount=1)

        self.warrior = Character("Ray", 100, 10, 10, 0, "party", inventory=[self.sword, self.potion])
        self.goblin = Character("David", 20, 10, 10, 0, "enemy", True)
        self.fastWarrior = Character("Dominic", 100, 10, 10, 30, "party", inventory=[self.sword, self.potion])
        self.fastGoblin = Character("Richard", 20, 10, 10, 30, "enemy", True)

    # Check that Battle object can run to completion
    def test_battle_1_finish(self):
        print("\n[NEW TEST]: Battle Start -> Complete")
        self.players.append(self.fastWarrior)
        self.enemies.append(self.fastGoblin)
        self.enemies.append(self.goblin)

        scene = Scene(fake_init_map())
        scene.add_character(self.warrior)
        scene.add_character(self.fastWarrior)
        scene.add_character(self.fastGoblin)
        scene.add_character(self.goblin)

        battle = Battle(scene, turnLimit=1)

        battle.start_battle()
        self.assertEqual("unknown", battle._battle_result)
        self.assertEqual(2, battle._turn)


def fake_init_map():
    # TODO: Use a DungeonGenerator to pass main a fully-structured dungeon with notable locations and entrance/exit.
    # Create the Map. Note: the technical term for our map is a 'graph'.
    room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
    # room2 = Location("Room 2", "The second room. It has a door to the first room, and another door-to an unknown area.")
    map1 = Map()
    map1.add_location(room1)
    # map1.add_location(Room2)
    # map1.connect_locations(room1, room2)

    # Set the initial location with a move_to
    map1.move_to(room1)
    return map1


# For future mock tests
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # suite.addTest(loader.loadTestsFromTestCase(Mock_test_1))
    # suite.addTest(loader.loadTestsFromTestCase(Mock_test_2))
    suite.addTest(loader.loadTestsFromTestCase(Mock_test_3))
    unittest.TextTestRunner().run(suite)
