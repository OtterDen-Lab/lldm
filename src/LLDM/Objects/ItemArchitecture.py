from abc import ABC, abstractmethod


# Testing ground for a proper abstract factory:
# Items to be able to account for: Armor, Potions, Scrolls, Weapons,
# Categories:
# Item >
#       Equippable > Armor, Weapons,
#       Consumables > Potions, Scrolls


# Base class for all items
class Item(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def drop(self):
        print(f"You drop your {self._name}")

    @abstractmethod
    def inspect(self):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value


# Categorical abstract class
class Equippable(Item, ABC):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.is_equipped = False

    def equip(self):
        if self.is_equipped:
            print(f"{self.name} is already equipped")
        else:
            print(f"Equipped {self.name}")
            self.is_equipped = True

    @property
    def is_equipped(self):
        return self._is_equipped

    @is_equipped.setter
    def is_equipped(self, value: bool):
        self._is_equipped = value

# TODO: turn Consumable into a Factory that create Potions / Scrolls and Food/Water.
class Consumable(Item):
    def __init__(self, name: str, description: str, charges: int,):
        super().__init__(name, description)
        self.charges = charges
        self.description = description

    @abstractmethod
    def use(self):
        pass

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def charges(self):
        return self._charges

    @charges.setter
    def charges(self, value: int):
        self._charges = value


# Concrete Class
class Potion(Consumable):
    def __init__(self, name: str, description: str, charges: int = 1):
        super().__init__(name, description, charges)

    def inspect(self):
        print(f"You inspect your [{self.name}].\n[{self.name}]: {self.description} ({self.charges} Charge)")

    def use(self):
        print(f"You use your {self.name}")


# Concrete Class
class Weapon(Equippable):
    def __init__(self, name: str, damage: int, description: str):
        super().__init__(name, description)
        self.damage = damage

    def inspect(self):
        print(f"You inspect your [{self.name}] ATK:{self.damage} Desc: {self.description}")

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value: int):
        self._damage = value

    def attack(self):
        pass


potion = Potion("Mana Potion", "It will restore your mana")
potion.inspect()
potion.use()
potion.drop()

weapon = Weapon("Sword", 8, "A sharp metal blade")
weapon.inspect()
weapon.equip()
