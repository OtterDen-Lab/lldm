# This class in inherited by most Objects, and handles their returns/to_strings and setters for name/descriptions
class PrettyPrinter(object):
    def __init__(self):
        self.name = None
        self.description = None

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

    def set_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Expected a string for name.")
        self.name = value

    def set_description(self, value):
        if not isinstance(value, str):
            raise ValueError("Expected a string for description.")
        self.description = value


class NestedFormatter(object):
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
