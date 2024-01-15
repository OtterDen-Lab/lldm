import openai
import os
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

# Using Sam Ogden's provided API Key for LLDM
# noinspection SpellCheckingInspection
openai.api_key = os.environ['GPTAPI']
MODEL = "gpt-3.5-turbo"
MODEL_PREVIEW = "gpt-4-1106-preview"


# ================================ Functions: =======================================
# Main Loop 2-Stage GPT Processor
def chat_complete_story(user_input: str, scene: Scene):
    # send only relevant Location objects (subset of graph) to each API prompt
    relevant_locations = scene.loc_map.get_relevant_locations_str()

    # Create an Event (Does not mutate data/information)
    event = first_call(user_input, relevant_locations, scene.characters)

    # Resolve Event (Updates data/information) or return False
    return second_call(event, scene, relevant_locations) if event else None


# First Call - Returns an Event object
def first_call(user_input: str, str_locations: str, characters):
    print("[AGENT]:", end=" ")

    # later, overwrite the graph entries using the list

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
    # Second Call
    image = None
    character = None
    for c in scene.characters:
        if c.entity == "party":
            character = c
            break

    # Call GPT a second time. One new call per event, using different tools, and updated dialogue.
    # Load GPT Functions into prompt
    tools = [
        Tools.CREATE_ITEM.value,
        Tools.CREATE_LOCATION.value,
        Tools.HANDLE_MOVEMENT.value,
        Tools.HANDLE_EXAMINE.value,
        Tools.HANDLE_BATTLE.value
    ]
    resolved_events = []
    # Load GPT Dialogue into Prompt (With Specific Event Data)
    messages = [{"role": "system", "content": Routes.CONTEXT_SIMPLE_AGENT},
                {"role": "user", "content":
                    f"\n Game Map: {str_locations} "
                    f"\n Characters: {scene.characters}"
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
    moving_into = function_args.get('moving_into')

    # Execute function according to matched name
    match tool_data.get('name'):
        case "create_item":
            item_response = create_item(name, description, damage=damage, amount=amount)
            new_item = item_response[0]
            character.inventory.append(new_item)
            resolved_events.append(item_response[1])

            # Generate Image of new item
            image = sdprompter(new_item.description, title=new_item.name)

        case "create_location":
            location_response = create_location(name, description, scene.loc_map)
            scene.loc_map = location_response[0]
            resolved_events.append(location_response[1])

            # Generate Image of new current Location
            image = sdprompter(scene.loc_map.current_location.description,
                               title=scene.loc_map.current_location.name)

        case "handle_movement":
            scene.loc_map = handle_movement(moving_into, scene.loc_map)

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

    return {'scene': Scene(scene.loc_map, resolved_events, scene.characters), 'image': image}


# Helper functions to force use of function based on Event category.
def tool_for(category=None):
    event_tool_map = {
        "Exploration": "create_location",
        "Item Generation": "create_item",
        "Movement": "handle_movement",
        "Examine": "handle_examine",
        "Battle": "handle_battle"
    }

    # Selecting the appropriate tool based on the event category
    event_tool_name = event_tool_map.get(category)

    # Constructing the tool dictionary
    return {"type": "function", "function": {"name": event_tool_name}} if event_tool_name else "auto"


def get_response_tool(messages, tools, category=None):
    # Execute OpenAI API call
    print("\n[OPENAI]: REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice=tool_for(category)
    )
    print("| RESPONSE RECEIVED")

    # Retrieve name and parameters of GPT function call
    tool_call = response.choices[0].message.tool_calls[0]
    return {"name": tool_call.function.name, "args": json.loads(tool_call.function.arguments)}


# Function to generate images, using an input text and an optional title (for the filename)
def sdprompter(subject: str, title: str = None):
    # Check if SD service is alive (Don't waste a GPT call if sdprompt is dead)
    if not is_url_alive():
        return title

    print("[SDPROMPTER]:", end=" ")
    # Execute OpenAI API call
    print("[OPENAI]: REQUEST SENT", end=" ")
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

    # Forward output to prompt location for SD
    write(Routes.PATH_SDCONFIG_PROMPT, str(response.choices[0].message.content))

    # Invoke the local SD instance to create an image based on the prompt
    print(str(response.choices[0].message.content))
    return generate(title=title)
