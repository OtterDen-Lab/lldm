from enum import Enum

from LLDM.Objects.PrettyPrinter import NestedFormatter


from pymongo import MongoClient

# Connection
client = MongoClient('localhost', 8192)
# Database
db = client['LLDM']
# Collections (= Tables)
backgrounds = db['background']
classes = db['class']
subclasses = db['subclass']
races = db['race']
subraces = db['subrace']


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
    def __init__(self, background, origin: str = None, personality: str = None, ideals: str = None, bonds: str = None, flaws: str = None):
        record = backgrounds.find_one({"name": background})
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
    # Description, size, traits, actions, senses are all computed with name and subtype.
    # TODO: Include racial features

    def __init__(self, race, subrace=None):
        record = races.find_one({"name": race})
        # for record in result:
        #     print(record)
        # record = enum_member.value
        self._name = record.get('name')
        self._subrace = None
        self._size = record.get('size')

        # Check if subrace is required
        if record.get('subraces') > 0:
            sub_record = subraces.find_one({"name": subrace})
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
    # TODO: Include class features

    def __init__(self, class_name, level: int, subclass=None):
        record = classes.find_one({"name": class_name})
        self.name = record.get('name')
        self._sub_class = None
        self.level = level
        self._hit_die = record.get('hit_dice')
        self._spell_casting_attr = record.get('spellcasting_mod')

        # TODO: Include subclass features (remove 'name' and attach more date)
        if record.get('subclasses') > 0 and subclass is not None:
            sub_record = subclasses.find_one({"name": subclass})
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

