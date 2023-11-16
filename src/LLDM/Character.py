import json

from .helpers.FileControl import *


class Character:
    def __init__(self, path_to_JSON):
        self.path_to_JSON = path_to_JSON
        self.JSON = json.loads(read(path_to_JSON))

    def save_character_data(self, character):
        # Save the character's JSON data to the file
        with open(self.path_to_JSON, 'w') as json_file:
            json.dump(character.JSON, json_file, indent=4)


    def __str__(self):
        return (f"\nName: {self.JSON['name']}"
                f"\nRace: {self.JSON['race']['subtype']} {self.JSON['race']['name']}"
                f"\nClass: {self.JSON['classes'][0]['name']} ({self.JSON['classes'][0]['subtype']}) "
                f"  Level: {self.JSON['classes'][0]['level']}"
                f"\nBackground: {self.JSON['background']['name']}"
                f"\nAlignment: {self.JSON['alignment']}"
                f"\nSkills: {self.JSON['skills']}"
                f"\nDetails: {self.JSON['details']}"
                f"\nLanguages: {self.JSON['languages']}"
                f"\nWeapons: {self.JSON['weapons']}"
                f"\nSpells: {self.JSON['spells']}"
                )
        # return f"{self.JSON["name"]}, {self.char_class}, Level: {self.level}"


class CharacterAnnotations:
    # Motivations, state, etc.
    # Something that modifies the character
    def __init__(self):
        self.character_list = []
        self.size = 0
        pass

    def build_attributes(self, characters):
        pass

    def update_attributes(self, character):
        pass
