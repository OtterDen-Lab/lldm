from ..Scene import Character


# Interactive Character Creator
# TODO: Expand this Chara cter creator to ask the user for input to set its name and inventory.
# Add functions for backstory, motivations, physical features if you have time.
# Use Core.Scene's Character.
class CharGen():
    def __init__(self):
        self.loo = []
        self.userI = ""

    def user_character():
        loo = []
        userInput = input()
        loo = userInput.split(" ")
        #? for now
        return Character(loo[0], int(loo[1]), int(loo[2]))

    def setup_default_character():
        return Character("player1", "party", 100, 5)