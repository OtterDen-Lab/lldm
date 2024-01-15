# GameLogic manages game states to determine whether there is an ongoing battle.
# This module is intended to serve a middle-man layer between Main, GPT, BattleManager, and WebApp
import random

from LLDM.Core.BattleGPT import chat_complete_battle_AI_input, chat_complete_battle_resolve, \
    chat_complete_battle_player_input, generate_conclusion


class Battle:
    _in_battle = False
    current_battle = None
    enemy_actions = ["Attack", "Wait"]
    active_player = None

    @classmethod
    def in_battle(cls):
        return cls._in_battle

    @classmethod
    def start_battle(cls, scene):
        if cls.in_battle():
            print("Already in a Battle!")
            return

        cls._in_battle = True
        print("Starting Battle\n")
        Battle(scene)
        return cls.cycle_logs()

    @classmethod
    def cycle_logs(cls):
        new_events = cls.current_battle.get_events()
        cls.current_battle.empty_events()
        return new_events

    def next_turn(self, acting_char):
        if not Battle.in_battle():
            print("Not in a Battle!")
            return

        print(f"{acting_char.name}(id:{acting_char.id})'s Turn!")
        self._battle_events.append(f"{acting_char.name}(id:{acting_char.id})'s Turn!")

        if acting_char.npc:
            self.ai_turn(acting_char)
        else:
            # Section executed as the terminal clause of AI turns
            # acting_char should reference a Player, so set up the class var for Process [which will call next_turn()]
            Battle.active_player = acting_char
            print(f"Set active to {acting_char.name}(id:{acting_char.id})")
            # Wait for <input>, which is main's handle_input()

    def ai_turn(self, acting_char):
        # Steps for AI during Battles:
        # Generate Action and Execute in one call.
        print(f"Targets: " + ' '.join(str(target.name) for target in self._living_party))

        # Auto-Generate Prompt [Returns an Event)
        prompt_input = chat_complete_battle_AI_input(
            location=self._location,
            self=acting_char,
            targets='\n'.join(f"{target.name} (id:{target.id})" for target in self._living_party),
            action=Battle.enemy_actions[random.randint(0, len(self.enemy_actions) - 1)]
        )

        # Execute Resolved Input
        response = chat_complete_battle_resolve(
            prompt_input,
            self=acting_char,
            targets=self._living_party
        )

        # Cleanup
        self.cleanup(response)

    def player_turn(self, acting_char, user_input):
        # Execute GPT calls to handle player input
        print(f"Enemies: " + ' '.join(str(enemy.name) for enemy in self._living_enemies))

        # Produce Event from raw input
        battle_event = chat_complete_battle_player_input(
            user_input,
            self=acting_char,
            targets='\n'.join(f"{enemy.name} (id:{enemy.id})" for enemy in self._living_enemies),
        )

        # Execute Resolved Input
        response = chat_complete_battle_resolve(
            battle_event,
            self=acting_char,
            targets=self._living_enemies
        )

        # Cleanup
        self.cleanup(response)

    def cleanup(self, response):
        if response:
            # Log Accrued Battle Events
            for event in response.get('events'):
                self._battle_events.append(event)

            # Use Response's packed items to update characters
            updated_chars = response.get('updated_chars')
            for character in updated_chars:
                self.update_char(character)

        # Cleanup Check
        if len(self._living_party) == 0 or len(self._living_enemies) == 0:
            print("Battle Ended!")
            self._battle_events.append("Battle Ended!")
            Battle._in_battle = False

            # Use GPT to generate a short recap of the events
            self._battle_events.append(generate_conclusion(self._battle_events))

        else:
            # Recurse until User Input is required.
            self.next_turn(self.find_next_living_character())

    def find_next_living_character(self):
        while True:
            self._turn = (self._turn + 1) % len(self._order)
            if self._order[self._turn].alive:
                break
        return self._order[self._turn]

    def get_events(self):
        return self._battle_events

    def empty_events(self):
        self._battle_events = []

    def update_char(self, updated_char):
        # faction-agnostic update a character across relevant lists (Living List, Order)
        target_index = None
        for i, character in enumerate(self._living_party if updated_char.entity == "party" else self._living_enemies):
            if character.id == updated_char.id:
                target_index = i
                break

        if updated_char.entity == "party":
            if not updated_char.alive:
                self._living_party.pop(target_index)
            else:
                self._living_party[target_index] = updated_char
        else:
            if not updated_char.alive:
                self._living_enemies.pop(target_index)
            else:
                self._living_enemies[target_index] = updated_char

        # Order does remove dead characters
        for i, character in enumerate(self._order):
            if character.id == updated_char.id:
                target_index = i
                break

        self._order[target_index] = updated_char

    def __init__(self, scene):
        # Unpack Entities from Scene
        self._location = scene.loc_map.current_location

        self._dead = []
        self._ran_away = []

        self._living_party = []
        self._living_enemies = []
        self._order = self.initiative(scene.characters)

        self._turn = 0
        self._battle_result = "unknown"
        self._battle_events = []

        self.next_turn(self._order[0])
        Battle.current_battle = self

    def initiative(self, all_characters):
        # Unpack participating characters and sort them by their Dexterity
        incl_chars = []
        for character in all_characters:
            if character.entity == "party" or character.entity == "enemy":
                if character.entity == "party":
                    self._living_party.append(character)
                else:
                    self._living_enemies.append(character)

                incl_chars.append(character)

        return sorted(incl_chars, key=lambda char: char.dexterity, reverse=True)
