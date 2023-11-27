from LLDM.Utility.PrettyPrinter import NestedFormatter, PrettyPrinter


# Events are the descriptions of actions or reactions created through play.
# User inputs are processed by GPT into action Events, then resolved by GPT again to produce reaction Events
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


# Simplified Character object.
# TODO: Optional: Add parameters
class Character(PrettyPrinter):
    def __init__(self, name: str, health: int, **kwargs):
        description = kwargs.get("description")
        inventory = kwargs.get("inventory")
        super().__init__(name, description)

        self._name = name
        self._health = health
        self._inventory = inventory if inventory is not None else []

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @property
    def inventory(self):
        return self._inventory


# Item object, with keyword arguments for optional attributes.
class Item(PrettyPrinter):
    def __init__(self, name: str, description: str, **kwargs):
        super().__init__(name, description)
        if kwargs.get("damage") is not None:
            self._damage = kwargs.get("damage")
        if kwargs.get("amount") is not None:
            self._amount = kwargs.get("amount")

    @property
    def amount(self):
        return self._amount

    @property
    def damage(self):
        return self._damage


# Node of a graph with bidirectional connections. Each connection has a distance (currently unused)
class Location(PrettyPrinter):
    def __init__(self, name: str, description: str, adjacent=None):
        super().__init__(name, description)

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


# Map. Holds Locations as in a node-based graph structure
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

    def add_location(self, new_location: Location):
        self.locations[new_location] = new_location

    def connect_locations(self, loc1: Location, loc2: Location, distance=1):
        if loc1 in self.locations and loc2 in self.locations:
            if loc1 and loc2:
                loc1.add_adjacent(loc2, distance)
                loc2.add_adjacent(loc1, distance)  # For undirected graph (bidirectional paths)

    def move_to(self, destination: Location):
        if self.current_location is None:
            # If there is no current location, set the initial location
            if isinstance(destination, Location):
                self.current_location = destination
        else:
            # If trying to move to a new location, check if it's adjacent
            if self.are_adjacent(self.current_location, destination):
                self.current_location = self.locations[destination]
            else:
                print(f"Cannot move to [{destination.name}] from [{self.current_location.name}]. Location not adjacent.")

    def are_adjacent(self, loc1: Location, loc2: Location):
        if loc1 in self.locations and loc2 in self.locations:
            if loc1 and loc2:
                return loc2 in loc1.adjacent  # FOR USE ONLY IN FULLY BIDIRECTIONAL GRAPHS. Edit for directed graphs.
        return False

    def get_adjacent_to_current(self):
        if self.current_location:
            return self.current_location.get_adjacent_locations()
        else:
            return None


# Scene represent the top level object.
# It holds the entire map/graph data, all events that have occurred, and all characters present.
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

    def get_character_by_name(self, name: str):
        for character in self._characters:
            if character.name == name:
                return character
        return None
