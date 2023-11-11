# DO NOT TOUCH THESE IMPORTS UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING: THE ORDER MATTERS!!!!!
from LLDM.GPT       import *
from LLDM.Objects.Scene import Scene, Location, Character, Map

# Example Usage:
# world = World("FantasyLand", "A magical realm of adventures.")
# party = [Character("Alice", "Wizard", 5), Character("Bob", "Warrior", 6)]
# quests = [Quest("Find the magic stone"), Quest("Defeat the dragon", "In Progress")]
# campaign = Campaign(world, party, quests)
# print(campaign)
print("LLDM Active:\nType \"exit\" to stop this program.\n")

# Flow:
# Player Input is resolved to an Event then the action is applied. Like, [Open Door]>Location Gen, [Open Chest]>Item Gen

# If Location Gen, new Location and Scene
# If the new scene should come with characters, generate them here, and them to the scene.
#  (including moving existing characters from the old scene)

# If Item Gen, new items
# Use GPT-Function calling logic to determine what type of item was generated, and what attributes it should have.
# Heavy use of optional parameters in gpt-logic and python class attributes should reduce complexity scaling
print("Stage 1: Initializing Scene")
Room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
# Room2 = Location("Room 2", "The second room. It has a door to the first room, and another door-to an unknown area.")

map1 = Map()
map1.add_location(Room1)
# map1.add_location(Room2)

# map1.connect_locations(Room1, Room2)


# Set the initial location
map1.move_to(Room1)
print(map1)

scene = Scene(map1)
character = Character("player1", 100)
scene.add_character(character)

print("Stage 2: ChatGPT Narration")
user_input = str(input())

events = []
inventory = []
scenario = None
while user_input != "exit":
    match user_input:
        case _:
            response = chat_complete_parallel(user_input, game_map=map1, scenario=scenario)

            if isinstance(response, Event):
                # Short-Circuit via Perception.
                events.append(response)
                scenario = response
                print(f"[{scenario.category}] [{scenario.title}] {scenario.summary}")

            elif response is not None:
                new_events = response.get('events')
                print("")
                events.append(new_events)
                for event in events:
                    print(str(event) + "\n")
                    # print(f"[{event.category}] [{event.title}] {event.summary} ")
                inventory.append(response.get('items'))

                # update map
                map1 = response.get('game_map')

            print("")
            print(map1)

    user_input = str(input())

print("Exited")

