# DO NOT TOUCH THESE IMPORTS UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING: THE ORDER MATTERS!!!!!
from LLDM.Core.GPT import *
from LLDM.Core.Scene import Scene, Location, Character, Map, Item

def init_scene():
    global scene
    scene = Scene(init_map())
    scene.add_character(init_char())

    iSword = Item("Iron Sword", "A rough blade crafted from sturdy iron.", damage=13, amount=1)
    potion = Item("Health Potion", "A small vial of red liquid.", healing=10, amount=1)
    scene.add_character(Character("Dominic", 20, 10, 10, 30, "enemy", True, inventory=[iSword]))
    scene.add_character(Character("Richard", 20, 10, 10, 30, "enemy", True))

    return scene


def init_map():
    # TODO: Use a DungeonGenerator to pass main a fully-structured dungeon with notable locations and entrance/exit.
    # Create the Map. Note: the technical term for our map is a 'graph'.
    room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
    # room2 = Location("Room 2", "The second room. It has a door to the first room, and another door-to an unknown area.")
    map1 = Map()
    map1.add_location(room1)
    # map1.add_location(room2)
    # map1.connect_locations(room1, room2)

    # Set the initial location with a move_to
    map1.move_to(room1)
    return map1


def init_char():
    character = Character("Ray", 100, 10, 10, entity="party")

    sword = Item("Sword", "A sturdy blade crafted from the finest steel.", damage=15, amount=1)
    character.inventory.append(sword)
    potion = Item("Health Potion", "A small vial of red liquid.", healing=10, amount=1)
    character.inventory.append(potion)

    return character


def process_input(user_input):
    global image_path, scene

    # Forward input to GPT, where it will be decided whether to be passed into Story or Battle
    response = chat_complete_story(user_input, scene=scene)
    if response:
        scene = response.get('scene')
        # False indicates Illegal Operation / Failed Input

        # Print the Player
        print(get_main_character())

        # Print the Map
        print(scene.loc_map)

        image_path = response.get('image_path')

def process_input_battle(user_input):
    global scene
    response = process_input_battle(user_input)
    if response:
        scene.characters = response.get('party')

def get_new_battle_events():
    return get_new_battle_events_GPT()

def main_gen_img():
    return sdprompter("test for dead url", "test")


def get_img():
    global image_path
    return str(image_path) if image_path is not None else None


def get_map():
    global scene
    return str(scene.loc_map)


def get_main_character():
    global scene
    for c in scene.characters:
        if c.entity == "party":
            return str(c)


def get_new_events():
    global scene
    return '\n'.join(str(event) for event in scene.events)


if __name__ != '__main__':
    print("Stage 1: Initializing Scene")
    image_path = None
    scene = init_scene()

    # Scenes are built off of maps. New map? New scene. (E.g. Dungeon, City)
    # If the new scene should come with characters, generate them, and add them to the scene.
    #  (including copying existing characters from the old scene)
    print("LLDM Active!")
    print("Stage 2: ChatGPT Narration")
