# from LLDM.Deprecated.World import World


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
    self._turn_order_()
    self.turn = 1
    self.battle_result = "unknown"
    self.character_index = 0

  def _turn_order_(self):
    self._assign_initiative_(self.enemy_list)
    self._assign_initiative_(self.players_list)
    self.order = sorted(self.order, key=lambda x: x[0])

  # TODO: Make an initiative stat for characters as a modifier
  # TODO: Figure out who should go first if the number is the same between characters
  def _assign_initiative_(self, team):
    for character in team:
      print("Roll initiative for " + character.JSON['name'] + "and enter here: ")
      init_num = int(input())
      while (init_num < 1 or init_num > 20):
        print("Invalid number, please input again.")
        print("\nRoll initiative for " + character.JSON['name'] + "and enter here: ")
        init_num = int(input())

      ## Use this instead if the computer is rolling the dice
      # init_num = helper_functions.roll_skill_check(character, "initiative", False)
      self.order.append((init_num, character))

  
  
  def start_battle(self):
    print("Starting Battle\n")
    self._start_battle_helper_()
    
    print(f"Battle beginning at turn {self.turn}")
    while (self.enemy_alive_count > 0 and self.player_alive_count > 0):
      self.current_turn(self.order[self.character_index][1])

      self.character_index = (self.character_index + 1) % len(self.order)
      if (self.character_index == 0): 
        self.turn += 1
        print(f"Turn complete. Starting Turn {self.turn}")

        break # For debug purposes, only one turn happens, otherwise infinite
    
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
    print("It is currently " + character.JSON['name'] + "'s time to act!")

    # TODO: Code all the necessary queries for a given player's turn
    # TODO: If it is an enemy's turn, auto generate information from GPT
    

    # TODO: Figure out how much action text there will be from the user. If it's an enemy, we would need to generate this information somehow.
    action_text = ""
    self.query_turn_story(action_text)

    # TODO: Update JSON Database based off keywords in action_text?


    # Update Character Annotations / Attributes
    # attributes.update_attributes(character)

    print("End of " + character.JSON['name'] + "'s turn\n")



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

  # Primarily for anger or fear leading to possible run away
  def check_motivation(self):
    pass

  # For Jalen
  def query_turn_story(self, action_text):
    # TODO: Query GPT for an explanation given information from the turn player

    # TODO: Update Vector DB with Chat GPT's summary:

    pass