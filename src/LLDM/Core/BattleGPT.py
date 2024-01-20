import openai
import os
import json

from LLDM.Utility import append, obj_to_json, Routes
from .gpt_tools import *

# Using Sam Ogden's provided API Key for LLDM
# noinspection SpellCheckingInspection
openai.api_key = os.environ['GPTAPI']
MODEL = "gpt-3.5-turbo"
MODEL_PREVIEW = "gpt-4-1106-preview"


# Function to get an input string for NPC actions
def chat_complete_battle_AI_input(**kwargs):
    print("\n[BATTLE AI INPUT]:", end=" ")
    self = kwargs.get('self')
    targets = kwargs.get('targets')
    action = kwargs.get('action')

    # Load GPT Dialogue
    messages = [
        {"role": "system", "content": Routes.BATTLE_CONTEXT_AI_EVENT},
        {"role": "user", "content": "\n You: " + str(self) +
                                    "\n Targets: " + str(targets) +
                                    "\n Action: " + str(action)
         }]

    # Load GPT Functions
    tools = [
        Tools.CREATE_AI_INPUT.value
    ]

    # Execute the OpenAI Call and store the tools used
    tool_data = get_response_tool(messages, tools, "AI")
    function_args = tool_data.get('args')

    # Handle the response of the first call to make Battle_Events
    title = function_args.get('title')
    summary = function_args.get('summary')
    category = function_args.get('category')

    return create_ai_input(title, summary, category)


def chat_complete_battle_player_input(user_input: str, **kwargs):
    # kwargs contains relevant information
    self = kwargs.get('self')
    targets = kwargs.get('targets')

    # Load GPT Dialogue
    messages = [
        {"role": "system", "content": Routes.BATTLE_CONTEXT_SIMPLE_EVENT},
        {"role": "user", "content": "\n Self: " + str(self) +
                                    "\n Targets: " + str(targets) +
                                    "\n User Input: " + str(user_input)
         }]

    # Load GPT Functions
    tools = [
        Tools.CREATE_BATTLE_EVENT.value,
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
        case "create_battle_event":
            return create_event(title, summary, category)
        case "illegal_action":
            print("Illegal Operation - Stop trying to coerce my AI!")
            return illegal_action(title)


def chat_complete_battle_resolve(event: Event, **kwargs):
    self = kwargs.get('self')
    targets = kwargs.get('targets')
    str_targets = '\n'.join(str(target) for target in targets)

    tools = [
        Tools.HANDLE_ATTACK.value,
        Tools.HANDLE_WAIT.value,
        Tools.HANDLE_ITEM.value
    ]
    resolved_events = [event]

    # Load GPT Dialogue into Prompt (With Specific Event Data)
    messages = [{"role": "system", "content": Routes.BATTLE_CONTEXT_SIMPLE_AGENT},
                {"role": "user", "content":
                    f"\n You: {str(self)} "
                    f"\n Targets: {str_targets}"
                    f"\n Action:{str(event.summary)}"
                 }]

    # Execute OpenAI API call (Second call, for modifying data structures)
    # Retrieve name and parameters of GPT function call
    tool_data = get_response_tool(messages, tools, event.category)

    # Setup common argument aliases
    function_args = tool_data.get('args')

    updated_chars = []

    target_id = function_args.get('targetID')

    # Execute function according to matched name
    match tool_data.get('name'):
        case "handle_attack":
            # Match Target Weapon (Item)
            weapon_name = function_args.get('weapon')
            print(f"Provided Target ID: {target_id} | Provided Weapon : {weapon_name}")
            weapon = next((item for item in self.inventory if weapon_name == item.name), None)

            # Match Target ID
            target = next((character for character in targets if character.id == target_id), None)

            # Perform Attack & Collect Results
            print(f"Found Target: {target.name} | Found Weapon : {str(weapon.name)} Dmg:{str(weapon.damage)}")
            attack_results = handle_attack(self, target, weapon)
            updated_chars.append(attack_results["target"])

            # Append the Event
            resolved_events.append(attack_results["event"])

        case "handle_wait":
            summary = function_args.get('summary')
            wait_info = handle_wait(self, summary)
            resolved_events.append(wait_info["event"])

        case "handle_item":
            # Match Target Item
            item_name = function_args.get('item')
            print(f"Provided Target ID: {target_id} | Provided Item : {item_name}")
            item = next((item for item in self.inventory if item_name == item.name), None)

            # Match Target ID
            target = next((character for character in targets if character.id == target_id), None)

            # Perform Usage & Collect Results
            print(f"Found Target: {target.name} | Found Item : {str(item.name)}")
            item_results = handle_item(self, target, item)
            updated_chars.append(item_results.get("user"))

            if item_results.get("target") is not None:
                updated_chars.append(item_results.get("target"))

            # Append the Event
            resolved_events.append(item_results["event"])

    # Log the new Reaction Events created from the Event Actions
    for event in resolved_events:
        # for event in events:
        # Dump Events into Log
        append(Routes.PATH_LOG_EVENTS, str(event))

    return {'events': resolved_events, 'updated_chars': updated_chars}


def generate_conclusion(battle_events):
    str_battle_events = '\n'.join(str(event) for event in battle_events)
    # Execute OpenAI API call
    print("[OPENAI]: REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": Routes.BATTLE_CONTEXT_CONCLUDER},
            {"role": "user", "content": str_battle_events}
        ]
    )
    print("| RESPONSE RECEIVED")
    print(str(response.choices[0].message.content))
    return str(response.choices[0].message.content)


# Helper functions to reduce duplication
def tool_for(category=None):
    # Force use of function based on Event category. This helps reduce GPT confusion
    event_tool_map = {
        "Attack": "handle_attack",
        "Wait": "handle_wait",
        "Item": "handle_item",
        "AI": "npc_action_description"
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
