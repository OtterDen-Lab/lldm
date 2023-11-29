from LLDM.Core.Scene import Character
# Interactive Character Creator
# Use Core.Scene's Character.

class CharGen():
    def __init__(self):
        self.loo = []
        self.userI = ""

    def user_character(self):
        self.userInput = input()
        self.loo = self.userInput.split(", ")
        print("what do they have? Item(name, dec, damage: , amount: ). If they don't have anything input \"n\"")
        self.userInput = input()
        items = []
        textExtracted = []
        if self.userInput == "n":
            return Character(self.loo[0], self.loo[1], int(self.loo[2]), int(self.loo[3]), items)
        textExtracted = self.userInput.split(", ")
        counter = 2
        while counter < len(textExtracted):
            separated = textExtracted[counter].split("=")
            separated[0].lower()
            damage = amount = None
            
            if separated[0] == "damage":
                damage = int(separated[1])
            elif separated[0] == "amount":
                amount = int(separated[1])
            
            items.append(Item(textExtracted[counter - 2], textExtracted[counter - 1], damage=damage, amount=amount))
            counter += 3
        return Character(self.loo[0], self.loo[1], int(self.loo[2]), int(self.loo[3]), items)
        #? for now

    def user_character_other(name:str, type:str, hp:int, dex_mod:int, objects:list):
        return Character(name, type, hp, dex_mod, objects)

    def setup_default_character():
        return Character("player1", "party", 100, 5, [])