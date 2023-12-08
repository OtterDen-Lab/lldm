'''
# Dominic TODO:
    Update Documentation

    If you want to give more battle specific info to main, edit story to include those, and edit main to retrieve those from the response object from battle
        - Should be after everything else is working for battle

    Update BattleSDPrompter.txt to make images for enemies?
'''

import random
from LLDM.Core.Scene import Character, Scene
from LLDM.Core.GPT import chat_complete_battle, chat_complete_battle_AI_input

class Battle:
    ## Initialize the battle object
    # TODO: Character Annotations now just optional attributes of Character, account for this
    # Update Motivations, surprise, distance for each (Defaults: normal (mood), surprise factor of 0 (no effect), distance factor of 0 (no effect), normal (state / status))
    def __init__(self, scene: Scene, turnLimit=1000, TESTMODE=False):
        self.TESTMODE = TESTMODE
        self._enemy_actions = ["Attack", "Wait"]

        self._location = scene.loc_map.current_location
        self._party_alive_count = 0
        self._enemy_alive_count = 0
        self._order = []
        self._create_full_Character_list_(scene.characters)
        self._dead = []
        self._ran_away = []
        self._turnLimit = turnLimit
        self._battle_result = "unknown"

    def start_battle(self):
        global inBattle
        inBattle = True

        # Before battle starts
        print("Starting Battle\n")
        self._assign_initiative_()
        self._turn = 1
        self._character_index = 0

        print(f"Current Turn: {self._turn}")
        # Check that there is still at least one of each team left
        while self._party_alive_count > 0 and self._enemy_alive_count > 0:
            self.current_turn()

            # Add anyone who is dead into the dead list
            for info in self._order:
                if info[1].health > 0: continue
                self._dead.append(info)

            # Update order to no longer include those who have died
            self._order[:] = [info for info in self._order if info[1].health > 0]
            orderSize = len(self._order)

            # Get next character in order, might also start next turn
            self._character_index = (min(self._character_index, orderSize - 1) + 1) % orderSize
            if self._character_index == 0:
                self._turn += 1
                # self._reset_temp_mods()

                if self._turnLimit < self._turn:
                    break

                print(f"Turn complete. Starting Turn {self._turn}")

        self._battle_result = "Victory" if self._party_alive_count > 0 else "Defeat"
        print("Battle Complete\n")
        return self.finalize_objects()

    def current_turn(self):
        global web_app_message, battle_events
        turnCharacter = self._order[self._character_index][1]
        print(f"It is currently {turnCharacter.name}'s time to act!")

        while True:
            if self.TESTMODE or turnCharacter.npc:
                print(f"Prompting for {turnCharacter.name}'s action")
                randomActionNum = 0 if self.TESTMODE else random.randint(0, len(self._enemy_actions) - 1)
                prompt_input = chat_complete_battle_AI_input(location=self._location, turnCharacter=turnCharacter,
                                                             charactersInfo=self._order,
                                                             randomAction=self._enemy_actions[randomActionNum])
            else:
                print(
                    f"Give {turnCharacter.name} something to do this turn. Provide target and other information as needed: ")
                while web_app_message is None:
                    continue
                prompt_input = web_app_message
                web_app_message = None
                # prompt_input = str(input())

            response = chat_complete_battle(prompt_input, location=self._location, turnCharacter=turnCharacter,
                                            charactersInfo=self._order)

            # Figure out who is going / Check order array (purely to assign input to character)
            # Send call with input and object metadata
            # Use response to update global battle_events
            # Return 0
            # // Outside (App.py)
            #   Fetch global battle_events
            #   Post to dialogue

            if response:
                battle_events = response.get('events')
                self._location = response.get('location')
                self._order = response.get('characters')
                break

        print(f"End of {turnCharacter.name}'s turn\n")

    #########################################
    #
    #          Pre-Battle Functions
    #
    #########################################

    def _create_full_Character_list_(self, all_characters: []):
        for character in all_characters:
            self._order.append((5, character))
            if character.entity == "party":
                self._party_alive_count += 1
            elif character.entity == "enemy":
                self._enemy_alive_count += 1

    def _assign_initiative_(self):
        """
        ! Currently assigns randomly, maybe a future update where we query user input for rolls.
          ONLY IF ABSOLUTELY REQUIRED.
        """
        self._order = [(random.randint(1, 20) + chr.dexterity, chr) for _, chr in self._order]
        self._order = sorted(self._order, key=lambda x: x[0], reverse=True)
        # print(self._order)

    #########################################
    #
    #    End of Battle Functions
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

    def finalize_objects(self):
        party = []
        enemies = []

        global inBattle
        inBattle = False

        for info in self._order:
            party.append(info[1]) if info[1].entity == 'party' else enemies.append(info[1])

        return {'party': party,
                'dead': self._dead,
                'location': self._location,
                'enemies': enemies,
                'outcome': self._battle_result
                }


# Battle Controller:
# Init Battle: Determine order and generate initiative array
#
# Current Turn() Iterates from index in initiative array, processing the input and resolving it.
#   No output, but overwrites battle_events
#
# If at the end of this turn, if one side (enemy/party) is dead, end the battle and set inBattle to False
#


def process_input_battle(user_input):
    global web_app_message
    web_app_message = user_input


web_app_message = None

# Whether a battle is in session
inBattle = False

# Events: Each turn generates one or more Event(s) of what just happened
battle_events = []


def get_battle_events():
    # Return new events generated per turn
    global battle_events
    return battle_events

    #########################################
    #
    #               Unused
    #
    #########################################
    ## Need to Update / Add in

    # def query_turn_story(self, action_text):
    #     text = "describe and summarize this: " + action_text
    #     print("[GAMEMASTER]:", end=" ")
    #     self.log.append({"role": "user", "content": text})
    #     person = openai.ChatCompletion.create(model=MODEL, messages=self.log)
    #     replay = person.choices[0].message['content']
    #     print(replay)
    #     self.action_log.append(replay)
    #     # TODO: Update Vector DB with Chat GPT's summary:

    # def grand_sum(self):
    #     auto_text = "Summarize the following events of the battle: "
    #     for text in self.action_log:
    #         auto_text += text + "\n"

    #     person = openai.ChatCompletion.create(model=MODEL, message=auto_text)
    #     replay = person.choice[0].message.centent
    #     print(replay)
