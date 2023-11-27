from LLDM.Core.Scene import Character


# Interactive Character Creator
# TODO: Expand this Character creator to ask the user for input to set its name and inventory.
# Add functions for backstory, motivations, physical features if you have time.
# Use Core.Scene's Character.

def setup_character():
    return Character("player1", 100, 10, 10, entity="party")
