from LLDM.Core.Scene import Location, Map

# TODO: Generate a fully-structured dungeon with notable locations and entrance/exit.
# Create the Map. Note: the technical term for our map is a 'graph'.


def setup_dungeon():
    # Replace the following with a randomly made graph and adjacent nodes. (or seek sizing via user input)
    # You can use random numbers for the names, and write bare-bones flags for descriptions (e.g. Has Chest, Has NPC)

    # You may create an Enum to hold the flag types if you think that would give more clarity.
    # At minimum, include a flag denoting start point, places with loot/chests, and places that will have an NPC (enemy)

    room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
    room2 = Location("Room 2", "The second room. It has a door to the first room, and another door-to an unknown area.")
    map1 = Map()
    map1.add_location(room1)
    map1.add_location(room2)
    map1.connect_locations(room1, room2)

    return map1
