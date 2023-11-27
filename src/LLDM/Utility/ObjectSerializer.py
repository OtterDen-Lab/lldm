from json import JSONEncoder
import json
from LLDM.Deprecated.Objects.WorldArchitecture import *

# from LLDM.Deprecated.WorldArchitecture import World, Continent, Region, City, Site, CityDistrict, Building
#
#
# This class serves as a Factory to build hierarchical game objects.
# It includes helper methods to convert nested objects to and from json/dicts


# Map Class names to their respective Types, to be used by the Factory to create instances based on dict keys
CLASS_MAP = {
    'World': World,
    'Continent': Continent,
    'Region': Region,
    'Site': Site,
    'City': City,
    'Building': Building,
    'CityDistrict': CityDistrict
    # 'Party': Party,
    # 'Character': Character
}


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


# Convert Object to Json/Dictionary
def obj_to_json(obj):
    return json.dumps(obj, indent=4, cls=Encoder)


# UNUSED Convert Json/Dictionary to Object
def json_to_obj(dct):
    return json.loads(dct, object_hook=custom_object_hook)


# UNUSED Serializer to create instances of classes using class_name
def class_factory(class_name, **kwargs):
    return CLASS_MAP[class_name](**kwargs)


# UNUSED Check for match between dictionary keys and class constructor. Use class_factory to construct matches
def custom_object_hook(dct):
    keys = set(dct.keys())
    for class_name, class_type in CLASS_MAP.items():
        arg_names = set(class_type.__init__.__code__.co_varnames[1:class_type.__init__.__code__.co_argcount])
        if keys == arg_names:
            return class_factory(class_name, **dct)
    return dct
