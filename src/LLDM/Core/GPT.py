import os
import json
import openai
from LLDM.Core.StableDiffusion import generate, is_url_alive
from LLDM.Utility.FileControl import *  # Also imports json in path_config.py
from LLDM.Utility.ObjectSerializer import obj_to_json
from LLDM.Utility.gpt_tools import *
from LLDM.Utility.path_config import *  # Also imports os in path_config.py

# Using Sam Ogden's provided API Key for LLDM
# noinspection SpellCheckingInspection
openai.api_key = os.environ['GPTAPI']
MODEL = "gpt-3.5-turbo"
MODEL_PREVIEW = "gpt-4-1106-preview"


# ================================ Functions: =======================================
# Main Loop 2-Stage GPT Processor
def chat_complete_story(user_input: str, **kwargs):
    print("[AGENT]:", end=" ")

    # Setup return values / important things to update
    game_map = kwargs.get('game_map')
    character = kwargs.get('character')
    events = []
    image_path = None

    # send only relevant Location objects (subset of graph) to each API prompt
    current_location = game_map.get_current_location()
    adjacent_locations = game_map.get_adjacent_to_current()

    locations = '\n'.join(str(location) for location in adjacent_locations)
    relevant_locations = f"[Map]: {locations}\nCurrent Location: [{current_location}]"
    # later, overwrite the graph entries using the list

    # Load GPT Dialogue (Add game information and user input)
    messages = [{"role": "system", "content": CONTEXT_SIMPLE_EVENT},
                {"role": "user", "content":
                    f"\n Game Map: {str(relevant_locations)} "
                    f"\n Character: {character}"
                    f"\n User Input:{user_input}"
                 }]

    # Load GPT Functions
    tools = [
        Tools.CREATE_EVENT.value,
        Tools.ILLEGAL_ACTION.value
    ]

    # Execute OpenAI API call (First call, for parsing input into an Event)
    print("[OPENAI]: REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    print("| RESPONSE RECEIVED")
    # print(f"Inputted: {relevant_locations} \n and {user_input}")

    # print("\nResponse: ", response, "\n")

    # Extract Data of Tools that GPT wanted to call
    tool_calls = response.choices[0].message.tool_calls
    print(tool_calls)

    for tool_call in tool_calls:
        # Retrieve name and parameters of GPT function call
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Setup common argument aliases
        title = function_args.get('title')
        summary = function_args.get('summary')
        category = function_args.get('category')

        # Execute function according to matched name
        match function_name:
            case "create_event":
                event = create_event(title, summary, category)
                events.append(event)
            case "illegal_action":
                print("Illegal Operation - Stop trying to coerce my AI!")
                return illegal_action(title)

    # Call GPT a second time. One new call per event, using different tools, and updated dialogue.
    # Load GPT Functions into prompt
    tools = [
        Tools.CREATE_ITEM.value,
        Tools.CREATE_LOCATION.value,
        Tools.HANDLE_MOVEMENT.value,
        Tools.HANDLE_EXAMINE.value
    ]
    resolved_events = []
    for event in events:
        # Load GPT Dialogue into Prompt (With Specific Event Data)
        messages = [{"role": "system", "content": CONTEXT_SIMPLE_AGENT},
                    {"role": "user", "content":
                        f"\n Game Map: {str(relevant_locations)} "
                        f"\n Character: {character}"
                        f"\n User Input/Event Description:{obj_to_json(event)}"
                     }]

        # Force use of function based on Event category. This helps reduce GPT confusion
        event_tool_name = None
        match event.category:
            case "Item Generation":
                event_tool_name = "create_item"
            case "Exploration":
                event_tool_name = "create_location"
            case "Movement":
                event_tool_name = "handle_movement"
            case "Examine":
                event_tool_name = "handle_examine"

        if event_tool_name is None:
            event_tool = "auto"
        else:
            event_tool = {
                "type": "function",
                "function": {"name": event_tool_name}
            }

        # Execute OpenAI API call (Second call, for modifying data structures)
        print("[OPENAI]: REQUEST SENT", end=" ")
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice=event_tool
        )
        print("| RESPONSE RECEIVED")

        # print(f"Inputted: {relevant_locations} \n and {obj_to_json(event)}")

        tool_calls = response.choices[0].message.tool_calls
        print(tool_calls)

        for tool_call in tool_calls:
            # Retrieve name and parameters of GPT function call
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Setup common argument aliases
            name = function_args.get('name')
            description = function_args.get('description')
            damage = function_args.get('damage')
            amount = function_args.get('amount')
            moving_into = function_args.get('moving_into')
            # game_map retrieved from kwargs above (at start)

            # Execute function according to matched name
            match function_name:
                case "create_item":
                    item_response = create_item(name, description, damage=damage, amount=amount)
                    new_item = item_response[0]
                    character.inventory.append(new_item)
                    resolved_events.append(item_response[1])

                    # Generate Image of new item
                    image_path = sdprompter(new_item.description, title=new_item.name)

                case "create_location":
                    location_response = create_location(name, description, game_map)
                    game_map = location_response[0]
                    resolved_events.append(location_response[1])

                    # Generate Image of new current Location
                    image_path = sdprompter(game_map.get_current_location().description, title=game_map.get_current_location().name)

                case "handle_movement":
                    game_map = handle_movement(moving_into, game_map)

                case "handle_examine":
                    # Retrieve parameters for the examine function
                    examine_type = function_args.get('type')
                    obj_name = function_args.get('obj_name')
                    new_description = function_args.get('description')

                    # Call the examine function
                    updated_object = handle_examine(examine_type, obj_name, new_description, game_map=game_map,
                                                    character=character)

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
                                game_map = updated_object
                                break
                            case "Character":
                                character = updated_object
                                break
                                # # Update the character in the characters list
                                # for i, character in enumerate(characters):
                                #     if character.name == obj_name:
                                #         characters[i] = updated_object
                                #         break
                    else:
                        print(f"No updates made for {obj_name}")

    # Log the new Reaction Events created from the Event Actions
    for event in resolved_events:
        events.append(event)

    for event in events:
        # Dump Events into Log
        append(PATH_LOG_EVENTS, str(event))

    return {'events': events, 'game_map': game_map, 'character': character, 'image_path': image_path}


# TODO: Create another 2-phase input parse>process>apply using gpt_tools strictly for Battle!
def chat_complete_battle(user_input: str, **kwargs):
    print("[BATTLE AGENT]:", end = " ")

    # Some POTENTIAL kwargs / important things to update
    location = kwargs.get('location')
    turnCharacter = kwargs.get('turnCharacter')
    charactersInvolved = kwargs.get('characters')
    events = []

    # Load GPT Dialogue
    messages = [
        {"role": "system", "content": BATTLE_CONTEXT_SIMPLE_EVENT},
        {"role": "user", "content": "\n Location: " + str(location) +
                                    "\n Current Turn: " + str(turnCharacter) +
                                    "\n Party: " + str(charactersInvolved) +
                                    "\n User Input: " + user_input
         }]
    
    # Load GPT Functions
    tools = [
        Tools.CREATE_BATTLE_EVENT.value,
        Tools.ILLEGAL_ACTION.value
    ]

    # Execute OpenAI API call
    print("[OPENAI]: REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    print("| RESPONSE RECEIVED")

    # TODO: Handle the response of the first call to make Battle_Events
    tool_calls = response.choices[0].message.tool_calls
    print(tool_calls)

    for tool_call in tool_calls:
        # Retrieve name and parameters of GPT function call
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Setup common argument aliases
        title = function_args.get('title')
        summary = function_args.get('summary')
        category = function_args.get('category')

        # Execute function according to matched name
        match function_name:
            case "create_battle_event":
                event = create_event(title, summary, category)
                events.append(event)
            case "illegal_action":
                print("Illegal Operation - Stop trying to coerce my AI!")
                return illegal_action(title)

    # Call GPT a second time. One new call per event, using different tools, and updated dialogue.
    # Load GPT Functions into prompt
    tools = [
        Tools.HANDLE_ATTACK.value
    ]
    resolved_events = []
    for event in events:
        # Load GPT Dialogue into Prompt (With Specific Event Data)
        messages = [{"role": "system", "content": BATTLE_CONTEXT_SIMPLE_AGENT},
                    {"role": "user", "content":
                        f"\n Game Map: {location} "
                        f"\n Character: {turnCharacter} "
                        f"\n User Input/Event Description:{obj_to_json(event)}"
                     }]

        # Force use of function based on Event category. This helps reduce GPT confusion
        event_tool_name = None
        match event.category:
            case "Attack":
                event_tool_name = "handle_attack"

        if event_tool_name is None:
            event_tool = "auto"
        else:
            event_tool = {
                "type": "function",
                "function": {"name": event_tool_name}
            }

        # Execute OpenAI API call (Second call, for modifying data structures)
        print("[OPENAI]: REQUEST SENT", end=" ")
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice=event_tool
        )
        print("| RESPONSE RECEIVED")

        tool_calls = response.choices[0].message.tool_calls
        print(tool_calls)

        for tool_call in tool_calls:
            # Retrieve name and parameters of GPT function call
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Setup common argument aliases
            targetID = function_args.get('targetID')
            weaponName = function_args.get('weapon')
            
            target = next((info[1] for info in charactersInvolved if info[1].id == targetID), None)
            weapon = target.getItemFromInventory(weaponName)

            # Execute function according to matched name
            match function_name:
                case "handle_attack":
                    attack_info = handle_attack(turnCharacter, target, weapon)
                    turnCharacter = attack_info["attacker"]
                    target = attack_info["target"]
                    # weapon = attack_info["weapon"]

                    for info in charactersInvolved:
                        if info[1].id == turnCharacter.id:
                            info[1] = turnCharacter
                        elif info[1].id == target.id:
                            info[1] = target

                    resolved_events.append(attack_info["event"])

    # Log the new Reaction Events created from the Event Actions
    for event in resolved_events:
        events.append(event)

    for event in events:
        # Dump Events into Log
        append(PATH_LOG_EVENTS, str(event))

    return {'events': events, 'location': location, 'characters': charactersInvolved}

# Function to get an input string for NPC actions
def chat_complete_battle_AI_input(**kwargs):
    print("[BATTLE AI INPUT]:", end = " ")

    # Some POTENTIAL kwargs / important things to update
    location = kwargs.get('location')
    turnCharacter = kwargs.get('turnCharacter')
    charactersInvolved = kwargs.get('characters')

    # Load GPT Dialogue
    messages = [
        {"role": "system", "content": BATTLE_CONTEXT_AI_EVENT},
        {"role": "user", "content": "\n Location: " + str(location) +
                                    "\n Current Turn: " + str(turnCharacter) +
                                    "\n Characters Involved: " + str(charactersInvolved)
         }]
    
    # Load GPT Functions
    tools = [
        Tools.CREATE_AI_INPUT.value
    ]

    # Execute OpenAI API call
    print("[OPENAI]: REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    print("| RESPONSE RECEIVED")

    # TODO: Handle the response of the first call to make Battle_Events
    return create_ai_input(str(response.choices[0].message.content))

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
            {"role": "system", "content": CONTEXT_SDPROMPTER},
            {"role": "user", "content": subject}
        ]
    )
    print("| RESPONSE RECEIVED")

    # Dump Log into file
    append(PATH_LOG_SDPROMPTER, str(response))

    # Forward output to prompt location for SD
    write(PATH_SDCONFIG_PROMPT, str(response.choices[0].message.content))

    # Invoke the local SD instance to create an image based on the prompt
    print(str(response.choices[0].message.content))
    return generate(title=title)
