# This class in inherited by most Deprecated, and handles their returns/to_strings and setters for name/descriptions


class PrettyPrinter(object):
    """
    Inheritable Class to add name, description, and custom to-str/return
    """
    def __init__(self, name: str = None, description: str = None):
        if name is not None:
            self._name = name
        if description is not None:
            self._description = description

    def __str__(self):
        lines = [self.__class__.__name__ + ':']
        for key, val in vars(self).items():
            lines += '{}: {}'.format(key, val).split('\n')
        return '\n    '.join(lines)

    def __repr__(self):
        lines = ['']
        for key, val in vars(self).items():
            lines += '{}: {}'.format(key, val).split('\n')
        return '\n    '.join(lines)

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


class NestedFormatter(object):
    """
    PrettyPrinter, only the custom to-str/repr and no inherited variables
    """
    def __str__(self):
        lines = [self.__class__.__name__ + ':']
        for key, val in vars(self).items():
            lines += '{}: {}'.format(key, val).split('\n')
        return '\n    '.join(lines)

    def __repr__(self):
        lines = ['']
        for key, val in vars(self).items():
            lines += '{}: {}'.format(key, val).split('\n')
        return '\n    '.join(lines)
