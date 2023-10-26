from LLDM.Objects.DungeonEnums import *
from LLDM.Objects.CharacterArchitecture import *


race = Race("Human")
class1 = Class("Artificer", 1)
background = Background("Sage")
character = Character("test", race, class1, background)

print(character)
