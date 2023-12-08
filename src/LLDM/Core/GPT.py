﻿import os
import json
import openai

from LLDM.Core.Scene import Scene
from LLDM.Core.StableDiffusion import generate, is_url_alive
from LLDM.Utility.FileControl import *  # Also imports json in path_config.py
from LLDM.Utility.ObjectSerializer import obj_to_json
from LLDM.Utility.gpt_tools import Tools, create_event, illegal_action, create_item, handle_examine, handle_movement, create_location, handle_attack, handle_wait, handle_item, create_ai_input, handle_battle
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
    scene = kwargs.get('scene')

    character = None
    for c in scene.characters:
        if c.entity == "party":
            character = c
            break

    events = []
    image_path = None

    # send only relevant Location objects (subset of graph) to each API prompt
    adjacent_locations = scene.loc_map.get_adjacent_to_current()

    locations = '\n'.join(str(location) for location in adjacent_locations)
    relevant_locations = f"[Map]: {locations}\nCurrent Location: [{scene.loc_map.current_location}]"
    # later, overwrite the graph entries using the list

    # Load GPT Dialogue (Add game information and user input)
    messages = [{"role": "system", "content": CONTEXT_SIMPLE_EVENT},
                {"role": "user", "content":
                    f"\n Game Map: {str(relevant_locations)} "
                    f"\n Characters: {scene.characters}"
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
        Tools.HANDLE_EXAMINE.value,
        Tools.HANDLE_BATTLE.value
    ]
    resolved_events = []
    for event in events:
        # Load GPT Dialogue into Prompt (With Specific Event Data)
        messages = [{"role": "system", "content": CONTEXT_SIMPLE_AGENT},
                    {"role": "user", "content":
                        f"\n Game Map: {str(relevant_locations)} "
                        f"\n Characters: {scene.characters}"
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
            case "Battle":
                event_tool_name = "handle_battle"

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
                    location_response = create_location(name, description, scene.loc_map)
                    scene.loc_map = location_response[0]
                    resolved_events.append(location_response[1])

                    # Generate Image of new current Location
                    image_path = sdprompter(scene.loc_map.current_location.description, title=scene.loc_map.current_location.name)

                case "handle_movement":
                    scene.loc_map = handle_movement(moving_into, scene.loc_map)

                case "handle_examine":
                    # Retrieve parameters for the examine function
                    examine_type = function_args.get('type')
                    obj_name = function_args.get('obj_name')
                    obj_owner_name = function_args.get('obj_owner_name')
                    new_description = function_args.get('description')

                    # Call the examine function
                    updated_object = handle_examine(examine_type, obj_name, new_description, scene=scene, obj_owner_name=obj_owner_name)

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
                case "handle_battle":
                    response = handle_battle(scene)

    # Log the new Reaction Events created from the Event Actions
    for event in resolved_events:
        events.append(event)

    # A bit confusing, but going into this section, 'events' is the array of all newly generated events.
    # a copy of 'events' is sent to 'new_events', and scene's events are merged with 'events'.
    # new_events = events
    # for event in scene.events:
    #     events.append(event)
    #     # Dump Events into Log
    #     append(PATH_LOG_EVENTS, str(event))

    scene = Scene(scene.loc_map, events, scene.characters)
    return {'scene': scene, 'image_path': image_path}








# TODO: Create another 2-phase input parse>process>apply using gpt_tools strictly for Battle!
def chat_complete_battle(user_input: str, **kwargs):
    print("\n[BATTLE AGENT]:", end = " ")

    # Some POTENTIAL kwargs / important things to update
    location = kwargs.get('location')
    turnCharacter = kwargs.get('turnCharacter')
    charactersInvolved = kwargs.get('charactersInfo')
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

    # print(response)

    # TODO: Handle the response of the first call to make Battle_Events
    tool_calls = response.choices[0].message.tool_calls
    # print(tool_calls)

    for tool_call in tool_calls:
        # Retrieve name and parameters of GPT function call
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Setup common argument aliases
        title = function_args.get('title')
        summary = function_args.get('summary')
        category = function_args.get('category')
        # print(f"{title} || {summary} || {category}")

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
        Tools.HANDLE_ATTACK.value,
        Tools.HANDLE_WAIT.value,
        Tools.HANDLE_ITEM.value
    ]
    resolved_events = []
    for event in events:
        print(obj_to_json(event))
        # Load GPT Dialogue into Prompt (With Specific Event Data)
        messages = [{"role": "system", "content": BATTLE_CONTEXT_SIMPLE_AGENT},
                    {"role": "user", "content":
                        f"\n Game Map: {location} "
                        f"\n Character: {turnCharacter} "
                        f"\n Characters Involved: {charactersInvolved}"
                        f"\n User Input/Event Description:{obj_to_json(event)}"
                     }]

        # Force use of function based on Event category. This helps reduce GPT confusion
        event_tool_name = None
        match event.category:
            case "Attack":
                event_tool_name = "handle_attack"
            case "Wait":
                event_tool_name = "handle_wait"
            case "Item":
                event_tool_name = "handle_item"

        if event_tool_name is None:
            event_tool = "auto"
        else:
            event_tool = {
                "type": "function",
                "function": {"name": event_tool_name}
            }

        # Execute OpenAI API call (Second call, for modifying data structures)
        print("\n[OPENAI]: REQUEST SENT", end=" ")
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice=event_tool
        )
        print("| RESPONSE RECEIVED")

        tool_calls = response.choices[0].message.tool_calls
        # print(tool_calls)

        for tool_call in tool_calls:
            # Retrieve name and parameters of GPT function call
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Setup common argument aliases
            targetID = function_args.get('targetID')

            # Execute function according to matched name
            match function_name:
                case "handle_attack":
                    weaponName = function_args.get('weapon')
                    # print(f"Found Target: {targetID} | Found Weapon : {weaponName}")

                    target = next((info[1] for info in charactersInvolved if info[1].id == targetID), None)
                    if target is None:
                        print(f"[ERROR MESSAGE]: targetID {targetID} NOT FOUND,", end = " ")
                        target = next((info[1] for info in charactersInvolved if info[1].entity != turnCharacter.entity), None)
                        print(f"DEFAULTING TO {target.name}")

                    weapon = turnCharacter.getItemFromInventory(weaponName)
                    if weapon is None:
                        print(f"[ERROR MESSAGE]: weapon {weaponName} NOT FOUND,", end=" ")
                        weapon = turnCharacter.inventory[0]
                        print(f"DEFAULTING TO FIRST ITEM IN INVENTORY:  {weapon.name}")

                    attack_info = handle_attack(turnCharacter, target, weapon)
                    turnCharacter = attack_info["attacker"]
                    target = attack_info["target"]
                    # weapon = attack_info["weapon"]

                    for info in charactersInvolved:
                        if info[1].id == turnCharacter.id:
                            info = info[0], turnCharacter
                        elif info[1].id == target.id:
                            info = info[0], target

                    resolved_events.append(attack_info["event"])
                
                case "handle_wait":
                    summary = function_args.get('summary')
                    wait_info = handle_wait(turnCharacter, summary)
                    resolved_events.append(wait_info["event"])
                case "handle_item":
                    itemName = function_args.get('item')
                    target = next((info[1] for info in charactersInvolved if info[1].id == targetID), None)
                    if target is None:
                        print(f"[ERROR MESSAGE]: targetID {targetID} NOT FOUND,", end=" ")
                        target = next((info[1] for info in charactersInvolved if info[1].entity == turnCharacter.entity), None)
                        print(f"DEFAULTING TO {target.name}")

                    item = turnCharacter.getItemFromInventory(itemName)
                    if item is None:
                        print(f"[ERROR MESSAGE]: item {itemName} NOT FOUND,", end=" ")
                        print(f"SKIPPING ITEM ACTION")
                    else:
                        item_info = handle_item(turnCharacter, target, item)
                        turnCharacter = item_info["user"]
                        target = item_info["target"]

                        for info in charactersInvolved:
                            if info[1].id == turnCharacter.id:
                                info = info[0], turnCharacter
                            elif info[1].id == target.id:
                                info = info[0], target

                        resolved_events.append(item_info["event"])


    # Log the new Reaction Events created from the Event Actions
    for event in resolved_events:
        events.append(event)

    for event in events:
        # Dump Events into Log
        append(PATH_LOG_EVENTS, str(event))

    return {'events': events, 'location': location, 'characters': charactersInvolved}




# Function to get an input string for NPC actions
def chat_complete_battle_AI_input(**kwargs):
    print("\n[BATTLE AI INPUT]:", end = " ")

    # Some POTENTIAL kwargs / important things to update
    location = kwargs.get('location')
    turnCharacter = kwargs.get('turnCharacter')
    charactersInvolved = kwargs.get('charactersInfo')
    randomActionNum = kwargs.get('randomAction')

    # Load GPT Dialogue
    messages = [
        {"role": "system", "content": BATTLE_CONTEXT_AI_EVENT},
        {"role": "user", "content": "\n Location: " + str(location) +
                                    "\n Current Turn: " + str(turnCharacter) +
                                    "\n Characters Involved: " + str(charactersInvolved) +
                                    "\n Action Number: " + str(randomActionNum)
         }]
    
    # Load GPT Functions
    tools = [
        Tools.CREATE_AI_INPUT.value
    ]
    tool_create_ai_input = {
        "type": "function",
        "function": {"name": "create_ai_input"}
    }
    # Execute OpenAI API call
    print("[OPENAI]: REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice=tool_create_ai_input
    )
    print("| RESPONSE RECEIVED")

    # TODO: Handle the response of the first call to make Battle_Events
    input_string = ""
    tool_calls = response.choices[0].message.tool_calls
    for tool_call in tool_calls:
        function_args = json.loads(tool_call.function.arguments)
        input_string += function_args.get('input_string')

    return create_ai_input(input_string)

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


