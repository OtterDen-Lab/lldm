from LLDM.Core.GPT import sdprompter, chat_complete_story
from LLDM.Core.Scene import Scene, Map
from LLDM.Core.GameLogic import Battle


def init_scene():
    global scene
    scene = Scene(Map(5))
    return scene


def handle_input(user_input):
    """
    Initial processor of user input (after being sent from the WebApp)
    :param user_input: raw user input
    :return: the Events to be displayed on the WebApp
    """
    global scene

    if user_input == "END":
        Battle._in_battle = False
        return ["Ended Battle- Returning to Story"]

    if Battle.in_battle():
        print("Battle Calls")

        print(f"{Battle.active_player.name} (id:{Battle.active_player.id})" + user_input)
        Battle.current_battle.player_turn(Battle.active_player, user_input)

        # Resume the recursive roster loop
        return Battle.cycle_logs()
    else:
        print("Story Calls")
        response = chat_complete_story(user_input, scene)

        if response:
            scene = response.get('scene')

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
    return f'Current Node: {scene.loc_map.current_node}\n{scene.loc_map}'


def get_main_character():
    global scene
    for c in scene.loc_map.get_current_characters():
        if c.entity == "party":
            return str(c)


def get_new_events():
    global scene
    return '\n'.join(str(event) for event in scene.events)


if __name__ != '__main__':
    image_path = None
    scene = init_scene()
