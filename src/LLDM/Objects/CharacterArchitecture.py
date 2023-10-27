from enum import Enum

from LLDM.Objects.PrettyPrinter import NestedFormatter
from LLDM.Objects import DungeonEnums


# This is a slightly different take on building hierarchies than the WorldArchitecture.
# Each of these classes are far more rigid, but fleshed out:
# By accessing Enums in DungeonEnums for data, I can setup a mock database to test values.
# One drawback is that Enums are immutable, meaning I can't create more classes or backgrounds on the fly.
# It's likely the enums may be replaced by JSON/Dicts to gain that dynamic mutability, so I've made it easer to convert
# That doesn't mean I can't change the values of created objects, either: I can make and use getter/setters.

# Note to self: Type checking in Python is stupid.


# TODO: Create a Feature class to hold gameplay properties
class Character(NestedFormatter):
    def __init__(self,
                 name,
                 raceObj,
                 classObj,
                 backgroundObj,
                 # TODO: Continue creating more objects
                 details=None,
                 description=None,
                 xp=None,
                 gear_proficiency=None,  # weapon_profs=None,armor_profs=None,tool_profs=None,
                 feats=None,
                 spells=None,
                 weapons=None,
                 equipment=None,
                 treasure=None
                 ):

        self._name = name
        if isinstance(raceObj, Race):
            self._race = raceObj
        else:
            raise TypeError("Invalid Race")

        if isinstance(classObj, Class):
            self._class = classObj
        else:
            raise TypeError("Invalid Class")

        if isinstance(backgroundObj, Background):
            self._background = backgroundObj
        else:
            raise TypeError("Invalid Background")

        # TODO: Implement these incomplete fields
        if description is not None:
            self._description = description
        if xp is not None:
            self._xp = xp

        if details is not None:
            self._details = details
        if gear_proficiency is not None:
            self._gear_proficiency = gear_proficiency
        if treasure is not None:
            self._treasure = treasure

        self.feats = feats if feats is not None else []
        self.spells = spells if spells is not None else []
        self.weapons = weapons if weapons is not None else []
        self.equipment = equipment if equipment is not None else []


class Background(NestedFormatter):
    DungeonEnums.init_backgrounds()

    def __init__(self, background, origin=None, personality=None, ideals=None, bonds=None, flaws=None):
        enum_member = _get_enum_member(background, DungeonEnums.Backgrounds)
        record = enum_member.value
        self._name = record.get('name')
        self._description = record.get('description')

        # TODO: Figure out where/how to implement these details
        if origin is not None:
            self._origin = origin
        if personality is not None:
            self._personality = personality
        if ideals is not None:
            self._ideals = ideals
        if bonds is not None:
            self._bonds = bonds
        if flaws is not None:
            self._flaws = flaws


class Race(NestedFormatter):
    DungeonEnums.init_races()
    DungeonEnums.init_subraces()
    # Description, size, traits, actions, senses are all computed with name and subtype.
    # TODO: Include racial features

    def __init__(self, race, subrace=None):
        enum_member = _get_enum_member(race, DungeonEnums.Races)
        record = enum_member.value
        self._name = record.get('name')
        self._subrace = None
        self._size = record.get('size')

        # Check if subrace is required
        if record.get('subraces') > 0:
            enum_member = _get_enum_member(subrace, DungeonEnums.Subraces)
            record = enum_member.value
            if self._name == record.get('parent'):
                self._subrace = record.get('name')
            # else:
            #     raise ValueError(f"Invalid Subrace: {record.get('parent')} does not have a {record.get('name')}")


class Class(NestedFormatter):
    DungeonEnums.init_classes()
    DungeonEnums.init_subclasses()
    # TODO: Include class features

    def __init__(self, cls, level, subclass=None):
        enum_member = _get_enum_member(cls, DungeonEnums.Classes)
        record = enum_member.value
        self._name = record.get('name')
        self._sub_class = None
        self._hit_die = record.get('hit_dice')
        self._spell_casting_attr = record.get('spellcasting_mod')

        if 0 < level <= 20:
            self._level = level
        else:
            raise TypeError("Invalid Level / Not Integer between 1 and 20 inclusive")

        # TODO: Include subclass features (remove 'name' and attach more date)
        # Set Subclass name and based on Enum Dict, and look for Spellcasting modifier if None
        if record.get('subclasses') > 0 and subclass is not None:
            enum_member = _get_enum_member(subclass, DungeonEnums.Subclasses)
            record = enum_member.value
            self._sub_class = record.get('name')
            self._spell_casting_attr = record.get('spellcasting_mod')


def _get_enum_member(obj, enum_class):
    print(f'Creating [{enum_class}] with: [{type(obj)}]')
    if isinstance(obj, str):
        # print(f'Searching for Key:[{obj}] in: {enum_class.__members__}')
        if enum_class[obj]:
            print(f'Found: [{enum_class[obj]}] Containing: {enum_class[obj].value}')
        return enum_class[obj]

    elif isinstance(obj, Enum):
        # print(f'Searching for Enum:[{obj}] in: {enum_class.__members__}')
        if obj in enum_class:
            print(f'Found: [{obj}] Containing: {obj.value}')
            return obj

    elif isinstance(obj, dict):
        # print(f'Searching for Dict:[{obj}] in: {enum_class.__members__}')
        raise NotImplementedError

    raise ValueError("Invalid: Double-Check parameters for missing or NoneType values")
