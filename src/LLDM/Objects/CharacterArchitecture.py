from enum import Enum

from .PrettyPrinter import NestedFormatter
from .DungeonEnums import Attributes, Size, Classes, Subclasses, Races, Subraces, Backgrounds


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
    def __init__(self, background_name, origin=None, personality=None, ideals=None, bonds=None, flaws=None):
        # TODO: Include description of background (in enum?)
        background_enum = getattr(Backgrounds, background_name, None)
        if background_enum is None:
            raise ValueError("Invalid Background / Background not in Enum")

        record = background_enum.value
        self._name = record.get('name')

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
    # TODO: Include racial features
    def __init__(self, race_name: str, subrace=None):
        # Currently using a very complicated str->enum->record, but it'll be easy to adapt to Dict/JSOn if needed
        # Description, size, traits, actions, senses are all computed with name and subtype.
        race_enum = getattr(Races, race_name, None)
        if race_enum is None:
            raise ValueError("Invalid Race / Race not in Enum")

        # grab the enum's value (a dictionary)
        record = race_enum.value
        self._name = record.get('name')
        self._size = record.get('size')

        # Check if subrace is required
        if record.get('subraces') > 0:
            if subrace is not None and subrace in Subraces:
                # TODO: Include subrace features (remove 'name' and attach more date)
                self._subrace = getattr(Subraces, subrace, None).value.get('name')
            else:
                raise ValueError("Subrace required but invalid / not found in Enum")


class Class(NestedFormatter):
    # TODO: Include class features
    def __init__(self, class_name: str, level, subclass=None):
        if 0 < level <= 20:
            self._level = level
        else:
            raise TypeError("Invalid Level / Not Integer between 1 and 20 inclusive")

        # Set Class name, Hit Dice, and Spellcasting modifier based on Enum Dict
        class_enum = getattr(Classes, class_name, None)
        if class_enum is None:
            raise ValueError("Invalid Class / Class not in Enum")

        record = class_enum.value
        self._name = record.get('name')
        self._hit_die = record.get('hit_dice')
        self._spell_casting_attr = record.get('spellcasting_mod')

        # TODO: Include subclass features (remove 'name' and attach more date)
        # Set Subclass name and based on Enum Dict, and look for Spellcasting modifier if None
        if record.get('subclasses') > 0 and subclass is not None:
            if subclass in Subclasses:
                record = getattr(Subclasses, subclass, None).value
                self._name = record.get('name')
                self._spell_casting_attr = record.get('spellcasting_mod')
            else:
                raise ValueError("Invalid Subclass / Subclass not in Enum")

