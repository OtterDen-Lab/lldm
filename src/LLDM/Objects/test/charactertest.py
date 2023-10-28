from LLDM.Objects import DungeonEnums
from LLDM.Objects.CharacterArchitecture import Background, Class, Race, Character


# Staging ground to test Object creation.
# Currently, handles Strings e.g. "Acolyte", and Enum Members e.g. DungeonEnums.Backgrounds.Acolyte
# Spaces are supported in String, provided that they are also the same in their 'name' attribute.
# e.g. "Eldritch Knight" and "Eldritch_Knight" and DungeonEnums.Subclasses.Eldritch_Knight ALL WORK
#
# Notes:
# Some 5e Races have required Subraces, and will error if left empty.
# Classes do NOT require subclasses.
# I've made name checking as robust as I can, but be careful with spaces & hyphens. ("Half-Elf" & "Wood Elf Heritage")

race = Race("Half-Elf", "Wood Elf Heritage")
class1 = Class("Fighter", 2, DungeonEnums.Subclasses.Eldritch_Knight)
background = Background("Sage")
character = Character("Ray", race, class1, background)
print(character)
