import networkx as nx

from LLDM.Core.CharGen import starter_character
from LLDM.Core.DunGen import setup_dungeon, node_detailer


class Map:
    """
    Map Class. A Wrapper to manage a Graph. (Node/Graph by NetworkX)
    """
    def __init__(self, size: int):
        self._map = setup_dungeon(size, starter_character())

    def __str__(self):
        # Create a string representation of the graph listing all nodes, connections, and attributes
        def neighbors(node: int):
            """
            Data concatenate/string converter
            :param node: index of node in graph
            :return: tuple of string data of neighbor nodes and attributes
            """
            nbrs = ' '.join(str(node) for node in nx.neighbors(self._map, node))
            attrs = self.get_attrs(node)
            return f'{nbrs} | {attrs} '

        return '\n'.join(f'Node: {str(node)} -> {neighbors(node)}' for node in self._map.nodes)

    @property
    def map(self):
        return self._map

    @property
    def current_node(self):
        print(f"Current Node Called: {self._map.graph['current_node']}")
        return self._map.graph['current_node']

    def get_current_characters(self):
        return self._map.nodes[self.current_node]['characters']

    @current_node.setter
    def current_node(self, new_node: int):
        # Access the Node Index, NOT the attrs
        new_num = [entry[0] for entry in self._map.nodes.data()][new_node]
        print(f'New Num: {new_num}')

        self._map.graph['current_node'] = new_num

    def set_node_attrs(self, node_index: int, key: str, value):
        self._map.nodes[node_index][key] = value

    def move_to(self, destination: int):
        """
        Update graph's 'current node' attribute & populate destination node's attributes
        :param destination: integer index of node in graph
        :return: this Map object
        """
        if destination in nx.neighbors(self._map, self.current_node):
            print(f'Found {destination} in neighbors. Attempting to move')

            # Transfer (party) characters
            for character in self._map.nodes[destination]['characters']:
                if character.entity == "party":
                    self._map.nodes[self.current_node]['characters'].append(character)

            self.current_node = destination

            if not self._map.nodes[destination]['flags'].visited:
                print(f'Rendering Node...')
                # Generate and assign fleshed-out attributes, and update flags.
                name, description, npc = node_detailer(self._map.nodes[destination].get('flags'))
                self._map.add_node(destination, name=f'{name}', description=f'{description}')
                if npc is not None:
                    print(f"Added NPC:{npc.name} to node's characters")
                    self._map.nodes[destination]['characters'].append(npc)
                self._map.nodes[destination]['flags'].visited = True

            return self

        else:
            print(f"Cannot move from [{self.current_node}] to [{destination}] . Node not adjacent.")

    def get_relevant_locations_str(self):
        """
        Data concatenate/string converter
        :return: returns a concatenated string of the current and adjacent nodes.
        """
        # return str(f"[Relevant Map]: \n{neighbors(node) for node in }\nCurrent Node: [{str(self.current_node)}]")
        current = f'Node: {self.current_node} | {self.get_attrs(self.current_node)}'
        adjacent = '\n'.join(f'Node: {self.current_node} -> {str(node)} | {self.get_attrs(node)}' for node in
                             nx.neighbors(self._map, self.current_node))
        return f'[Current Node]\n{current}\n[Relevant Map]\n{adjacent}'

    def get_attrs(self, node_index: int):
        """
        Data concatenate/string converter
        :param node_index: integer index of node in graph
        :return: returns a concatenated string of the specified node's attributes
        """
        values_to_join = [str(value) for key, value in self._map.nodes[node_index].items() if key != 'characters']
        return ' | '.join(values_to_join)
