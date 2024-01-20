from LLDM.Utility import PrettyPrinter


class Item(PrettyPrinter):
    """
    Item object, with keyword arguments for optional attributes.
    """
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
