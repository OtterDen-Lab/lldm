from LLDM.helpers import helper_functions
from LLDM import Character


class Battle():
  ## Initialize the battle object
    # I'm thinking enemies and players are listed separately
    # Location, enemies, and players can all be objects thanks to how Character Class is implemented
    # Character Annotations Class can hold motivations, surprise, and distance
      # This is from GPT or players, therefore MUST be updated by LLDM BEFORE passing to Battle object
      # Plan is to have a new task called Prepare_Battle, which will be given a list of players and enemies, as well as context, and its job is to update motivations, surprise, and distance for each (Defaults: normal (mood), surprise factor of 0 (no effect), distance factor of 0 (no effect), normal (state)).
  def __init__(self, location, enemies, players):
    self.location_obj = location
    self.enemy_list = enemies
    self.enemy_alive_count = len(enemies)
    self.players_list = players
    self.player_alive_count = len(players)
    self.order = []

  def _start_battle_helper_(self):
    self.turn_order()
    self.turn = 1
    self.battle_result = "unknown"
    self.character_index = 0

  def _assign_initiative_(self, team):
    for character in team:
      print("Roll initiative for " + character.get_name() + "and enter here: ")
      init_num = int(input())
      while (init_num < 1 or init_num > 20):
        print("Invalid number, please input again.")
        print("\nRoll initiative for " + character.get_name() + "and enter here: ")
        init_num = int(input())

      ## Use this instead if the computer is rolling the dice
      # init_num = helper_functions.roll_skill_check(character, "initiative", False)
      self.order.append((init_num, character))

  def turn_order(self):
    self._assign_initiative_(self.enemyList)
    self._assign_initiative_(self.playersList)
    self.order = sorted(self.order, key=lambda x: x[0])

  
  def start_battle(self):
    print("Starting Battle\n")
    self._start_battle_helper_()
    
    print("Battle beginning at turn " + self.turn)
    while (self.enemy_alive_count > 0 and self.player_alive_count > 0):
      self.current_turn(self.order[character_index])

      character_index = (character_index + 1) % len(self.order)
      if (character_index == 0): 
        self.turn += 1
        print("Turn complete. Starting Turn " + self.turn)
    
    print("Battle Complete\n")

    if (self.battle_result == "victory"):
      self._victory_()
    elif (self.battle_result == "defeat"):
      self._defeat_()
    elif (self.battle_result == "players flee"):
      self._run_away_players_()
    elif (self.battle_result == "enemies flee"):
      self._run_away_enemies_()
    

  def current_turn(self, character):
    # For Jalen to implement
    print("It is currently " + character.get_name() + "'s time to act!")



    # Update character info here
    print("End of " + character.get_name() + "'s turn")



#################################
#
#        Battle Functions
#
#################################

  def _victory_(self):
    pass

  def _defeat_(self):
    pass

  def _run_away_players_(self):
    pass

  def _run_away_enemies_(self):
    pass

  def _damage_calculator_(self):
    pass

  def action_attack(self):
    pass

  def action_wait(self):
    pass

  def action_skill(self):
    pass

  def check_motivation(self):
    pass
