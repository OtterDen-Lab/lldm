from enum import Enum

from LLDM.Objects.ItemArchitecture import Item, Weapon
from LLDM.Objects.PrettyPrinter import NestedFormatter

from pymongo import MongoClient


# Understanding WHEN to Read & Write to Mongo:
# Example: Getting appropriate loot from a dungeon
#
# Event: Player finds a Chest in Dungeon
# ChatCompletion Function trigger: genContainer(Scene)
# Read: Scene object from Mongo (contains full world details)
# GPT generates a Container(Name, Contents)
# Write: Chest to MongoDB's Scene>World>>>Location
#
# Event: Player opens Chest in Dungeon
# ChatCompletion Function trigger: dropLoot(Player, Chest)
# Read: Player>Inventory from Mongo
# Read: Chest>Contents from Mongo
# Script: Add Contents to Inventory in Python
# Script: Remove Contents from Chest in Python
# Write: Save Updated Character to Mongo
# Write: Save Updated Chest to Mongo

#
# GPT returns Weapon JSON
# Script creates Python Object from JSON
#   WeaponObj is now usable in-script (can be passed to other scripts if necessary)
#   Isolated Methods do not have access (Ex. NPC_gen() only reads DB, so doesn't have access)
#
# Script stores Python Object in Mongo
#   WeaponObj_JSON is now accessible to ALL readers
#
# Note: Atomically store upon creation, atomically store upon modification (and deletion)
#   Then, only use reads or passes of reads.


# Connection
client = MongoClient('localhost', 8192)
# Database
db = client['LLDM']
# Collections (= Tables)
background_collection = db['background']
class_collection = db['class']
race_collection = db['race']
character_collection = db['character']


class Background(NestedFormatter):
    def __init__(self, name, summary: str = None, personality: str = None, skills=None, motivations=None, bonds=None, flaws=None):
        record = background_collection.find_one({"name": name})
        self.name = record.get('name')
        if summary is None:
            self.summary = record.get('summary')
        else:
            self.summary = summary

        self.personality = personality
        self.skills = skills
        self.motivations = motivations
        self.bonds = bonds
        self.flaws = flaws

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def personality(self):
        return self._personality

    @personality.setter
    def personality(self, value):
        self._personality = value

    @property
    def skills(self):
        return self._skills

    @skills.setter
    def skills(self, value):
        self._skills = value

    def add_skill(self, value: str):
        self._skills.add(value)

    @property
    def motivations(self):
        return self._motivations

    @motivations.setter
    def motivations(self, value):
        self._motivations = value

    def add_motivation(self, value: str):
        self._motivations.add(value)

    @property
    def bonds(self):
        return self._bonds

    @bonds.setter
    def bonds(self, value):
        self._bonds = value

    def add_bond(self, value: str):
        self._bonds.add(value)

    @property
    def flaws(self):
        return self._flaws

    @flaws.setter
    def flaws(self, value):
        self._flaws = value

    def add_flaw(self, value: str):
        self._flaws.add(value)


class Race(NestedFormatter):
    # Description, size, traits, actions, senses are all computed with name and subtype.

    def __init__(self, race, subrace=None):
        record = race_collection.find_one({"name": race})
        # for record in result:
        #     print(record)
        # record = enum_member.value
        self._name = record.get('name')
        self._subrace = None
        self._size = record.get('size')

        # Check if subraces exist- if they do, try to set it to the parameter
        if subrace in record.get('subraces'):
            self._subrace = subrace

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
    def __init__(self, class_name, level: int, subclass=None):
        record = class_collection.find_one({"name": class_name})
        self._name = record.get('name')
        self._sub_class = None
        self.level = level
        self._hit_die = record.get('hit_dice')

        if subclass is not None and subclass in record.get('subclasses'):
            self._sub_class = subclass

    @property
    def name(self):
        return self._name

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


class Stats(NestedFormatter):
    def __init__(self, classObj: Class, inventory):
        self._speed = 30
        self._max_health = classObj.hit_die
        self._health = self._max_health
        self._armor = 10


class Condition(NestedFormatter):
    def __init__(self, name: str, duration: int, effect: str = None):
        self._name = name
        self._duration = duration
        self._effect = effect


class Character(NestedFormatter):
    def __init__(self, name: str, race: Race, classes, background: Background, weapons=None, inventory=None, xp: int = None, gold: int = None):
        # Mandatory
        self._name = name  # String
        self._race = race  # Race Object
        self._background = background  # Background Object
        self._classes = classes  # List of Class Objects

        # Computed
        self._stats = Stats(classes[0], inventory)
        self._conditions = None

        # Optional
        self._xp = xp  # Experience
        self._gold = gold  # Gold
        self._weapons = weapons if weapons is not None else []  # List of Weapon Objects
        self._inventory = inventory if inventory is not None else []  # List of Item Objects

    def add_weapon(self, weapon: Weapon):
        self._weapons.append(weapon)

    def add_item(self, item: Item):
        self._inventory.append(item)

    def add_condition(self, condition: Condition):
        self._conditions.append(condition)
