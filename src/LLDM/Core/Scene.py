import networkx as nx

from LLDM.Utility.PrettyPrinter import NestedFormatter, PrettyPrinter
from LLDM.Core.DunGen import setup_dungeon


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
    id_counter = 1
    all_characters = {}

    def __init__(self, name: str, health: int, attack: int, defense: int, dexterity=0, entity="neutral", npc=False,
                 **kwargs):
        description = kwargs.get("description") if kwargs.get("description") is not None else ""
        inventory = kwargs.get("inventory")
        super().__init__(name, description)

        self._id = Character.id_counter
        Character.id_counter += 1
        Character.all_characters[self.id] = self

        self._name = name
        self._health = health
        self._attack = attack
        self._defense = defense
        self._dexterity = dexterity
        self._entity = entity
        self._npc = npc
        self._alive = True
        self._inventory = inventory if inventory is not None else []
        self._inventory.append(Item("Fist", "Punch enemies for a bit of damage", damage=5))

        self.is_alive = True

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value

    @property
    def attack(self):
        return self._attack

    @property
    def defense(self):
        return self._defense

    @property
    def dexterity(self):
        return self._dexterity

    @property
    def entity(self):
        return self._entity

    @property
    def npc(self):
        return self._npc

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value: bool):
        self._alive = value

    @property
    def inventory(self):
        return self._inventory

    def printInventory(self):
        inventory_str = f"{self.name} : {[item.name for item in self._inventory]}"
        print(inventory_str)

    def reset(self):
        Character.all_characters.clear()
        Character.id_counter = 1


# Item object, with keyword arguments for optional attributes.
class Item(PrettyPrinter):
    def __init__(self, name: str, description: str, **kwargs):
        super().__init__(name, description)
        if kwargs.get("damage") is not None:
            self._damage = kwargs.get("damage")
        if kwargs.get("amount") is not None:
            self._amount = kwargs.get("amount")
        if kwargs.get("healing") is not None:
            self._healing = kwargs.get("healing")

    @property
    def amount(self):
        return self._amount

    @property
    def damage(self):
        return self._damage

    @property
    def healing(self):
        return self._healing


# Map. Wrapper to manage a Graph. (Node/Graph by NetworkX)
class Map:
    def __init__(self, size: int):
        self._map = setup_dungeon(size)

    def __str__(self):
        # Create a string representation of the graph listing all nodes, connections, and attributes
        def neighbors(node: int):
            nbrs = ' '.join(str(node) for node in nx.neighbors(self._map, node))
            attrs = ' | '.join(str(value) for value in self._map.nodes[node].values())
            return f'{nbrs} | {attrs} '

        return '\n'.join(f'Node: {str(node)} -> {neighbors(node)}' for node in self._map.nodes)

    @property
    def map(self):
        return self._map

    @property
    def current_node(self):
        print(f"Current Node Called: {self._map.graph['current_node']}")
        return self._map.graph['current_node']

    @current_node.setter
    def current_node(self, new_node: int):
        # Access the Node Index, NOT the attrs
        new_num = [entry[0] for entry in self._map.nodes.data()][new_node]
        print(f'New Num: {new_num}')

        self._map.graph['current_node'] = new_num

    def get_node_num_by_name(self, name: str):
        # Search for the Location by name and return it
        for node, data in self._map.nodes.data():
            if data["name"] == name:
                return node
        return None

    def set_node_attrs(self, node_index: int, key: str, value):
        self._map.nodes[node_index][key] = value

    def move_to(self, destination: int):
        if destination in nx.neighbors(self._map, self.current_node):
            print(f'Found {destination} in neighbors. Attempting to move')
            self.current_node = destination
        else:
            print(f"Cannot move from [{self.current_node}] to [{destination}] . Node not adjacent.")

    def get_relevant_locations_str(self):
        def attrs(node: int):
            return ' | '.join(str(value) for value in self._map.nodes[node].values())

        # return str(f"[Relevant Map]: \n{neighbors(node) for node in }\nCurrent Node: [{str(self.current_node)}]")
        current = f'Node: {self.current_node} | {attrs(self.current_node)}'
        adjacent = '\n'.join(f'Node: {self.current_node} -> {str(node)} | {attrs(node)}' for node in nx.neighbors(self._map, self.current_node))
        return f'[Current Node]\n{current}\n[Relevant Map]\n{adjacent}'


# Scene represent the top level object.
# It holds the entire map/graph data, all events that have occurred, and all characters present.
class Scene(NestedFormatter):
    time = 0

    def __init__(self, loc_map, events=None, characters=None):
        self._loc_map = loc_map
        self._events = events if events is not None else []
        self._characters = characters if characters is not None else []

    def get_character_by_name(self, name: str):
        for character in self._characters:
            if character.name == name:
                return character
        return None

    @property
    def loc_map(self):
        return self._loc_map

    @loc_map.setter
    def loc_map(self, loc_map: Map):
        self._loc_map = loc_map

    @property
    def events(self):
        return self._events

    def add_event(self, event: Event):
        self._events.append(event)

    @property
    def characters(self):
        return self._characters

    def add_character(self, character: Character):
        self._characters.append(character)

    @characters.setter
    def characters(self, characters):
        self._characters = characters
