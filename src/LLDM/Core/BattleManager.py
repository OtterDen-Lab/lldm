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

# Globals
# Whether a battle is in session
inBattle = False

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
        self._battle_events = []

    def start_battle(self):
        global inBattle
        inBattle = True

        # Before battle starts
        print("Starting Battle\n")
        self._assign_initiative_()
        self._turn = 1
        self._character_index = 0

    def get_action_input(self):
        # Check that there is still at least one of each team left
        if self._party_alive_count <= 0 or self._enemy_alive_count <= 0 or self._turnLimit < self._turn:
            self._battle_result = "Victory" if self._party_alive_count > 0 else "Defeat"
            print("Battle Complete\n")
            return self.finalize_objects()
        
        turnCharacter = self._order[self._character_index][1]
        self._turnCharacter = turnCharacter
        print(f"It is currently {turnCharacter.name}'s time to act!")

        while True:
            if self.TESTMODE or turnCharacter.npc:
                print(f"Prompting for {turnCharacter.name}'s action")
                randomActionNum = 0 if self.TESTMODE else random.randint(0, len(self._enemy_actions) - 1)
                return {'prompt_input': chat_complete_battle_AI_input(
                    location=self._location, 
                    turnCharacter=turnCharacter,
                    charactersInfo=self._order,
                    randomAction=self._enemy_actions[randomActionNum]
                )}
            else:
                return None
            
    def get_action_response(self, prompt_input: str, turnCharacter: Character):
        response = chat_complete_battle(
            prompt_input, 
            location=self._location,
            turnCharacter=turnCharacter,
            charactersInfo=self._order
        )

        if response:
            self._battle_events = response.get('events')
            self._location = response.get('location')
            self._order = response.get('characters')
        
        return response
    
    def resolve_turn(self, turnCharacter: Character):
        print(f"End of {turnCharacter.name}'s turn\n")
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
            print(f"Turn complete. Starting Turn {self._turn}")

            # Figure out who is going / Check order array (purely to assign input to character)
            # Send call with input and object metadata
            # Use response to update global battle_events
            # Return 0
            # // Outside (App.py)
            #   Fetch global battle_events
            #   Post to dialogue

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
                'enemies': enemies,
                'outcome': self._battle_result,
                'prompt_input': "END"
                }

    def get_battle_events(self):
        # Return new events generated per turn
        return self._battle_events

    def get_turn_character(self):
        return self._turnCharacter

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
