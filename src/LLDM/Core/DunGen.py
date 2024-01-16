import random
import networkx as nx
import matplotlib.pyplot as plt


# Create flags for notable features
class RoomFlags:
    def __init__(self):
        self.has_chest = False
        self.has_npc = False

    def __repr__(self):
        return ' '.join(f"{key}: {value} |" for key, value in self.__dict__.items())


def gen_flags():
    flags = RoomFlags()
    if random.random() < 0.2:
        flags.has_chest = True
    if random.random() < 0.2:
        flags.has_npc = True
    return flags


def setup_dungeon(num_nodes: int):
    g = nx.barabasi_albert_graph(num_nodes, 1)

    for i in range(num_nodes):
        g.add_node(i, name=f'Room {i + 1}')
        g.add_node(i, description=f'Description {i + 1}')
        g.add_node(i, flags=gen_flags())

    g.graph['current_node'] = [entry[0] for entry in g.nodes.data()][0]

    # Draw the dungeon map using Matplotlib
    nx.draw(g, with_labels=True, font_weight='bold', node_size=700, node_color='lightgray', font_color='black',
            font_size=8)
    plt.show()
    return g


# dungeon = setup_dungeon(5)
# print(dungeon.graph['current_node'])

# for node in nx.neighbors(dungeon, 0):
#     print(node)

# print(1 in nx.neighbors(dungeon, 0))

# print(dungeon.nodes[0].get('name'))
# dungeon.nodes[0]['name'] = "new"
# print(dungeon.nodes[0].get('name'))

# print(dungeon.graph['current_location'])
#
# print(dungeon.nodes[0])
#
# for node, data in dungeon.nodes.data():
#     if data["name"] == "Room 1":
#         print(node)

