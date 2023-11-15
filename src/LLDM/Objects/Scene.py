from LLDM.Objects.PrettyPrinter import NestedFormatter
from LLDM.Objects.WorldArchitecture import BaseLocation
from json import JSONEncoder
import json


class Event:
    def __init__(self, title: str, summary: str, category: str):
        self._title = title
        self._summary = summary
        self._category = category

    def __str__(self):
        return f"[{self.category}] {self.title}: {self.summary}"

    def __repr__(self):
        return f"[{self.category}] {self.title}: {self.summary}"

    @property
    def summary(self):
        return self._summary

    @property
    def title(self):
        return self._title

    @property
    def category(self):
        return self._category


class Character(NestedFormatter):
    def __init__(self, name: str, health: int):
        self._name = name
        self._health = health


class Item(NestedFormatter):
    def __init__(self, name: str, description: str, **kwargs):
        self._name = name
        self._description = description
        if kwargs.get("damage") is not None:
            self._damage = kwargs.get("damage")
        if kwargs.get("amount") is not None:
            self._amount = kwargs.get("amount")


class Location:
    def __init__(self, name, description, adjacent=None):
        self._name = name
        self._description = description
        self.adjacent = adjacent if adjacent is not None else {}
        # Dictionary to hold adjacent locations and their respective distances

    def __str__(self):
        # Create a string with the name of the location and its connections
        adjacent_names = ', '.join(adj.name for adj in self.adjacent)
        return f"[{self.name}] | Connections: [{adjacent_names}] | {self.description}"

    def add_adjacent(self, location, distance=1):
        self.adjacent[location] = distance

    def get_adjacent_locations(self):
        return self.adjacent.keys()

    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self._name


class Map:
    def __init__(self):
        self.locations = {}  # Holds Location objects. Which have their own list of adjacent locations
        self.current_location = None  # Location object

    def __str__(self):
        # Create a string representation of the map with all locations and their connections
        locations = '\n'.join(str(location) for location in self.locations)
        return f"[Map]: Current Location: [{self.current_location.name}]\n{locations}"

    def get_current_location(self):
        return self.current_location

    def get_location_by_name(self, name: str):
        # Search for the Location by name and return it
        for location in self.locations:
            if location.name == name:
                return location
        return None

    def add_location(self, location: Location):
        self.locations[location] = location

    def connect_locations(self, loc1: Location, loc2: Location, distance=1):
        if loc1 in self.locations and loc2 in self.locations:
            if loc1 and loc2:
                loc1.add_adjacent(loc2, distance)
                loc2.add_adjacent(loc1, distance)  # For undirected graph (bidirectional paths)

    def move_to(self, location: Location):
        if self.current_location is None:
            # If there is no current location, set the initial location
            if isinstance(location, Location):
                self.current_location = location
        else:
            # If trying to move to a new location, check if it's adjacent
            if self.are_adjacent(self.current_location, location):
                self.current_location = self.locations[location]
            else:
                print(f"Cannot move to [{location.name}] from [{self.current_location.name}]. Location not adjacent.")

    def are_adjacent(self, loc1: Location, loc2: Location):
        if loc1 in self.locations and loc2 in self.locations:
            if loc1 and loc2:
                return loc2 in loc1.adjacent
        return False

    def get_adjacent_to_current(self):
        if self.current_location:
            return self.current_location.get_adjacent_locations()
        else:
            return None


class Scene(NestedFormatter):
    time = 0

    def __init__(self, loc_map: Map):
        self._loc_map = loc_map
        self._events = []
        self._characters = []

    def set_map(self, loc_map: Map):
        self._loc_map = loc_map

    def add_event(self, event: Event):
        self._events.append(event)

    def add_character(self, character: Character):
        self._characters.append(character)

# Room1 = Location("Room 1", "The first room")
# Room2 = Location("Room 2", "The second room")
# Room3 = Location("Room 3", "The third room")
#
# map1 = Map()
# map1.add_location(Room1)
# map1.add_location(Room2)
# map1.add_location(Room3)
#
# map1.connect_locations(Room1, Room2)
# map1.connect_locations(Room2, Room3)
#
# print(map1)