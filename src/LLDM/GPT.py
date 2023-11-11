from .Objects.ObjectSerializer import obj_to_json
from .Objects.Scene import Event, Item, Location, Map
from .helpers.gpt_tools import *
from .helpers.path_config import *
from .StableDiffusion import generate

import openai
import json

openai.api_key = os.getenv("")
# Using Sam Ogden's provided API Key for LLDM
# noinspection SpellCheckingInspection
openai.api_key = os.environ['GPTAPI']
MODEL = "gpt-3.5-turbo"
MODEL_PREVIEW = "gpt-4-1106-preview"


# ================================ Functions: =======================================

# ChatCompletion Method (So IDE will stop yelling at me for duplicated code)
def chat_complete(context_file, user_input):
    print("[OPENAI]: REQUEST SENT", end=" ")
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": context_file},
            {"role": "user", "content": user_input}
        ]
    )
    print("| RESPONSE RECEIVED")
    return completion


def chat_complete_assistant(context_file, user_input, assistant_pretext):
    print("[OPENAI] API REQUEST SENT")
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": context_file},
            {"role": "assistant", "content": assistant_pretext},
            {"role": "user", "content": user_input}
        ]
    )
    return completion


def chat_complete_parallel(user_input, **kwargs):
    print("[AGENT]:", end=" ")

    # Setup return values
    game_map = kwargs.get('game_map')
    scenario = kwargs.get('scenario')
    events = []
    items = []

    # send only relevant Location objects (subset of graph) to each API prompt
    current_location = game_map.get_current_location()
    adjacent_locations = game_map.get_adjacent_to_current()

    locations = '\n'.join(str(location) for location in adjacent_locations)
    relevant_locations = f"[Map]: {locations}\nCurrent Location: [{current_location}]"
    # later, overwrite the graph entries using the list

    # Load GPT Dialogue
    messages = [{"role": "system", "content": CONTEXT_SIMPLE_EVENT}]

    # Optional: Load extra detail (from perception) into prompt
    if scenario is not None:
        messages.append({"role": "assistant", "content": str(scenario)})

    # Add game information and user input
    messages.append({"role": "user", "content": "\n Game Map: " + str(relevant_locations) + "\n User Input: " + user_input})



    # Load GPT Functions
    tools = [
        Tools.CREATE_EVENT.value
        # Tools.HANDLE_PERCEPTION.value
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

    # print(f"Inputted: {relevant_locations} \n and {user_input}")

    # Extract Data of Tools that GPT wanted to call
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

        # Execute function according to matched name
        match function_name:
            case "create_event":
                event = create_event(title, summary, category)
                events.append(event)
            case "handle_perception":
                event = create_event(title, summary, "Perception")
                # events.append(event)
                # return {'events': events, 'game_map': game_map, 'items': items}
                return event

    # Call GPT a second time. One new call per event, using different tools, and updated dialogue.
    # Load GPT Functions into prompt
    tools = [
        Tools.CREATE_ITEM.value,
        Tools.CREATE_LOCATION.value,
        Tools.HANDLE_MOVEMENT.value
    ]
    resolved_events = []
    for event in events:
        # Load GPT Dialogue into Prompt (With Specific Event Data)
        messages = [
            {"role": "system", "content": CONTEXT_SIMPLE_AGENT},
            {"role": "user", "content": "\n Game Map: " + str(relevant_locations) + "\n User Input/Event Description: " + obj_to_json(event)}
        ]

        # Force use of function based on Event category

        event_tool_name = None
        match event.category:
            case "Item Generation":
                event_tool_name = "create_item"
            case "Exploration":
                event_tool_name = "create_location"
            case "Movement":
                event_tool_name = "handle_movement"
            case "General Inquiry":
                pass

        if event_tool_name is None:
            event_tool = "auto"
        else:
            event_tool = {
                "type": "function",
                "function": {"name": event_tool_name}
            }

        # Execute OpenAI API call
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
        # print(tool_calls)

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
            # game_map retrieved from kwargs above

            # Execute function according to matched name
            match function_name:
                case "create_item":
                    item_response = create_item(name, description, damage, amount)
                    items.append(item_response[0])
                    resolved_events.append(item_response[1])
                case "create_location":
                    location_response = create_location(name, description, game_map)
                    game_map = location_response[0]
                    resolved_events.append(location_response[1])

                case "handle_movement":
                    game_map = handle_movement(moving_into, game_map)

            #
            # # Add the data of parallel function responses
            # messages.append(
            #     {
            #         "tool_call_id": tool_call.id,
            #         "role": "tool",
            #         "name": function_name,
            #         "content": function_response,
            #     }
            # )
    events.append(resolved_events)
    return {'events': events, 'game_map': game_map, 'items': items}


def chronicler(gm_entry):
    print("[CHRONICLER]:", end=" ")

    # Send GameChronicler the response, to have it create a new summary.
    completion = chat_complete(CONTEXT_CHRONICLER, gm_entry)

    # Dump Log to file
    append(PATH_LOG_CHRONICLER, str(completion))

    # Update the summary
    write(PATH_OUTPUT_CHRONICLER, str(completion.choices[0].message.content))
    # print(str(completion.choices[0].message.content))
    print(str(completion.choices[0].message.content))
    return str(completion.choices[0].message.content)


def gamemaster(user_input):
    print("[GAMEMASTER]:", end=" ")
    summarized_history = read(PATH_OUTPUT_CHRONICLER)

    # Complete the ChatCompletion
    completion = chat_complete_assistant(CONTEXT_GAMEMASTER, user_input, summarized_history)

    # Dump Log into file
    append(PATH_LOG_GAMEMASTER, str(completion))

    # Test GPT-JSON message structure
    # First, convert the message into a string, then trim the newlines.
    gpt_json = json.loads(str(completion.choices[0].message.content).replace("\n", ""))

    # Store natural-language response
    append(PATH_OUTPUT_GAMEMASTER, str(gpt_json["response"]))
    print(str(gpt_json["response"]))
    return str(gpt_json["response"])



def sdprompter():
    print("[SDPROMPTER]:", end=" ")

    # Fetch Chronicled Summary (WIP: Use JSON Location when mature)
    summary = read(PATH_OUTPUT_CHRONICLER)

    completion = chat_complete(CONTEXT_SDPROMTER, summary)

    # Dump Log into file
    append(PATH_LOG_SDPROMPTER, str(completion))

    # Currently, PATH_OUTPUT_SDPROMPTER  is commented out because I can't imagine a scenario where it'll be read

    # Forward output to prompt location for SD
    write(PATH_SDCONFIG_PROMPT, str(completion.choices[0].message.content))

    # Invoke the local SD instance to create an image based on the prompt
    print(str(completion.choices[0].message.content))
    return generate()


def process_input(user_input):
    match user_input:
        case "exit":
            raise Exception("Exited (using text)!")
        case _:
            return gamemaster(user_input)


def place_character(character_path):
    completion = chat_complete(CONTEXT_GAMESETUP, read(character_path))
    chronicler(completion.choices[0].message.content)
    return completion.choices[0].message.content


def place_player(Character):
    print("[GameSetup]:", end=" ")
    completion = chat_complete(CONTEXT_GAMESETUP, str(Character))
    chronicler(completion.choices[0].message.content)
    return str(completion.choices[0].message.content)


def print_image():
    return sdprompter()
