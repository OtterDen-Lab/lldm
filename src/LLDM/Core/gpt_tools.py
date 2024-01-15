from enum import Enum
from LLDM.Core.Scene import Event, Item, Location, Map, Character

battle = None


class Tools(Enum):
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
                        "enum": ["Item Generation", "Movement", "Exploration", "Examine", "Battle"],
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
    CREATE_LOCATION = {
        "type": "function",
        "function": {
            "name": "create_location",
            "description": "Create a new Location (a location not present in the game map). Make sure you only describe the features, which must include a new exit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the new location."
                    },
                    "description": {
                        "type": "string",
                        "description": "The description of the new location. Make sure it has some sort of exit. This is only the description of the LOCATION, and should not be addressed to anybody"
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
            "description": "Handles player movement between existing locations in the game map",
            "parameters": {
                "type": "object",
                "properties": {
                    "moving_into": {
                        "type": "string",
                        "description": "The name of the entered location (provided in the game map)."
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
                        "description": "The name of best fitting object"
                    },
                    "obj_owner_name": {
                        "type": "string",
                        "description": "If applicable, this is the name of whoever possesses the item"
                    },

                    "description": {
                        "type": "string",
                        "description": "A rewritten description, retaining all important details but also including new ones. Just the facts, no addressing any observers."
                    }
                },
                "required": ["type", "obj_name", "description"]
            }
        }
    }
    # TODO: Implement properties
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
    # TODO: Add more battle events
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
    print(f"[Event] ChatGPT wanted to make an Event: [{category}] {title}")
    return Event(title, summary, category)


def create_location(name: str, description: str, game_map: Map):
    print(f"[Event] ChatGPT wanted to make a Location: {name}")
    if game_map.get_location_by_name(name) is None:
        new_location = Location(name, description)
        game_map.add_location(new_location)
        # Only linear connections (if working as intended): New location & Old location. (then move)
        game_map.connect_locations(game_map.current_location, new_location)
        # Atomic move into new location (could be decoupled, but harder to define)
        # print("Moving into new location")
        game_map = handle_movement(new_location.name, game_map)
    else:
        print(f"[EventError] ChatGPT wanted to make a Location that already exists. Skipping creation")

    return game_map, create_event(name, description, "Location Generated")
    # Trying to make non-linear connections by having adjacency given by gpt
    # print(f"ChatGPT wanted to connect them to: {adjacent_names}")
    # print(f"connecting {new_location} to")
    # for adjacent_name in adjacent_names:
    #     print(f"{adjacent_name}")
    #     adjacent_location = game_map.get_location_by_name(adjacent_name)
    #     game_map.connect_locations(new_location, adjacent_location)


def create_item(name: str, description: str, **kwargs):
    print(f"[Event] ChatGPT wanted to make an Item: {name}")
    # Assuming Item can take damage and amount as None
    item = Item(name, description, damage=kwargs.get("damage"), amount=kwargs.get("amount"))
    return item, create_event(name, description, "Item Generated")


def handle_movement(moving_into: str, game_map: Map):
    print(f"[Event] ChatGPT wanted to perform a Movement into {moving_into}")
    possible_location = game_map.get_location_by_name(moving_into)
    if possible_location is not None:
        game_map.move_to(possible_location)
        # print(f"Current location: {game_map.get_current_location()}")
    else:
        print(f"Move failed: No location found with matching name. Was ChatGPT supposed to create a location instead?")
    return game_map


# Create functions to be called by GPT via Tool-calls.

def handle_input_battle(user_input, resolve_response=None):
    global battle

    # If user_input == "END", the battle has ended and response contains updated object info
    while user_input != "END":
        response = battle.get_action_response(user_input, battle.get_turn_character())
        if response is None:
            # Web app needs to print something about the action being invalid and to go again?
            break

        battle.resolve_turn(battle.get_turn_character())

        resolve_response = battle.get_action_input()
        if resolve_response is None: break  # New player input required

        user_input = resolve_response.get('prompt_input')

    return resolve_response


def get_new_battle_events_GPT_Tools():
    global battle
    return battle.get_battle_events()


# Attack Function: You can add/remove/edit the parameters as needed.
# TODO: Damage Calculator
# TODO: Handle variations of attacks (weapon, spells, ???)
def handle_attack(attacker: Character, target: Character, weapon: Item):
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
    # Internal function for actual item application (extend this for more item effects)
    def apply_item_effect(character: Character):
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
    print(f"[Battle Event] ChatGPT wanted to perform a Wait action for {character.name}.")
    print(f"[Battle Event Resolve] {summary}")
    return {"event": create_event(
        "",
        summary,
        "Wait"
    )}


def handle_examine(obj_type: str, obj_name: str, new_description: str, **kwargs):
    scene = kwargs.get('scene')

    character = None

    # print("\nEntered handle_examine function!\n")
    if obj_type == "Item":
        print("\nType Item\n")
        obj_owner_name = kwargs.get('obj_owner_name')
        if obj_owner_name is not None:
            for char in scene.characters:
                if char.name == obj_owner_name:
                    # Find the item in the inventory
                    for item in char.inventory:
                        if item.name == obj_name:
                            # Update the item's description
                            item.description = new_description
                            return item  # Return the updated item
                    print(f"Item named {obj_name} not found in inventory.")

    elif obj_type == "Location":
        print("\nType Location\n")
        game_map = scene.loc_map
        if game_map:
            # Find the location in the game map
            location = game_map.get_location_by_name(obj_name)
            if location:
                # Update the location's description
                location.description = new_description
                return game_map  # Return the updated game_map
            else:
                print(f"Location named {obj_name} not found.")
        else:
            print("Game map not provided.")

    elif obj_type == "Character":
        for char in scene.characters:
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
    npc_action_event = create_event(title, summary, category)
    print(f"[AI INPUT] ChatGPT wanted to make an AI INPUT: {npc_action_event}")
    return npc_action_event
