from LLDM.Character import Character
from LLDM.World import World
#? for now I will include a dice rolls for turn order
import random

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
    self.dice = random.Random()
    # ? For now this does not include spells or anything that use character specific actions
    self.commands = ["Attack", "Dodge", "Help", "Hide", "Grapple", "Search", "Ready", "Character"]
    self.tempMods = {
      "dodge": False,
    }

  def _start_battle_helper_(self):
    self._turn_order_()
    self.turn = 1
    self.battle_result = "unknown"
    self.character_index = 0

  def _turn_order_(self):
    #! This should be all in one not two seperate list of players and enemies
    self._assign_initiative_(self.players_list, self.enemy_list)
    # self._assign_initiative_(self.enemy_list)
    # self._assign_initiative_(self.players_list)
    self.order = sorted(self.order, key=lambda x: x[0])

  # TODO: Make an initiative stat for characters as a modifier
  # TODO: Figure out who should go first if the number is the same between characters
  #! This should be all in one there is no need for teams all we need to gather all characters
  """
  ! Also if we need an intiiative stat for character we don't need to assign manually we should need a rng d20
  ! from there you should assign current initiative per character this can be solved quickly for either our team
  ! or the campign team

  """

  # def _assign_initiative_(self, team):
  #   for character in team:
  #     print("Roll initiative for " + character.JSON['name'] + "and enter here: ")
  #     init_num = int(input())
  #     while (init_num < 1 or init_num > 20):
  #       print("Invalid number, please input again.")
  #       print("\nRoll initiative for " + character.JSON['name'] + "and enter here: ")
  #       init_num = int(input())

  #     ## Use this instead if the computer is rolling the dice
  #     # init_num = helper_functions.roll_skill_check(character, "initiative", False)
  #     self.order.append((init_num, character))

  def _assign_initiative_(self, team1, team2):
    print("Merging party members to enemies")
    # self.true_order = []
    for character in team1:
      print("\nRolling initiative for " + character.JSON['name'] + "(Party): ")
      roll = self.dice.randint(0, 21) + character.JSON['ability_scores']['dex_mod']
      self.order.append((roll, character))
      # print(roll)

    for character in team2:
      print("\nRolling initiative for " + character.JSON['name'] + "(Enemy): ")
      roll = self.dice.randint(0, 21) + character.JSON['ability_scores']['dex_mod']
      self.order.append((roll, character))
      # print("\n" + character.JSON['name'] + " rolled " + roll)

    # for character in team:
    #   print("Roll initiative for " + character.JSON['name'] + "and enter here: ")
    #   init_num = int(input())
    #   while (init_num < 1 or init_num > 20):
    #     print("Invalid number, please input again.")
    #     print("\nRoll initiative for " + character.JSON['name'] + "and enter here: ")
    #     init_num = int(input())

    #   ## Use this instead if the computer is rolling the dice
    #   # init_num = helper_functions.roll_skill_check(character, "initiative", False)
    #   self.order.append((init_num, character))

  
  
  def start_battle(self):
    print("Starting Battle\n")
    self._start_battle_helper_()
    
    print(f"Battle beginning at turn {self.turn}")
    #! For here you need to check
    while (self.enemy_alive_count > 0 and self.player_alive_count > 0):
      #! check if its the enemie's turn
      self.current_turn(self.order[self.character_index][1])

      self.character_index = (self.character_index + 1) % len(self.order)
      if (self.character_index == 0): 
        self.turn += 1
        print(f"Turn complete. Starting Turn {self.turn}")
        self.reset_temp_mods(self)

        break # For debug purposes, only one turn happens, otherwise infinite
    
    print("Battle Complete\n")
    

  def current_turn(self, character):
    # For Jalen to implement
    print("It is currently " + character.JSON['name'] + "'s time to act!\n")

    #? check if the character is an enemy
    # TODO: Code all the necessary queries for a given player's turn
    if (character.JSON['player']['entity'] != "party"):
      print("AI commands")
    else:
      print("Give " + character.JSON['name'] + " something to do: ")
      other_text = input()
      if (self.commands.__contains__(other_text)):
        print(character.JSON['name'] + " is doing " +  other_text + "\n")
        self.action_function(other_text)
        """
        ! all movement based action will not be considered for the time being
        #? create a list of what commnads do what
        #? Attack - character a attacks character b via normal means with current equipment
        #? Dodge - for the time being all characters who attacks character a will have disadventage
        #? Help - character b will get advantage
        #? Hide - character a will attempt to hide but I not too sure if we can but the function into this
        #? Grapple - characer a will restrain character b
        #? Search - character a will search for items and such but this resposiblity should be in the campaign team
        """

    # TODO: If it is an enemy's turn, auto generate information from GPT? or have do the same thing as the player...
    

    # TODO: Figure out how much action text there will be from the user. If it's an enemy, we would need to generate this information somehow.
    action_text = ""
    self.query_turn_story(action_text)

    # TODO: Update JSON Database based off keywords in action_text?


    # Update Character Annotations / Attributes
    # attributes.update_attributes(character)

    print("End of " + character.JSON['name'] + "'s turn\n")

  def action_function(self, option):
    found_character = False
    for key in self.tempMods:
      if key == option:
        self.set_mod(self, option)

  def reset_temp_mods(self):
    for key in self.tempMods:
        self.tempMods[key] = False

  def set_mod(self, mod_key):
    self.tempMods[mod_key] = True

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