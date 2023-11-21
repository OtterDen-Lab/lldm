# DO NOT TOUCH THESE IMPORTS UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING: THE ORDER MATTERS!!!!!
from LLDM.Core.GPT import *
from LLDM.Core.Scene import Scene, Location, Character, Map



print("LLDM Active:\nType \"exit\" to stop this program.\n")

# TODO: Use a DungeonGenerator to pass main a fully-structured dungeon with notable locations and entrance/exit.
# Create the Map. Note: the technical term for our map is a 'graph'.

Room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
# Room2 = Location("Room 2", "The second room. It has a door to the first room, and another door-to an unknown area.")
map1 = Map()
map1.add_location(Room1)
# map1.add_location(Room2)
# map1.connect_locations(Room1, Room2)

# Set the initial location with a move_to
map1.move_to(Room1)
print(map1)


# Scenes are built off of maps. New map? New scene. (E.g. Dungeon, City)
# If the new scene should come with characters, generate them, and add them to the scene.
#  (including copying existing characters from the old scene)
print("Stage 1: Initializing Scene")
scene = Scene(map1)
character = Character("player1", 100)

sword = Item("Sword", "A sturdy blade crafted from the finest steel.", damage=100, amount=1)
character.inventory.append(sword)
potion = Item("Health Potion", "A small vial of red liquid.", amount=1)
character.inventory.append(potion)

scene.add_character(character)


# Enter main loop of input>process>apply>input
print("Stage 2: ChatGPT Narration")
user_input = None

events = []
scenario = None
while user_input != "exit":
    user_input = str(input())
    match user_input:
        case _:
            # Perform the ChatCompletion with our user input
            response = chat_complete_story(user_input, game_map=map1, character=character)

            # False indicates Illegal Operation / Failed Input
            if response is False:
                continue

            # If a response is received
            if response is not None:
                # Add the items to the inventory of a character in the scene
                print("")
                character = response.get('character')

                # Update the Map
                print("")
                map1 = response.get('game_map')
                print(map1)

                # extract the new events and append to our log
                new_events = response.get('events')
                print("")
                for event in new_events:
                    events.append(event)

                # Print our Total Event Log
                print("Event History (Log)")
                for event in events:
                    print(event)

print("Exited")

