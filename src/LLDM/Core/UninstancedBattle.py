import random
from LLDM.Core.Scene import Character, Scene
from LLDM.Core.GPT import chat_complete_battle, chat_complete_battle_AI_input

# Global Variables
TESTMODE = False
_enemy_actions = ["Attack", "Wait"]
_location = None
_party_alive_count = 0
_enemy_alive_count = 0
_order = []
_dead = []
_ran_away = []
_turnLimit = 1000
_battle_result = "unknown"
_inBattle = False
_turn = 0
_character_index = 0

# Initialize Battle
def initialize_battle(scene: Scene, turn_limit=1000):
    global _location, _party_alive_count, _enemy_alive_count, _order, _dead, _ran_away, _turnLimit, _battle_result, _turn, _character_index
    _location = scene.loc_map.current_location
    _party_alive_count = 0
    _enemy_alive_count = 0
    _order = []
    _dead = []
    _ran_away = []
    _turnLimit = turn_limit
    _battle_result = "unknown"
    _turn = 1
    _character_index = 0
    create_full_character_list(scene.characters)
    assign_initiative()

def create_full_character_list(all_characters: []):
    global _order, _party_alive_count, _enemy_alive_count
    for character in all_characters:
        _order.append((5, character))
        if character.entity == "party":
            _party_alive_count += 1
        elif character.entity == "enemy":
            _enemy_alive_count += 1

def assign_initiative():
    global _order
    _order = [(random.randint(1, 20) + chr.dexterity, chr) for _, chr in _order]
    _order.sort(key=lambda x: x[0], reverse=True)

# Other functions like start_battle, current_turn, etc., need to be refactored similarly.

# Example usage
scene = Scene(...)  # Initialize Scene object
initialize_battle(scene)
