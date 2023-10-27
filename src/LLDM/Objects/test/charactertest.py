from LLDM.Objects import DungeonEnums
from LLDM.Objects.CharacterArchitecture import Background, Class, Race

# acolyte_dict = {'name': 'Acolyte', 'description': 'a acolyte'}

# background_str = Background("Acolyte")
# print(background_str)
#
# background_hard = Background(DungeonEnums.Backgrounds.Acolyte)
# print(background_hard)
#
race_str = Race("Elf", "Wood")
print(race_str)

race_hard = Race(DungeonEnums.Races.Elf, DungeonEnums.Subraces.Wood)
print(race_hard)

# class_str = Class("Fighter", 2, "Eldritch Knight")
# print(class_str)

# class_hard = Class("Artificer", 2)
# print(class_hard)

# race = Race("Human")
# class1 = Class("Artificer", 1)
# background = Background("Sage")
# character = Character("test", race, class1, background)
# print(character)
