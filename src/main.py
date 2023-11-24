# DO NOT TOUCH THESE IMPORTS UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING: THE ORDER MATTERS!!!!!
from LLDM.Core.GPT import *
from LLDM.Core.Scene import Scene, Location, Character, Map


def init_map():
    # TODO: Use a DungeonGenerator to pass main a fully-structured dungeon with notable locations and entrance/exit.
    # Create the Map. Note: the technical term for our map is a 'graph'.
    room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
    # room2 = Location("Room 2", "The second room. It has a door to the first room, and another door-to an unknown area.")
    map1 = Map()
    map1.add_location(room1)
    # map1.add_location(Room2)
    # map1.connect_locations(room1, room2)

    # Set the initial location with a move_to
    map1.move_to(room1)
    return map1


def init_char():
    character = Character("player1", 100)

    sword = Item("Sword", "A sturdy blade crafted from the finest steel.", damage=100, amount=1)
    character.inventory.append(sword)
    potion = Item("Health Potion", "A small vial of red liquid.", amount=1)
    character.inventory.append(potion)

    return character


def process_input(user_input):
    global starter_map, starter_character, events, new_events, image_path
    response = chat_complete_story(user_input, game_map=starter_map, character=starter_character)

    # False indicates Illegal Operation / Failed Input
    if response:
        # Add the items to the inventory of a character in the scene
        print("")
        starter_character = response.get('character')

        # Update the Map
        print("")
        starter_map = response.get('game_map')
        print(starter_map)

        # extract the new events and append to our log
        new_events = response.get('events')
        print("")
        for event in new_events:
            events.append(event)

        # Print our Total Event Log
        print("Event History (Log)")
        for event in events:
            print(event)

        image_path = response.get('image_path')


def main_gen_img():
    return sdprompter("test for dead url", "test")


def get_img():
    global image_path
    return str(image_path)


def get_map():
    global starter_map
    return str(starter_map)


def get_character():
    global starter_character
    return str(starter_character)


def get_all_events():
    global events
    return '\n'.join(str(event) for event in events)


def get_new_events():
    global new_events
    return '\n'.join(str(event) for event in new_events)


if __name__ != '__main__':
    print("Stage 1: Initializing Scene")
    events = []
    new_events = []
    starter_map = init_map()
    starter_character = init_char()
    image_path = None

    scene = Scene(starter_map)
    scene.add_character(starter_character)
    # Scenes are built off of maps. New map? New scene. (E.g. Dungeon, City)
    # If the new scene should come with characters, generate them, and add them to the scene.
    #  (including copying existing characters from the old scene)
    print("LLDM Active!")
    print("Stage 2: ChatGPT Narration")


# This uncomment this to use main.py directly. Note: Exit command is removed for above.
# if __name__ == '__main__':
#     # Enter main loop of input>process>apply>input
#     user_input = None
#     starter_map = init_map()
#     starter_character = init_char()
#     events = []
#
#     while user_input != "exit":
#         user_input = str(input())
#         match user_input:
#             case _:
#                 # Perform the ChatCompletion with our user input
#                 response = chat_complete_story(user_input, game_map=starter_map, character=starter_character)
#
#                 # False indicates Illegal Operation / Failed Input
#                 if response is False:
#                     continue
#
#                 # If a response is received
#                 if response is not None:
#                     # Add the items to the inventory of a character in the scene
#                     print("")
#                     starter_character = response.get('character')
#
#                     # Update the Map
#                     print("")
#                     starter_map = response.get('game_map')
#                     print(starter_map)
#
#                     # extract the new events and append to our log
#                     new_events = response.get('events')
#                     print("")
#                     for event in new_events:
#                         events.append(event)
#
#                     # Print our Total Event Log
#                     print("Event History (Log)")
#                     for event in events:
#                         print(event)
#     print("Exited")




