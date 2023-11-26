from LLDM.Core.Scene import Location, Map

# TODO: Generate a fully-structured dungeon with notable locations and entrance/exit.
# Create the Map. Note: the technical term for our map is a 'graph'.

# Setting these up as true or false for right now, starting_room should only be set to true once, this is pretty bare bones and I'm not too sure its a good approach in the long term
class RoomFlag(Enum):
    starting_room = false
    has_chest = false
    has_npc = false

def setup_dungeon():
    # Replace the following with a randomly made graph and adjacent nodes. (or seek sizing via user input)
    # You can use random numbers for the names, and write bare-bones flags for descriptions (e.g. Has Chest, Has NPC)

    # You may create an Enum to hold the flag types if you think that would give more clarity.
    # At minimum, include a flag denoting start point, places with loot/chests, and places that will have an NPC (enemy)

    # Set this up, so we generate a dungeon with random connections
    map1 = Map()
    roooms = []

    # For right now we don't have an input, so I'm just going to set it up with 5 rooms
    for i in range(5):
        room_name = f"Room{i+1}"
        room_description = f"The {i+1} room."
        room_flags = []

        # Only do this for the first room, probably a bad idea since in the future we may want a random middle room to the be starting point
        # Also change the description to be this since it's going to be the starting point of the dungeon.
        if i == 0:
            room_flags.append(RoomFlag.starting_room)
            room_description = "The first room of a dungeon"

        # For both loot and NPC right now there will be a 20% chance for loot or an npc these are not mutually exclusive so there could be both a npc and loot
        # Also updating room_description based on if the flags are appended
        if random.random() < 0.2:
            roon_flags.append(RoomFlag.has_chest)
            room_description += "It has a chest."
        if random.random() < 0.2:
            room_flags.append(RoomFlag.has_npc)
            room_description += "It has an NPC inside"

        # Finally we create the room with the flags, I will need to add to connection flags as well
        room[i] = Location(room_name, room_description) # I'm not even sure if we need to pass the flags since they'll be in the description
        map1.add_location(room[i]) #Add to map, only issue is that it'll always add something just called room I'll have to ask about this

    # At the end we return the map1
    return map1



    # room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
    # room2 = Location("Room 2", "The second room. It has a door to the first room, and another door-to an unknown area.")
    # map1 = Map()
    # map1.add_location(room1)
    # map1.add_location(room2)
    # map1.connect_locations(room1, room2)
    #
    # return map1
