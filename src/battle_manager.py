# TODO: copy and use current party and enemy JSON files then use that for the battle and apply it to the old when finished
# TODO: update JSON files
# TODO: line 85
from LLDM.Character import Character
from LLDM.World import World
import random
import openai

#! if this key outdated somehow just use another one...
openai.api_key = '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'

MODEL = "gpt-3.5-turbo"

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
    self.message_counter = 0
    self.log = []
    self.action_log = []
    self.current_target = ""
  
  
  def start_battle(self):
    print("Starting Battle\n")
    self._start_battle_helper_()
    self.set_storyteller()
    
    print(f"Battle beginning at turn {self.turn}")
    #! For here you need to check
    while (self.enemy_alive_count > 0 and self.player_alive_count > 0):
      #! at some point we need to check if how many enemies or players are alive
      self.current_turn(self.order[self.character_index][1])
      self.update_characters()
      self.character_index = (self.character_index + 1) % len(self.order)
      if (self.character_index == 0): 
        self.turn += 1
        print(f"Turn complete. Starting Turn {self.turn}")
        self.reset_temp_mods()

        break #! For debug purposes, only one turn happens, otherwise infinite
    
    print("Battle Complete\n")

  def current_turn(self, character):
    print("It is currently " + character.JSON['name'] + "'s time to act!\n")
    while True:
      # TODO: manage dodges
      #? check if the character is an enemy
      # TODO: Code all the necessary queries for a given player's turn
      if (character.JSON['player']['entity'] != "party"):
        print("Prompting for " + character.JSON['name'] + "'s action\n")
        prompt_input = queryStringGetHelpFromRayForWhatThisShouldBe
      else:
        print("Give " + character.JSON['name'] + " something to do this turn. Provide target and other information as needed: ")
        prompt_input = str(input())

      match prompt_input:
        case _:
          action = self.chat_complete_getAction(prompt_input, character)
          if action is False or action['action_type'] == "help":
            continue
          
          if action is not None:
            response = self.chat_complete_performAction(action, character)

            # Update Character Annotations / Attributes

            break

    print("End of " + character.JSON['name'] + "'s turn\n")



  """
  ! all movement based action will not be considered for the time being
  #? create a list of what commnads do what
  #? Attack - character a attacks character b via normal means with current equipment
  #? Dodge - for the time being all characters who attacks character a will hdisadventage
  #? Help - character b will get advantage
  #? more action can be callled later maybe...
  """

  def action_function(self, option):
    found_character = False
    if option == self.commands[1]:
      self.set_dodge(1, self.order[self.character_index][1])
      self.breaker = True

    elif option == self.commands[4]:
      self.set_ready(1)
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
          self.current_target = option
          self.breaker = True

  #! AS OF THE CURRENT MOMENT THIS DOESN'T WORK
  #! NEEDS TO UPDATE JSON FILES

  def set_dodge(self, number, character):
    pass
    # if number == 1:
    #   character.JSON['Status Aliments']["Dodge"] = True
    # else:
    #   character.JSON['Status Aliments']["Dodge"] = False
    

  #! AS OF THE CURRENT MOMENT THIS DOESN'T WORK
  #! NEEDS TO UPDATE JSON FILES
  def set_ready(self, number, character):
    pass
    # if number == 1:
    #   character.JSON['Status Aliments']["Ready"] = True

    # else:
    #   character.JSON['Status Aliments']["Ready"] = False

  def find_character(self, option):
    order_index = 0
    while order_index < len(self.order):
      if self.order[order_index][1].JSON['name'] == option:
        return True
      order_index += 1
    return False


#########################################
#
#          Pre-Battle Functions
#
#########################################

  def _start_battle_helper_(self):
    self._turn_order_()
    self.turn = 1
    self.battle_result = "unknown"
    self.character_index = 0

  def _turn_order_(self):
    self._assign_initiative_(self.players_list, self.enemy_list)
    self.order = sorted(self.order, key=lambda x: x[0])

  def _assign_initiative_(self, team1, team2):
    """
    ! Also if we need an intiiative stat for character we don't need to assign manually we should   need a rng d20
    ! from there you should assign current initiative per character this can be solved quickly for  either our team
    ! or the campign team
    """

    print("Merging party members to enemies")
    for character in team1:
      print("\nRolling initiative for " + character.JSON['name'] + "(Party): ")
      roll = self.dice.randint(0, 21) + character.JSON['ability_scores']['dex_mod']
      self.order.append((roll, character))

    for character in team2:
      print("\nRolling initiative for " + character.JSON['name'] + "(Enemy): ")
      roll = self.dice.randint(0, 21) + character.JSON['ability_scores']['dex_mod']
      self.order.append((roll, character))



#########################################
#
#        Chat Complete Functions
#
#########################################

  def chat_complete_getAction(self):
    pass

  def chat_complete_performAction(self):
    pass



#########################################
#
#          Battle Functions
#
#########################################

  def handle_attack(self):
    pass

  def handle_dodge(self, character):
    character.JSON['Status Aliments']["Dodge"] = True
    pass

  def handle_help(self):
    pass

  def handle_actions(self):
    pass

  def handle_wait(self):
    pass

  def check_motivation(self):
    # TODO: Primarily for anger or fear leading to possible run away

    pass

  def update_characters(self):
    #! grabs character JSON files and determine if the characters are dead "HP < 0"
    number = 0
    while number < len(self.order):
      passed = True
      if self.order[number][1].JSON['hit_points']['current'] < 0:
        if self.order[number][1].JSON['player']['entity'] != "party":
          self.enemy_list.remove(self.order[number][1])

        else:
          self.players_list.remove(self.order[number][1])

        self.order.remove(self.order[number])
        self.player_alive_count = len(self.players_list)
        self.enemy_alive_count = len(self.enemy_list)
      if passed:
        number += 1

#########################################
#
#    End of Battle Functions - Richard
#
#########################################

  def conclusion_summary_GPT(self, outcome):
    # TODO: Check LLDM MasterDoc (Should be in slack group DM)
    
    pass

  def rewards_distribution(self):
    # TODO: Check LLDM MasterDoc

    pass

  def reset_battle_check(self):
    # TODO: Check LLDM MasterDoc

    pass

  # Dominic will implement
  def finalize_objects(self):

    pass






#########################################
#
#               Unused
#
#########################################
  # # TODO: If it is an enemy's turn, auto generate information from GPT? or have do the same thing as the player...
    

  #   # TODO: Figure out how much action text there will be from the user. If it's an enemy, we would need to generate this information somehow.
  #   #? character x does [action]
  #   #? character x attack/helps y
  #   action_text = ""
  #   action_text += character.JSON['name'] + " does "
  #   #? if/switch cases for actions
  #   if other_text == "dodge":
  #     action_text += "a dodge on the next time if they are hit"
  #   elif other_text == "attack":
  #     action_text += " an attack"
  #   elif other_text == "ready":
  #     action_text = character.JSON['name'] + " will prepare an action."
    
  #   self.query_turn_story(action_text)

  # Need to Update / Add in
    # For Jalen
  def query_turn_story(self, action_text):
    text = "discribe and summarize this: " + action_text
    print("[GAMEMASTER]:", end=" ")
    self.log.append({"role": "user", "content": text})  
    person = openai.ChatCompletion.create(model=MODEL, messages=self.log)
    replay = person.choices[0].message['content']
    print(replay)
    self.action_log.append(replay)
    # TODO: Update Vector DB with Chat GPT's summary:
    

  def set_storyteller(self):
    #? The context can be edited for maybe for a better description
    self.log.append({"role": "system", "content": "You are a Dungeon Master facilitating a Dungeons and Dragons campaign that is currently within a battle"})
  
  def grand_sum(self):
    auto_text = "Summarize the following events of the battle: "
    for text in self.action_log:
      auto_text += text + "\n"
    
    person = openai.ChatCompletion.create(model=MODEL, message=auto_text)
    replay = person.choice[0].message.centent
    print(replay)