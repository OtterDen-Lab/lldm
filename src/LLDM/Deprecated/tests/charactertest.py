from LLDM.Deprecated.Objects.CharacterArchitecture import Background, Class, Race, Character
from LLDM.Deprecated.Objects.ItemArchitecture import Potion, Damage, Weapon

# Notes:
# Classes do NOT require subclasses.
# I've made name checking as robust as I can, but be careful with spaces & hyphens. ("Half-Elf" & "Wood Elf Heritage")

# Test Character
race = Race("Half-Elf", "Wood Elf Heritage")
class1 = Class("Fighter", 2, "Eldritch Knight")
background = Background("Outlander")
character = Character("Ray", race, [class1], background)

# Test Items
health_pot = Potion("Healing Potion", "Heals you")
sword = Weapon("Sword", "Melee", Damage(8, 1, "Slashing"), "A gleaming blade")
character.add_item(health_pot)
character.add_weapon(sword)  # TODO Turn this into a factory method: calling add_item(WEAPON) should use add_weapon()

print(character)

# Notes: First Draft on revised Entities. A lot of things left to do:
# I've done the best I can to make sure that the new MongoSchema .json are correct (and match character.json).
# But I'm not perfect, so keep an eye out for sly typos/bugs/inconsistencies between character, the other jsons, & mongo
#
# Add method to remove Conditions & Items/Weapons from Character
#
# Understand why we don't need component classes in the database:
#   Things like 'Damage', 'Stats', and maybe 'Condition' shouldn't exist in Mongo = They can't exist on their own.
#   They can and should be made inside Python, on the fly, whenever we need them.
#
# Figure out how to merge Weapons & Items
# Need ENUMs or other methods to ensure: Category, Weapon Type, Dice_Type, and Damage_Type are all Valid Strings
#
