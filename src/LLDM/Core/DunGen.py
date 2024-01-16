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


def setup_dungeon(num_nodes):
    graph = nx.barabasi_albert_graph(num_nodes, 1)

    # Draw the dungeon map using Matplotlib
    nx.draw(graph, with_labels=True, font_weight='bold', node_size=700, node_color='lightgray', font_color='black',
            font_size=8)
    plt.show()

    for i in range(len(graph.nodes)):
        graph.add_node(i, name=f'Room {i + 1}')
        graph.add_node(i, description=f'Description {i + 1}')

        flags = set_flags()
        graph.add_node(i, flags=flags)

    return graph


def set_flags():
    flags = RoomFlags()
    if random.random() < 0.2:
        flags.has_chest = True
    if random.random() < 0.2:
        flags.has_npc = True
    return flags


