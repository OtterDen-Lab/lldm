import json

from helpers.FileControl import *


class Character:
    def __init__(self, path_to_JSON):
        self.JSON = json.loads(read(path_to_JSON))

    def __str__(self):
        return f"{self.JSON['name']}"
        # return f"{self.JSON["name"]}, {self.char_class}, Level: {self.level}"


class CharacterAnnotations:
    # Motivations, state, etc.
    # Something that modifies the character
    pass
