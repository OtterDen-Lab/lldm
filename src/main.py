from LLDM.Core.GPT import chat_complete_story
from LLDM.Core.Scene import Scene, Map
from LLDM.Core.GameLogic import Battle


class Campaign:
    scene = None
    image_path = None

    @classmethod
    def init_scene(cls):
        cls.scene = Scene(Map(5))

    @classmethod
    def get_img(cls):
        return str(cls.image_path) if cls.image_path is not None else None

    @classmethod
    def get_map(cls):
        return f'Current Node: {cls.scene.loc_map.current_node}\n{cls.scene.loc_map}'

    @classmethod
    def get_main_character(cls):
        for c in cls.scene.loc_map.get_current_characters():
            if c.entity == "party":
                return str(c)

    @classmethod
    def get_new_events(cls):
        return '\n'.join(str(event) for event in cls.scene.events)

    @classmethod
    def handle_input(cls, user_input):
        """
        Initial processor of user input (after being sent from the WebApp)
        :param user_input: raw user input
        :return: the Events to be displayed on the WebApp
        """

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
            response = chat_complete_story(user_input, cls.scene)

            if response:
                cls.scene = response.get('scene')

                cls.image_path = response.get('image')
                return cls.scene.events


if __name__ != '__main__':
    Campaign.init_scene()
