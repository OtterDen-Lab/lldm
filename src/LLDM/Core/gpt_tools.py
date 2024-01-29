import json
import os
from enum import Enum

import openai

from LLDM.Core.Character import Character
from LLDM.Core.Item import Item
from LLDM.Core.Map import Map
from LLDM.Core.Scene import Event


# Using Sam Ogden's provided API Key for LLDM, add an environment variable keyed 'GPTAPI' with the value of the API key.
# noinspection SpellCheckingInspection
openai.api_key = os.environ['GPTAPI']
MODEL = "gpt-3.5-turbo"
MODEL_PREVIEW = "gpt-4-1106-preview"

# ChatCompletion Helper functions to reduce duplication
def tool_for(category=None):
    """
    Helper function to force use of function based on Event category.
    :param category: Enum type of action as determined by GPT
    :return: a snippet of json that determines tool use in a ChatCompletion call
    """
    event_tool_map = {
        # StoryGPT Tools
        "Item Generation": "create_item",
        "Movement": "handle_movement",
        "Examine": "handle_examine",
        "Battle": "handle_battle",
        # BattleGPT Tools
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
    """
    :param messages: the dialogue to be processed by GPT
    :param tools: the functions to be made accessible to GPT
    :param category: optional arg to force use of a specific tool
    :return: tuple of the function name and arguments used by GPT
    """
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


# ChatCompletion Tools & Handlers
class Tools(Enum):
    """
    Enum Class to hold the various JSON function/tools for GPT to use
    """
    # First Call - Resolve Input into described action
    CREATE_EVENT = {
        "type": "function",
        "function": {
            "name": "create_event",
            "description": "Process the user text into a described action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the event stemming from the resolved player action.",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Item Generation", "Movement", "Examine", "Battle"],
                        "description": "What category the event is most like. Exploration includes opening doors or actions that would reveal locations. Movement is character locomotion. Examine gives more information about something. Battle is the party choosing to fight the enemy (or enemies) in the current room. Pick one from the enum."
                    },
                    "summary": {
                        "type": "string",
                        "description": "The eloquent narration of what occurred in the event"
                    }
                },
                "required": ["title", "category", "summary"]
            }
        }
    }
    ILLEGAL_ACTION = {
        "type": "function",
        "function": {
            "name": "illegal_action",
            "description": "If the player tries to do something impossible, too improbable, or otherwise unfitting a low-level RPG character",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "enum": ["Prompt Injection Attack", "Beyond Character Capabilities", "Other"],
                        "description": "What category the illegal action is closest to. Pick one from the enum."
                    }
                },
                "required": ["title"],
            }
        }
    }

    # Second Call - Apply described action to game data
    CREATE_ITEM = {
        "type": "function",
        "function": {
            "name": "create_item",
            "description": "Create an Item Object as a result of an Event revealing a container's contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the item generated."
                    },
                    "description": {
                        "type": "string",
                        "description": "A brief description of the physical characteristics of the item."
                    },
                    "damage": {
                        "type": "integer",
                        "description": "An optional parameter to be added for when an Item is some sort of weapon."
                    },
                    "amount": {
                        "type": "integer",
                        "description": "An optional parameter for when an Item contains multiple homogenous items, like a bag of coins, or a quiver of arrows."
                    }
                },
                "required": ["name", "description"],
            }
        }
    }
    HANDLE_MOVEMENT = {
        "type": "function",
        "function": {
            "name": "handle_movement",
            "description": "Handles player movement between nodes in the game map",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_index": {
                        "type": "integer",
                        "description": "The node index of the node (first number provided in the game map)."
                    }
                },
                "required": ["moving_into"],
            }
        }
    }
    HANDLE_EXAMINE = {
        "type": "function",
        "function": {
            "name": "handle_examine",
            "description": "Provide additional details about a game object upon examination.",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["Item", "Location", "Character"],
                        "description": "The type of object being examined."
                    },
                    "obj_name": {
                        "type": "string",
                        "description": "The name of best fitting object. If object is a node/location, provide only the integer index"
                    },
                    "obj_owner_name": {
                        "type": "string",
                        "description": "If applicable, this is the name of whoever possesses the item"
                    },

                    "description": {
                        "type": "string",
                        "description": "A rewritten description, safelky extrapolating upon details (such as node connections, or other characteristics). Just the facts, no addressing any observers."
                    }
                },
                "required": ["type", "obj_name", "description"]
            }
        }
    }
    HANDLE_BATTLE = {
        "type": "function",
        "function": {
            "name": "handle_battle",
            "description": "Handles a battle between the party and the enemies in the given location on the map.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "A descriptive summary of how the characters start to prepare themselves to fight."
                    }
                },
                "required": ["summary"],
            }
        }
    }

    # Battle Division Calls

    # This makes a simulated user input for NPCs
    CREATE_AI_INPUT = {
        "type": "function",
        "function": {
            "name": "npc_action_description",
            "description": "Describe a combat action taken by an NPC",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the event stemming from the resolved character action. It should be concise.",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Attack", "Wait", "Item"],
                        "description": "What category the event is most like. Attack is an action which deals damage to an enemy. Wait is an action where the character does nothing or waits around. Item is an action where the character uses an item that does not deal damage. Pick one from the enum."
                    },
                    "summary": {
                        "type": "string",
                        "description": "The description of the combat action taken"
                    }
                },
                "required": ["title", "category", "summary"]
            }
        }
    }

    # This is the battle-equivalent of CREATE_EVENT.
    # This is an input-processor specifically tailored to analyze user inputs in the context of a battle.
    CREATE_BATTLE_EVENT = {
        "type": "function",
        "function": {
            "name": "create_battle_event",
            "description": "Process the user text into a described battle action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the event stemming from the resolved character action. It should be concise, but include at minimum the character name and category type. Other relevant information may be included if provided by User Input string.",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Attack", "Wait", "Item"],
                        "description": "What category the event is most like. Attack is an action which deals damage to an enemy. Wait is an action where the character does nothing or waits around. Item is an action where the character uses an item that does not deal damage. Pick one from the enum."
                    },
                    "summary": {
                        "type": "string",
                        "description": "The eloquent narration of what occurred in the event."
                    }
                },
                "required": ["title", "category", "summary"]
            }
        }
    }

    # Second Call - Apply described action to game data
    HANDLE_ATTACK = {
        # TODO: Add anything else needed to compute an attack.
        "type": "function",
        "function": {
            "name": "handle_attack",
            "description": "Handles player attack against another character, be it player, enemy, or NPC.",
            "parameters": {
                "type": "object",
                "properties": {
                    "targetID": {
                        "type": "integer",
                        "description": "The _id attribute of the character being attacked, ignoring capitalization for character names. Set to -1 if no character is specified or the character being attacked doesn't have an _id attribute."
                    },
                    "weapon": {
                        "type": "string",
                        "description": "The name of the weapon being used for the attack. If a weapon is not specified or the character doesn't have the weapon, set this to None."
                    }
                },
                "required": ["targetID", "weapon"],
            }
        }
    }
    HANDLE_WAIT = {
        "type": "function",
        "function": {
            "name": "handle_wait",
            "description": "Handles player waiting around and passing their turn.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "The description of the character waiting around."
                    }
                },
                "required": ["summary"]
            }
        }
    }
    HANDLE_ITEM = {
        # TODO: Add anything else needed to use the Item.
        "type": "function",
        "function": {
            "name": "handle_item",
            "description": "Handles player action to use an item. The item's effect will vary depending on the item's description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "targetID": {
                        "type": "integer",
                        "description": "The ID of the character being targetted for the item use, ignoring capitalization for character names. Set to -1 if no character is specified or the character being targetted doesn't have an ID."
                    },
                    "item": {
                        "type": "string",
                        "description": "The name of the item being used. If an item is not specified or the character doesn't have the item, set this to None."
                    }
                },
                "required": ["targetID", "item"],
            }
        }
    }


def illegal_action(title: str):
    print(f"User inputted an illegal action: {title}")
    return False


def create_event(title: str, summary: str, category: str):
    """

    :param title: the name of the event
    :param summary: a brief description of what occurred
    :param category: an Enum string assigning what type of Event this is
    :return:
    """
    print(f"[Event] ChatGPT wanted to make an Event: [{category}] {title}")
    return Event(title, summary, category)


def create_item(name: str, description: str, **kwargs):
    """
    :param name: the item's name
    :param description: standard description of the item
    :param kwargs: extra parameters afforded to certain Items.
    :return: tuple of the Item object and the Event associated with its creation
    """
    print(f"[Event] ChatGPT wanted to make an Item: {name}")
    # Assuming Item can take damage and amount as None
    item = Item(name, description, damage=kwargs.get("damage"), amount=kwargs.get("amount"))
    return item, create_event(name, description, "Item Generated")


def handle_movement(target_index: int, game_map: Map):
    """
    Determine viability of move to a neighboring node, and then update the graph's Current Node attribute to reflect the change
    :param target_index: integer of a node in the NetworkX Barabasi_Albert Graph
    :param game_map: the current Map object (holding the graph, which has the node)
    :return: the game map (may or may not be updated)
    """
    print(f"[Event] ChatGPT wanted to perform a Movement into Node {target_index}")
    possible_node = game_map.map.nodes[target_index]
    img_req = False
    if possible_node is not None:
        # If the destination node is unvisited, set img_visited to false
        if not game_map.is_node_visited(target_index):
            img_req = True
        game_map.move_to(target_index)
    else:
        print(f"Move failed: No Node found with matching name.")

    return {"game_map": game_map, "img_gen": img_req}


def handle_attack(attacker: Character, target: Character, weapon: Item):
    """
    Attack Function: You can add/remove/edit the parameters as needed.
    :param attacker: a Character object performing the attack
    :param target: a Character object receiving the attack
    :param weapon: the weapon (Item) used in the attack
    :return: tuple containing updated target object, and associated Event
    """
    print(
        f"[Battle Event] ChatGPT wanted to perform an Attack from {attacker.name} onto {target.name} using {weapon.name}.")

    target.health -= weapon.damage

    if target.health <= 0:
        target.health = 0
        target.alive = False

    event_summary = f"Attack from {attacker.name} onto {target.name} using {weapon.name}. This did {weapon.damage} damage, and now {target.name} has {target.health} health left."

    print(f"[Battle Event Resolve] {event_summary}")
    return {"target": target, "event": create_event("Attack:", event_summary, "Attack")}


def handle_item(user: Character, item: Item, target: Character):
    """
    Handles item usage.
    :param user: the Character activating/consuming the Item
    :param item: the used Item
    :param target: the Character receiving the effects
    :return: tuple containing the updated user, target, item, and associated Event
    """
    def apply_item_effect(character: Character):
        """
        Internal function for actual item application (extend this for more item effects)
        :param character: recipient Character
        :return: string communicating item effect
        """
        if item.healing is not None:
            character.health += item.healing
            return f"{item.name} used by {user.name} onto {character.name}. This healed {item.healing} damage, and now {character.name} has {character.health} health left."
        return f"{user.name} attempted to use {item.name} onto {character.name}. But no effect happened."

    # Target Designation for item application
    print(f"[Battle Event] ChatGPT wanted to perform an Item action: {item.name} | {user.name} -> {target.name}")
    user.inventory.remove(item)
    if user.id == target.id:
        target = None
        event_summary = apply_item_effect(user)
    else:
        event_summary = apply_item_effect(target)

    result = {"user": user, "target": target, "item": item, "event": create_event("", event_summary, "Item")}
    print(f"[Battle Event Resolve] {event_summary}")
    return result


def handle_wait(character: Character, summary: str):
    """
    Battle function to handle character skipping turn
    :param character: active Character
    :param summary: brief description of the character waiting in place
    :return:
    """
    print(f"[Battle Event] ChatGPT wanted to perform a Wait action for {character.name}.")
    print(f"[Battle Event Resolve] {summary}")
    return {"event": create_event(
        "",
        summary,
        "Wait"
    )}


def handle_examine(obj_type: str, obj_name: str, new_description: str, **kwargs):
    """
    Handler Function to rewrite an object's description given subject metadata by GPT
    :param obj_type: class of the Item
    :param obj_name: name (or index, in the case of nodes) of the object
    :param new_description: successor description
    :param kwargs: extra information
    :return: updated object
    """

    scene = kwargs.get('scene')
    character = None

    # print("\nEntered handle_examine function!\n")
    if obj_type == "Item":
        print("\nExamine Type: Item\n")
        obj_owner_name = kwargs.get('obj_owner_name')
        if obj_owner_name is not None:
            for char in scene.loc_map.get_current_characters():
                if char.name == obj_owner_name:
                    # Find the item in the inventory
                    for item in char.inventory:
                        if item.name == obj_name:
                            # Update the item's description
                            item.description = new_description
                            return item  # Return the updated item
                    print(f"Item named {obj_name} not found in inventory.")

    elif obj_type == "Location":
        print("\nExamine Type: Location\n")
        game_map = scene.loc_map
        if game_map:
            # Find the node in the game map
            node_index = int(obj_name)
            if node_index in game_map.map:
                # Update the node's description
                game_map.set_node_attrs(node_index, "description", new_description)
                return game_map  # Return the updated game_map
            else:
                print(f"Location named {obj_name} not found.")
        else:
            print("Game map not provided.")

    elif obj_type == "Character":
        for char in scene.loc_map.get_current_characters():
            if char.name == obj_name:
                char.description += " " + new_description
                return char  # Return the updated character

        # if characters:
        #     # Find the character
        #     for character in characters:
        #         if character.name == obj_name:
        #             # Update the character's description
        #             character.description += " " + new_description
        #             return character  # Return the updated character
        #     print(f"Character named {obj_name} not found.")
        # else:
        #     print("Character list not provided.")

    else:
        print(f"Unknown type: {obj_type}")


def create_ai_input(title: str, summary: str, category: str):
    """
    Event instantiating handler for AI input processing
    """
    npc_action_event = create_event(title, summary, category)
    print(f"[AI INPUT] ChatGPT wanted to make an AI INPUT: {npc_action_event}")
    return npc_action_event

