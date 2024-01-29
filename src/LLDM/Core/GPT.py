import json

# from LLDM.Core.Scene import Scene
# from LLDM.Core.StableDiffusion import generate, is_url_alive
# from LLDM.Utility.FileControl import *  # Also imports json in path_config.py
# from LLDM.Utility.ObjectSerializer import obj_to_json
# from LLDM.Utility.gpt_tools import *
# from LLDM.Utility.path_config import *  # Also imports os in path_config.py

from .GameLogic import Battle
from .Scene import Scene
from LLDM.Utility import write, append, obj_to_json, Routes
from .StableDiffusion import generate, is_url_alive
from .gpt_tools import *


# ================================ Functions: =======================================
def chat_complete_story(user_input: str, scene: Scene):
    """
    # Two-Stage GPT Processor
    :param user_input: input from the user/webapp
    :param scene: the current Scene
    :return: the results of the second call, which is a Scene and an image
    """
    # send only relevant Location objects (subset of graph) to each API prompt
    relevant_locations = scene.loc_map.get_relevant_locations_str()

    # Create an Event (Does not mutate data/information)
    event = first_call(user_input, relevant_locations, scene.loc_map.get_current_characters())

    # Resolve Event (Updates data/information) or return False
    return second_call(event, scene, relevant_locations) if event else None


# First Call - Returns an Event object
def first_call(user_input: str, str_locations: str, characters):
    """

    :param user_input: input from the user/webapp passed into the calling function
    :param str_locations: data of relevant locations (Current & Adjacent Nodes)
    :param characters: characters within the current Node
    :return: an Event object constructed to hold an action processed from player input
    """
    print("[AGENT]:", end=" ")

    # Load GPT Dialogue (Add game information and user input)
    messages = [{"role": "system", "content": Routes.CONTEXT_SIMPLE_EVENT},
                {"role": "user", "content":
                    f"\n Game Map: {str_locations} "
                    f"\n Characters: {characters}"
                    f"\n User Input:{user_input}"
                 }]

    # Load GPT Functions
    tools = [
        Tools.CREATE_EVENT.value,
        Tools.ILLEGAL_ACTION.value
    ]

    # Execute OpenAI API call & retrieve name and parameters of GPT function call
    tool_data = get_response_tool(messages, tools)
    function_args = tool_data.get('args')

    # Setup common argument aliases
    title = function_args.get('title')
    summary = function_args.get('summary')
    category = function_args.get('category')

    # Execute function according to matched name
    match tool_data.get('name'):
        case "illegal_action":
            print("Illegal Operation - Stop trying to coerce my AI!")
            return illegal_action(title)
        case "create_event":
            return create_event(title, summary, category)


def second_call(event: Event, scene: Scene, str_locations: str):
    """
    :param event: the Event created from the first call
    :param scene: the current Scene object
    :param str_locations: data of relevant locations (Current & Adjacent Nodes)
    :return: a new Scene (to update/replace the current) and image
    """
    # Second Call
    image = None
    character = None
    for c in scene.loc_map.get_current_characters():
        if c.entity == "party":
            character = c
            break

    # Call GPT a second time. One new call per event, using different tools, and updated dialogue.
    # Load GPT Functions into prompt
    tools = [
        Tools.CREATE_ITEM.value,
        Tools.HANDLE_MOVEMENT.value,
        Tools.HANDLE_EXAMINE.value,
        Tools.HANDLE_BATTLE.value
    ]
    resolved_events = []
    # Load GPT Dialogue into Prompt (With Specific Event Data)
    messages = [{"role": "system", "content": Routes.CONTEXT_SIMPLE_AGENT},
                {"role": "user", "content":
                    f"\n Game Map: {str_locations} "
                    f"\n Characters: {scene.loc_map.get_current_characters()}"
                    f"\n User Input/Event Description:{obj_to_json(event)}"
                 }]

    # Execute OpenAI API call & retrieve name and parameters of GPT function call
    tool_data = get_response_tool(messages, tools, event.category)

    # Retrieve name and parameters of GPT function call
    function_args = tool_data.get('args')

    # Setup common argument aliases
    name = function_args.get('name')
    description = function_args.get('description')
    damage = function_args.get('damage')
    amount = function_args.get('amount')
    target_index = function_args.get('target_index')

    # Execute function according to matched name
    match tool_data.get('name'):
        case "create_item":
            item_response = create_item(name, description, damage=damage, amount=amount)
            new_item = item_response[0]
            character.inventory.append(new_item)
            resolved_events.append(item_response[1])

            # Generate Image of new item
            image = sdprompter(new_item.description, new_item.name)

        case "handle_movement":
            movement_response = handle_movement(target_index, scene.loc_map)
            scene.loc_map = movement_response.get('game_map')

            name, description = scene.loc_map.get_node_attrs(scene.loc_map.current_node)
            event.title = f"Moving into {name}"
            event.summary = description
            resolved_events.append(event)

            # Generate Image of location (if new location)
            if movement_response.get('img_gen'):
                print("Requesting Image Generation")
                name, desc = scene.loc_map.get_node_attrs(scene.loc_map.current_node)
                image = sdprompter(desc, name)

        case "handle_examine":
            # Retrieve parameters for the examine function
            examine_type = function_args.get('type')
            obj_name = function_args.get('obj_name')
            obj_owner_name = function_args.get('obj_owner_name')
            new_description = function_args.get('description')

            # Call the examine function
            updated_object = handle_examine(examine_type, obj_name, new_description, scene=scene,
                                            obj_owner_name=obj_owner_name)

            # Update the game state based on the type of object examined
            if updated_object:
                match examine_type:
                    case "Item":
                        # Update the item in character's inventory
                        for i, item in enumerate(character.inventory):
                            if item.name == obj_name:
                                character.inventory[i] = updated_object
                                break
                    case "Location":
                        # Update the game map
                        scene.loc_map = updated_object

                    case "Character":
                        character = updated_object
                        # # Update the character in the characters list
                        # for i, character in enumerate(characters):
                        #     if character.name == obj_name:
                        #         characters[i] = updated_object
                        #         break
            else:
                print(f"No updates made for {obj_name}")

        case "handle_battle":
            print("Entering Battle Recursion")
            for battle_event in Battle.start_battle(scene):
                print(battle_event)
                resolved_events.append(battle_event)
            print("Exited Battle Recursion")

    return {'scene': Scene(scene.loc_map, resolved_events), 'image': image}


def sdprompter(subject: str, title: str = None):
    """
    Function to generate images and perform file I/O to log and save them.
    :param subject: input text / image prompt
    :param title: optional title (for the filename)
    :return: a filepath to the image
    """
    # Check if SD service is alive (Don't waste a GPT call if sdprompt is dead)
    if not is_url_alive():
        return title

    # Execute OpenAI API call
    print("[SDPROMPTER]: OPENAI REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": Routes.CONTEXT_SDPROMPTER},
            {"role": "user", "content": subject}
        ]
    )
    print("| RESPONSE RECEIVED")

    # Dump Log into file
    append(Routes.PATH_LOG_SDPROMPTER, str(response))

    # Generate an image using the generated prompt
    prompt = str(response.choices[0].message.content)
    print(prompt)
    return generate(prompt, title)
