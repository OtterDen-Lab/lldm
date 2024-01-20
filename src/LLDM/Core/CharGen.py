from LLDM.Core.Character import Character
from LLDM.Core.Item import Item


# Character Creator
# TODO: Expand this Character creator to ask the user for input to set its name and inventory.


def new_npc():
    """Returns a hard-coded Enemy NPC Character"""
    return Character("Goblin", 100, 10, 10, 1, "enemy", True)


def starter_character():
    """Inits and returns a starter Player Character"""
    sword = Item("Sword", "A sturdy blade crafted from the finest steel.", damage=15, amount=1)
    potion = Item("Health Potion", "A small vial of red liquid.", healing=10, amount=1)
    return Character("Ray", 50, 10, 10, 2, "party", False, inventory=[sword, potion])
