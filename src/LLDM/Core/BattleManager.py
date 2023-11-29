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

class Battle():
    ## Initialize the battle object
    '''
    If you want to start a battle, you must provide:
      - Location (Scene object)
      - Enemies (List of Character objects which would be the mobs)
      - Party (List of Character objects which would be the party)
        - Can add neutral / helpful NPCs into party for now, might separate later

    Example: 
      battle = Battle(location, enemies, party)
      response = battle.start_battle() # Battle will update party accordingly
      party = response["party"]

      ## If needed
      # enemies = response["enemies"]
      # location = response["location"]
    '''
    # TODO: Character Annotations now just optional attributes of Character, account for this
      # Update Motivations, surprise, distance for each (Defaults: normal (mood), surprise factor of 0 (no effect), distance factor of 0 (no effect), normal (state / status))
    def __init__(self, location: Scene, enemies:[], party: [], turnLimit=1000, TESTMODE=False):
        self.TESTMODE = TESTMODE
        self._actions = ["Attack", "Wait"]
        
        self._location = location
        self._create_full_Character_list_([party, enemies])
        self._party_alive_count = len(party)
        self._enemy_alive_count = len(enemies)
        self._dead = []
        self._ran_away = []
        self._turnLimit = turnLimit

    def start_battle(self):
        # Before battle starts
        print("Starting Battle\n")
        self._assign_initiative_()
        self._turn = 1
        self._battle_result = "unknown"
        self._character_index = 0

        print(f"Current Turn: {self._turn}")
        # Check that there is still at least one of each team left
        while (self._party_alive_count > 0 and self._enemy_alive_count > 0):
            self.current_turn()
            
            self._order[:] = [info for info in self._order if info[1].health > 0]
            orderSize = len(self._order)

            self._character_index = (min(self._character_index, orderSize-1) + 1) % orderSize
            if (self._character_index == 0):
                self._turn += 1
                # self._reset_temp_mods()

                if (self._turnLimit < self._turn):
                    break
                
                print(f"Turn complete. Starting Turn {self._turn}")

        print("Battle Complete\n")
        return self.finalize_objects()

    def current_turn(self):
        turnCharacter = self._order[self._character_index][1]
        print(f"It is currently {turnCharacter.name}'s time to act!")

        while True:
            if (self.TESTMODE or turnCharacter.npc):
                print(f"Prompting for {turnCharacter.name}'s action")
                randomActionNum = 0 if self.TESTMODE else random.randint(0, len(self._actions)-1)
                prompt_input = chat_complete_battle_AI_input(location=self._location, turnCharacter=turnCharacter, charactersInfo=self._order, randomAction=self._actions[randomActionNum])
            else:
                print(f"Give {turnCharacter.name} something to do this turn. Provide target and other information as needed: ")
                prompt_input = str(input())

            response = chat_complete_battle(prompt_input, location=self._location, turnCharacter=turnCharacter, charactersInfo=self._order)

            if response:
                # self._events = response.get('events')
                self._location = response.get('location')
                self._order = response.get('characters')
                break

        print(f"End of {turnCharacter.name}'s turn\n")


    #########################################
    #
    #          Pre-Battle Functions
    #
    #########################################

    def _create_full_Character_list_(self, teams: []):
        self._order = []
        for team in teams:
            for character in team:
                self._order.append((5, character))

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

    def finalize_objects(self):
        party = []
        enemies = []

        for info in self._order:
            party.append(info[1]) if info[1].entity == 'party' else enemies.append(info[1])

        return {'party': party,
                'dead': self._dead,
                'location': self._location,
                'enemies': enemies
                }

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