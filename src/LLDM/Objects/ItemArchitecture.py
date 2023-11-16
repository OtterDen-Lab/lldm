from abc import ABC, abstractmethod
from LLDM.Objects.PrettyPrinter import NestedFormatter


# TODO: Need ENUMs or other methods to ensure: Category, Weapon Type, Dice_Type, and Damage_Type are all Valid Strings

class Item(ABC, NestedFormatter):
    def __init__(self, name: str, description: str, category: str):
        self._name = name
        self._description = description
        self._category = category


class Consumable(Item):
    def __init__(self, name: str, description: str, category: str, charges: int):
        super().__init__(name, description, category)
        self._charges = charges


class Potion(Consumable):
    def __init__(self, name: str, description: str):
        super().__init__(name, description, "Consumable", 1)


class Damage(NestedFormatter):
    def __init__(self, dice_type: int, dice_count: int, damage_type: str):
        self._dice_type = dice_type
        self._dice_count = dice_count
        self._damage_type = damage_type


# Concrete Class
class Weapon(Item):
    def __init__(self, name: str, weapon_type: str, damage: Damage, description: str):
        super().__init__(name, description, "Weapon")
        self._weapon_type = weapon_type
        self._damage = damage


# health_pot = Potion("Healing Potion", "Heals you")
# print(health_pot)
#
# sword = Weapon("Sword", "Melee", Damage(8, 1, "Slashing"), "A gleaming blade")
# print(sword)
