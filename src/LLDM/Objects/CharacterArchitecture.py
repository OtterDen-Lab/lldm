from enum import Enum

from LLDM.Objects.PrettyPrinter import NestedFormatter
from LLDM.Objects import DungeonEnums


# This is a slightly different take on building hierarchies than the WorldArchitecture.
# Each of these classes are far more rigid, but fleshed out:
# By accessing Enums in DungeonEnums for data, I can set up a mock database to test values.
# One drawback is that Enums are immutable, meaning I can't create more classes or backgrounds on the fly.
# It's likely the enums may be replaced by JSON/Dicts to gain that dynamic mutability, so I've made it easer to convert
# That doesn't mean I can't change the values of created objects, either: I can make and use getter/setters.
# WARNING!!!: TODO: Remove (or just move) hardcoded Enum Loading:
#  DungeonEnums.load_enum('background_data.json', 'Backgrounds', 'name')
#
# Note to self: Type checking in Python is so stupid.
#
# Important: BATTLE DESIGN: I have purposefully omitted certain Setters.
# You can only change the following:
# Character name & Class level.
# Future: Set character size as a new field, and then reset to immutable Race size.

# TODO: Create a Feature class to hold gameplay properties
class Background(NestedFormatter):
    DungeonEnums.load_enum('background_data.json', 'Backgrounds', 'name')

    def __init__(self, background, origin: str = None, personality: str = None, ideals: str = None, bonds: str = None, flaws: str = None):
        enum_member = _get_enum_member(background, DungeonEnums.Backgrounds)
        record = enum_member.value
        self._name = record.get('name')
        self._description = record.get('description')

        # TODO: Figure out where/how to implement these details
        self._origin = origin
        self._personality = personality
        self._ideals = ideals
        self._bonds = bonds
        self._flaws = flaws

    @property
    def name(self):
        return self.name

    @property
    def description(self):
        return self._description


class Race(NestedFormatter):
    DungeonEnums.load_enum('race_data.json', 'Races', 'name')
    DungeonEnums.load_enum('subrace_data.json', 'Subraces', 'name')

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
            sub_member = _get_enum_member(subrace, DungeonEnums.Subraces)
            sub_record = sub_member.value
            if self.name == sub_record.get('parent'):
                self._subrace = sub_record.get('name')
            # else:
            #     raise ValueError(f"Invalid Subrace: {record.get('parent')} does not have a {record.get('name')}")

    @property
    def name(self):
        return self._name

    @property
    def subrace(self):
        return self._subrace

    @property
    def size(self):
        return self._size


class Class(NestedFormatter):
    DungeonEnums.load_enum('class_data.json', 'Classes', 'name')
    DungeonEnums.load_enum('subclass_data.json', 'Subclasses', 'name')

    # TODO: Include class features

    def __init__(self, class_name, level: int, subclass=None):
        enum_member = _get_enum_member(class_name, DungeonEnums.Classes)
        record = enum_member.value
        self.name = record.get('name')
        self._sub_class = None
        self.level = level
        self._hit_die = record.get('hit_dice')
        self._spell_casting_attr = record.get('spellcasting_mod')


        # TODO: Include subclass features (remove 'name' and attach more date)
        # Set Subclass name and based on Enum Dict, and look for Spellcasting modifier if None
        if record.get('subclasses') > 0 and subclass is not None:
            sub_member = _get_enum_member(subclass, DungeonEnums.Subclasses)
            sub_record = sub_member.value
            self._sub_class = sub_record.get('name')
            self._spell_casting_attr = sub_record.get('spellcasting_mod')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int):
        if 0 < value <= 20:
            self._level = value
        else:
            raise TypeError("Invalid Level / Not Integer between 1 and 20 inclusive")

    @property
    def sub_class(self):
        return self._sub_class

    @property
    def hit_die(self):
        return self._hit_die

    @property
    def spell_casting_attr(self):
        return self._spell_casting_attr


class Character(NestedFormatter):
    def __init__(self,
                 name: str,
                 raceObj: Race,
                 classObj: Class,
                 backgroundObj: Background,
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

        self.name = name
        self._race = raceObj
        self._class = classObj
        self._background = backgroundObj

        # TODO: Implement these incomplete fields
        self._description = description
        self._xp = xp
        self._details = details
        self._gear_proficiency = gear_proficiency
        self._treasure = treasure

        self.feats = feats if feats is not None else []
        self.spells = spells if spells is not None else []
        self.weapons = weapons if weapons is not None else []
        self.equipment = equipment if equipment is not None else []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def race(self):
        return self._race

    @property
    def class_(self):
        return self._class

    @property
    def background(self):
        return self._background


def _get_enum_member(obj, enum_class: DungeonEnums):
    print(f'Creating [{enum_class}] with: [{type(obj)}]')
    if isinstance(obj, str):
        # print(f'Searching for [{obj}] in: {enum_class}')
        if obj in enum_class.__members__:
            # print(f'Found: [{enum_class[obj]}] in Enums(Member Key) Containing: {enum_class[obj].value}')
            return enum_class[obj]
        else:
            print(f'{obj} is not in {enum_class} as an Enum member key... is this a raw data value (name)?')
            for member in enum_class.__members__.values():
                if member.value['name'] == obj:
                    # print(f'Found: [{member}] in raw dict data. Containing: {member.value}')
                    return member

    elif isinstance(obj, Enum):
        # print(f'Searching for Enum:[{obj}] in: {enum_class.__members__}')
        if obj in enum_class:
            # print(f'Found: [{obj}] in Enums(Object). Containing: {obj.value}')
            return obj

    elif isinstance(obj, dict):
        # print(f'Searching for Dict:[{obj}] in: {enum_class.__members__}')
        raise NotImplementedError

    raise ValueError("Invalid: Double-Check parameters for missing or NoneType values")
