import json
from enum import Enum

Races = None
Subraces = None
Backgrounds = None
Classes = None
Subclasses = None


def load_enum(filename, enum_name, primary_key):
    print(f'Loading [{filename}] into Enum:[{enum_name}]')

    with open(filename, "r") as file:
        file_data = json.load(file)

    dictionary = {record[primary_key].replace(' ', '_').replace('-', '_'): record for record in file_data}

    globals()[enum_name] = Enum(enum_name, dictionary)


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
