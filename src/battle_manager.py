'''
# Dominic TODO:
    Currently updated up to line 43 / 62
    
    Track player deaths and enemy deaths separately

    Update Documentation

    If you want to give more battle specific info to main, edit story to include those, and edit main to retrieve those from the response object from battle
        - Should be after everything else is working for battle

    Update BattleSDPrompter.txt to make images for enemies?
'''

import random
import openai
from LLDM.Core.Scene import Character, Scene

class Battle():
    ## Initialize the battle object
    '''
    If you want to start a battle, you must provide:
      - Location (Scene object)
      - Enemies (List of Character objects which would be the mobs)
      - Players (List of Character objects which would be the party)
    '''
    # TODO: Character Annotations now just optional attributes of Character, account for this
      # Update Motivations, surprise, distance for each (Defaults: normal (mood), surprise factor of 0 (no effect), distance factor of 0 (no effect), normal (state / status))
    def __init__(self, location: Scene, enemies: [Character], players: [Character]):
        self._location = location
        self._id_counter = 1
        self._enemies = self._create_character_dict_(enemies)
        self._party = self._create_character_dict_(players)
        self._order = []

    def start_battle(self):
        print("Starting Battle\n")
        self._start_battle_helper_()

        print(f"Current Turn: {self._turn}")
        # Check that there is still at least one of each team left
        while (len(self._enemies) > 0 and len(self._party) > 0):
            self.current_turn(self._order[self._character_index][1])
            self.update_characters()
            self._character_index = (self._character_index + 1) % len(self._order)
            if (self.character_index == 0):
                self._turn += 1
                print(f"Turn complete. Starting Turn {self._turn}")
                self.reset_temp_mods()

                break  # ! For debug purposes, only one turn happens, otherwise infinite

        print("Battle Complete\n")

    def current_turn(self, character_id: int):
        turnCharacter = self._party[character_id] if character_id in self._party else self._enemies[character_id]
        print(f"It is currently {turnCharacter.name}'s time to act!\n")

        while True:
            if (turnCharacter.entity != "party"):
                print(f"Prompting for {turnCharacter.name}'s action\n")
                prompt_input = 
            else:
                print("Give " + character.JSON[
                    'name'] + " something to do this turn. Provide target and other information as needed: ")
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
            print(
                "Dodge - within the next interaction, the next attack that will be placed on you will roll for disadvantage")
            print("Ready - within the next interaction, you can prepair your next action if attacked")
            print("Help (X character) - helping a character will give them an advantage for the next roll")
            print("Actions - prints this message again")

        elif option == self.commands[0]:
            option = input("Who?: ")
            if self.find_character(option):
                self.current_target = option
                self.breaker = True

    # ! AS OF THE CURRENT MOMENT THIS DOESN'T WORK
    # ! NEEDS TO UPDATE JSON FILES

    def set_dodge(self, number, character):
        pass
        # if number == 1:
        #   character.JSON['Status Aliments']["Dodge"] = True
        # else:
        #   character.JSON['Status Aliments']["Dodge"] = False

    # ! AS OF THE CURRENT MOMENT THIS DOESN'T WORK
    # ! NEEDS TO UPDATE JSON FILES
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

    def _create_character_dict_(self, team: [Character]):
        character_dict = {}
        for character in team:
            character_dict[self._id_counter] = character
            self._id_counter += 1
        return character_dict
    
    def _start_battle_helper_(self):
        self._assign_initiative_()
        self._turn = 1
        self._battle_result = "unknown"
        self._character_index = 0

    def _assign_initiative_(self):
        """
        ! Currently assigns randomly, maybe a future update where we query user input for rolls.
          ONLY IF ABSOLUTELY REQUIRED.
        """
        for character in self._party:
            # print(f"\nRolling initiative for {character.name} (Party): ")
            roll = random.randint(1, 20) + character.dexterity
            self._order.append((roll, character.name))

        for character in self._enemies:
            # print("\nRolling initiative for " + character.JSON['name'] + "(Enemy): ")
            roll = random.randint(1, 20) + character.dexterity
            self._order.append((roll, character.name))

        self._order = sorted(self._order, key=lambda x: x[0])

    #########################################
    #
    #          Battle Functions - Moving to gpt_tools.py
    #
    #########################################

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
        # ! grabs character JSON files and determine if the characters are dead "HP < 0"
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

    # def set_storyteller(self):
    #     # ? The context can be edited for maybe for a better description
    #     self.log.append({"role": "system",
    #                      "content": "You are a Dungeon Master facilitating a Dungeons and Dragons campaign that is currently within a battle"})

    def grand_sum(self):
        auto_text = "Summarize the following events of the battle: "
        for text in self.action_log:
            auto_text += text + "\n"

        person = openai.ChatCompletion.create(model=MODEL, message=auto_text)
        replay = person.choice[0].message.centent
        print(replay)
