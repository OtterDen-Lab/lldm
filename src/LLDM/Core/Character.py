from LLDM.Core.Item import Item
from LLDM.Utility import PrettyPrinter


class Character(PrettyPrinter):
    """Simplified Character object, with useful attrs"""
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
