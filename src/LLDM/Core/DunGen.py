import json
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import openai

from LLDM.Core.CharGen import new_npc
from LLDM.Utility import Routes

# Using Sam Ogden's provided API Key for LLDM
# noinspection SpellCheckingInspection
openai.api_key = os.environ['GPTAPI']
MODEL = "gpt-3.5-turbo"
MODEL_PREVIEW = "gpt-4-1106-preview"


class RoomFlags:
    """Object to hold flags, to indicate notable features of a node"""
    def __init__(self):
        self.has_chest = False
        self.has_npc = False
        self.visited = False
        self.degree = -1

    def __repr__(self):
        return ' '.join(f"{key}: {value} |" for key, value in self.__dict__.items())


def gen_flags():
    """Function to initialize flags. USes double percentage to randomly toggle flags."""
    flags = RoomFlags()
    if random.random() < 0.2:
        flags.has_chest = True
    if random.random() < 0.2:
        flags.has_npc = True
    return flags


def setup_dungeon(num_nodes: int, starting_character):
    """
    Dungeon Node-Graph Initialization
    :param num_nodes: the number of nodes in this graph. Ex. Rooms in a Dungeon.
    :param starting_character: a character that will be initialized in the first room.
    :return: A NetworkX Barabasi_Albert Graph Object, with attributes holding game information inside the Graph & its Nodes.
    """

    g = nx.barabasi_albert_graph(num_nodes, 1)

    # Build Node-Map
    for i in range(num_nodes):
        g.add_node(i, name=f'Node {i}', description=f'Description {i}', characters=[], flags=gen_flags())

    # Assign Flag: Terminal (Node has only 1 connection)
    for i in range(num_nodes):
        g.nodes[i]['flags'].degree = g.degree(i)

    # Default starting point is first node
    g.graph['current_node'] = [entry[0] for entry in g.nodes.data()][0]

    # Render first node (explicitly, rest are done through Scene>Map's move_to()
    print(f'Rendering First Node...')
    name, description, npc = node_detailer(g.nodes[0].get('flags'), "A dark room in a deep dungeon")
    g.add_node(0, name=f'{name}', description=f'{description}', characters=[starting_character])
    if npc:
        g.nodes[0]['characters'].append(npc)
        print(f"Added NPC:{npc.name} to node's characters")
    g.nodes[0]['flags'].visited = True

    # Draw the dungeon map using Matplotlib
    nx.draw(g, with_labels=True, font_weight='bold', node_size=700, node_color='lightgray', font_color='black',
            font_size=8)
    plt.show()
    return g


def node_detailer(flags, prev_node_name: str = None):
    """
    Function to generate detailed node attributes by calling GPT with basic area information
    :param prev_node_name: optional details of previous location, for thematic consistency/continuity
    :param flags:
    :return: The string name & description, as well as the npc (Character) of the Node
    """

    print(f"Rendering Node with flags: {flags}")
    str_flags = ""
    if flags.degree > 0:
        str_flags += f"\nThis location has {flags.degree} connection(s) to other location(s)"

    if flags.has_npc:
        str_flags += "\nThis location contains an enemy NPC."

    if flags.has_chest:
        str_flags += "\nThis location contains a chest"

    # Execute OpenAI API call
    print("[OPENAI]: REQUEST SENT", end=" ")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "system", "content": Routes.CONTEXT_DUNGEON},
                  {"role": "user", "content": f"Previous Location: {prev_node_name}"},
                  {"role": "user", "content": f"Next Location Details: {str_flags}"}],
        tools=[{
            "type": "function",
            "function": {
                "name": "detail_dungeon",
                "description": "Create new names and descriptions for the location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the location",
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the location"
                        },
                        "npc": {
                            "type": "integer",
                            "description": "0 or a 1 depending on whether there is an Enemy NPC"
                        }
                    },
                    "required": ["name", "description", "npc"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "detail_dungeon"}}
    )
    print("| RESPONSE RECEIVED")

    # Return name and parameters of GPT function call
    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    npc = None
    if args.get('npc') == 1:
        npc = new_npc()

    print(f"{args.get('name')} | {args.get('description')} | NPC: {npc}")

    return args.get('name'), args.get('description'), npc
