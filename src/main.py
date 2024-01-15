# DO NOT TOUCH THESE IMPORTS UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING: THE ORDER MATTERS!!!!!
from LLDM.Core.GPT import sdprompter, chat_complete_story
from LLDM.Core.Scene import Scene, Location, Character, Map, Item
from LLDM.Core.GameLogic import Battle


def init_scene():
    global scene
    scene = Scene(init_map())

    sword = Item("Sword", "A sturdy blade crafted from the finest steel.", damage=15, amount=1)
    iron_sword = Item("Iron Sword", "A rough blade crafted from sturdy iron.", damage=13, amount=1)
    potion = Item("Health Potion", "A small vial of red liquid.", healing=10, amount=1)

    scene.add_character(Character("Ray", 50, 10, 10, 2, "party", False, inventory=[sword, potion]))
    scene.add_character(Character("Dominic", 20, 10, 10, 3, "enemy", True, inventory=[iron_sword]))
    scene.add_character(Character("Richard", 20, 10, 10, 1, "enemy", True))

    return scene


def init_map():
    # TODO: Use a DungeonGenerator to pass main a fully-structured dungeon with notable locations and entrance/exit.
    room1 = Location("Room 1", "The first room of a sprawling dungeon. It has a closed door off to the side.")
    map1 = Map()
    map1.add_location(room1)
    map1.move_to(room1)
    return map1


def handle_input(user_input):
    global scene

    if user_input == "END":
        Battle._in_battle = False
        return ["Ended Battle- Returning to Story"]

    if Battle.in_battle():
        print("Battle Calls")

        # Placeholder resolution of player action
        # TODO: Build player action resolution (Refactor/Remove chat_complete_battle()

        # return handle_input_battle(user_input)
        # Battle.current_battle.next_turn(Battle.active_player)
        print(f"{Battle.active_player.name} (id:{Battle.active_player.id})" + user_input)
        Battle.current_battle.player_turn(Battle.active_player, user_input)

        # Resume the recursive roster loop
        # Battle.current_battle.next_turn(Battle.current_battle.find_next_living_character())
        return Battle.cycle_logs()
    else:
        print("Story Calls")
        response = chat_complete_story(user_input, scene)

        if response:
            scene = response.get('scene')
            # Note, this returns directly to the webapp with strings and Event objects.

            global image_path
            image_path = response.get('image')
            return scene.events


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
    # print("Stage 1: Initializing Scene")
    image_path = None
    scene = init_scene()
