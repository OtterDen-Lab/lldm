from enum import Enum
from LLDM.Objects.Scene import Event, Item, Location, Map


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
                        "enum": ["Item Generation", "Movement", "Exploration", "General Inquiry"],
                        "description": "What category the event is most like. Exploration includes opening doors or actions that would reveal locations. Movement is character locomotion. Pick one from the enum."
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
    HANDLE_PERCEPTION = {
        "type": "function",
        "function": {
            "name": "handle_perception",
            "description": "General-purpose function to reveal more detail about the game environment. This includes searching for details and answering questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of query.",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Your natural response as a TTRPG DM, provide details, clues or events to give something the player can interact with and keep the story going."
                    }
                },
                "required": ["title", "summary"],
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


def illegal_action(title: str):
    print(f"User inputted an illegal action: {title}")
    return False


def create_event(title: str, summary: str, category: str, **kwargs):
    print(f"ChatGPT wanted to make an Event: [{category}] {title}")
    return Event(title, summary, category)


def create_location(name, description, game_map, **kwargs):
    print(f"ChatGPT wanted to make a Location: {name}")
    if game_map.get_location_by_name(name) is None:
        new_location = Location(name, description)
        game_map.add_location(new_location)
        # Only linear connections (if working as intended): New location & Old location. (then move)
        game_map.connect_locations(game_map.get_current_location(), new_location)

        print("Atomically moving into new connection")
        game_map = handle_movement(new_location.name, game_map)
    else:
        print(f"ChatGPT wanted to make a Location that already exists. Skipping creation")

    return game_map, create_event(name, description, "Location Generated")
    # Trying to make non-linear connections by having adjacency given by gpt
    # print(f"ChatGPT wanted to connect them to: {adjacent_names}")
    # print(f"connecting {new_location} to")
    # for adjacent_name in adjacent_names:
    #     print(f"{adjacent_name}")
    #     adjacent_location = game_map.get_location_by_name(adjacent_name)
    #     game_map.connect_locations(new_location, adjacent_location)


def create_item(name, description, damage=None, amount=None, **kwargs):
    print(f"ChatGPT wanted to make an Item: {name}")
    # Assuming Item can take damage and amount as None
    item = Item(name, description, damage=damage, amount=amount)
    return item, create_event(name, description, "Item Generated")
    # Only useful if we're passing this back into GPT through messages.append({"content": function_response})
    # return obj_to_json(item)


def handle_movement(moving_into, game_map, **kwargs):
    print(f"ChatGPT wanted to Move a character into {moving_into}")
    possible_location = game_map.get_location_by_name(moving_into)
    if possible_location is not None:
        game_map.move_to(possible_location)
        print(f"Current location: {game_map.get_current_location()}")
    else:
        print(f"Move failed: No location found with matching name. Was ChatGPT supposed to create a location instead?")
    return game_map
