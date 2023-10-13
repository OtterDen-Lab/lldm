from LLDM.helpers import helper_functions


class Battle(LLDM_module):
  def __init__(self):
    character1 = None
    helper_functions.roll_skill_check(character1, "initiative", False)
    


def start_battle(
    characters, #
    character_annotations, # motivations, feelings, states
    environment, #
    positions, # todo?
    
):
  pass