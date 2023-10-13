# What does a Campaign Object have?
# World (Regions / Countries / Cities
# Party (Character[])
# Quests (Quest[])

def create_character(character_json):
    return character_json


class Campaign:
    def __init__(self, world=None, party=None, quests=None):
        if quests is None:
            quests = []
        if party is None:
            party = []
        self.world = world
        self.party = party
        self.quests = quests

    def add_character(self, character):
        self.party.append(character)

    def add_quest(self, quest):
        self.quests.append(quest)

    def __str__(self):
        party_str = "\n".join(str(char) for char in self.party) if self.party else "None"
        quest_str = "\n".join(str(quest) for quest in self.quests) if self.quests else "None"
        return f"World:\n{self.world}\n\nParty:\n{party_str}\n\nQuests:\n{quest_str}"
