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
    self.breaker = False
    # ? For now this does not include spells or anything that use character specific actions
    self.commands = ["attack", "dodge", "help", "hide", "ready", "character", "actions", "wait"]
    self.some_text =""

  def _start_battle_helper_(self):
    self._turn_order_()
    self.turn = 1
    self.battle_result = "unknown"
    self.character_index = 0

  def _turn_order_(self):
    self._assign_initiative_(self.players_list, self.enemy_list)
    self.order = sorted(self.order, key=lambda x: x[0])

  
  """
  ! Also if we need an intiiative stat for character we don't need to assign manually we should need a rng d20
  ! from there you should assign current initiative per character this can be solved quickly for either our team
  ! or the campign team
  """

  def _assign_initiative_(self, team1, team2):
    print("Merging party members to enemies")
    for character in team1:
      print("\nRolling initiative for " + character.JSON['name'] + "(Party): ")
      roll = self.dice.randint(0, 21) + character.JSON['ability_scores']['dex_mod']
      self.order.append((roll, character))

    for character in team2:
      print("\nRolling initiative for " + character.JSON['name'] + "(Enemy): ")
      roll = self.dice.randint(0, 21) + character.JSON['ability_scores']['dex_mod']
      self.order.append((roll, character))
  
  
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

        break #! For debug purposes, only one turn happens, otherwise infinite
    
    print("Battle Complete\n")
    

  def current_turn(self, character):
    # For Jalen to implement
    other_text = ""
    print("It is currently " + character.JSON['name'] + "'s time to act!\n")
    while True:
      # TODO: manage dodges
      #? check if the character is an enemy
      # TODO: Code all the necessary queries for a given player's turn
      if (character.JSON['player']['entity'] != "party"):
        print("AI commands")
        break
      else:
        print("Give " + character.JSON['name'] + " something to do: ")
        other_text = input()
        other_text = other_text.lower()
        if (self.commands.__contains__(other_text)):
          print(character.JSON['name'] + " is doing " +  other_text + "\n")
          self.action_function(other_text, character)
          if self.breaker:
            break
          """
          ! all movement based action will not be considered for the time being
          #? create a list of what commnads do what
          #? Attack - character a attacks character b via normal means with current equipment
          #? Dodge - for the time being all characters who attacks character a will have disadventage
          #? Help - character b will get advantage
          #? more action can be callled later maybe...
          """

    # TODO: If it is an enemy's turn, auto generate information from GPT? or have do the same thing as the player...
    

    # TODO: Figure out how much action text there will be from the user. If it's an enemy, we would need to generate this information somehow.
    #? character x does [action]
    #? character x attack/helps y
    print(self.some_text)
    action_text = ""
    action_text += character.JSON['name'] + " does "
    #? if/switch cases for actions
    if other_text == "dodge":
      action_text += "a dodge on the next time if they are hit"
    elif other_text == "attack":
      action_text += " an attack"
    elif other_text == "ready":
      action_text = character.JSON['name'] + " will prepair an action."
    
    self.query_turn_story(action_text)

    # TODO: Update JSON Database based off keywords in action_text?



    # Update Character Annotations / Attributes
    # attributes.update_attributes(character)

    print("End of " + character.JSON['name'] + "'s turn\n")

  def action_function(self, option, character):
    found_character = False
    if option == self.commands[1]:
      self.set_dodge(1, character)
      self.breaker = True

    elif option == self.commands[4]:
      self.set_ready(1, character)
      self.breaker = True

    elif option == self.commands[6]:
      print("Attack (X character) - attacks the character with your current equipted weapon")
      print("Dodge - within the next interaction, the next attack that will be placed on you will roll for disadvantage")
      print("Ready - within the next interaction, you can prepair your next action if attacked")
      print("Help (X character) - helping a character will give them an advantage for the next roll")
      print("Actions - prints this message again")

    elif option == self.commands[0]:
      option = input("Who?: ")
      if self.find_character(option):
          #? this is commented out for now because it will throw an error
          #self.action_attack(self)
          self.breaker = True
          #? find character b

  def set_dodge(self, number, character):
    if number == 1:
      character.JSON['Status Aliments']["Dodge"] = True
      #TODO: Figure out a way to update JSON files or have this particular stat to be passed through the basebase
      #? or have another database to keep track of our character states

    else:
      character.JSON['Status Aliments']["Dodge"] = False

  def set_ready(self, number, character):
    if number == 1:
      character.JSON['Status Aliments']["Ready"] = True

    else:
      character.JSON['Status Aliments']["Ready"] = False

  def find_character(self, option):
    order_index = 0
    while order_index < len(self.order):
      if self.order[order_index][1].JSON['name'] == option:
        return True
      order_index += 1
    return False


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