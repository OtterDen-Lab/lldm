import json
from enum import Enum

Races = None
Subraces = None
Backgrounds = None
Classes = None
Subclasses = None


def init_backgrounds():
    print("Initializing Enum: Background")
    global Backgrounds
    with open('background_data.json', "r") as file:
        background_data = json.load(file)
    background_dict = {record['name']: record for record in background_data}
    Backgrounds = Enum('Backgrounds', background_dict)


def init_races():
    print("Initializing Enum: Race")
    global Races
    with open('race_data.json', "r") as file:
        race_data = json.load(file)
    race_dict = {record['name']: record for record in race_data}
    Races = Enum('Races', race_dict)


def init_classes():
    print("Initializing Enum: Class")
    global Classes
    with open('class_data.json', "r") as file:
        class_data = json.load(file)
    class_dict = {record['name']: record for record in class_data}
    Classes = Enum('Classes', class_dict)


def init_subclasses():
    print("Initializing Enum: Subclass")
    global Subclasses
    with open('subclass_data.json', "r") as file:
        subclass_data = json.load(file)
    subclass_dict = {record['name']: record for record in subclass_data}
    Subclasses = Enum('Subclasses', subclass_dict)


def init_subraces():
    print("Initializing Enum: Subrace")
    global Subraces
    with open('subrace_data.json', "r") as file:
        subrace_data = json.load(file)
    subrace_dict = {record['name']: record for record in subrace_data}
    Subraces = Enum('Subraces', subrace_dict)


class Attributes(Enum):
    STR = "STR"
    DEX = "DEX"
    CON = "CON"
    INT = "INT"
    WIS = "WIS"
    CHA = "CHA"


class Size(Enum):
    TINY = "TINY"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    HUGE = "HUGE"
    GARGANTUAN = "GARGANTUAN"
