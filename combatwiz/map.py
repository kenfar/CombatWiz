#!/usr/bin/env python

import sys
import networkx as nx
import matplotlib.pyplot as plt
import threading

def main():
    new_map = Mapper(dimensions=(100, 100))
#    new_map.display()
    print new_map.get_route(new_map.get_node('0:0'), new_map.get_node('10:5'))

class Mapper(object):
    '''
    Basic calls for ease of use
    '''
    def get_route(self, source, target):
        '''
        Return list of node traversals
        '''
        return nx.shortest_path(self.graph, source, target)

    def get_node(self, name):
        '''
        Returns node based on id
        '''
        try:
            target_node = self.node_dict[name]
        except KeyError:
            return None
        return target_node

    '''
    Bottom code to establish important things
    '''
    def __init__(self, dimensions=(20, 20), axes=8):
        '''
        Class for network
        '''
        self.dimensions = dimensions
        self.node_dict = {}
        self.graph = nx.Graph()
        self.initialize_graph(dimensions)
        self.create_edges(axes)

    def initialize_graph(self, dimensions):
        '''
        Initialize the number of nodes needed
        '''
        threads = []
        for x in range(dimensions[0]):
            for y in range(dimensions[1]):
                threads.append(threading.Thread(target=self.add_node, args=(x, y)))
        [thread.start() for thread in threads]

    def add_node(self, x, y):
        '''
        Add node to graph
        '''
        new_node = Node()
        new_node.x = x
        new_node.y = y
        new_node.name = "%i:%i" % (x, y)
        self.graph.add_node(new_node)
        self.node_dict[new_node.name] = new_node


    def create_edges(self, axes):
        '''
        Add all edges based on axes
        '''
        for node in self.graph:
            for cursor in self.graph:
                if node == cursor:
                    pass
                x_flag = abs(node.x - cursor.x)
                y_flag = abs(node.y - cursor.y)
                good_val_range = [0, 1]
                if (x_flag == y_flag and x_flag == 0):
                    pass
                elif x_flag in good_val_range and y_flag in good_val_range:
                    self.graph.add_edge(node, cursor)
                    node.edges.append(cursor)

    def display(self):
        '''
        Displays the graph using matplotlib
        '''
        position = self.establish_positions(self.dimensions)
        sizes = self.establish_sizes()
        nx.draw_networkx(self.graph,
                         pos=position,
                         font_size=5,
                         linewidths=0.5,
                         width=0.5,
                         node_size=sizes)
        plt.show()
#        plt.savefig('grid.svg')

    def establish_positions(self, dimensions):
        '''
        Get grid positions
        '''
        positions = {}
        for node in self.graph:
            positions[node] = [node.x, node.y]
        return positions

    def establish_sizes(self):
        '''
        Get node sizes
        '''
        sizes = []
        for node in self.graph:
            sizes.append(20)
        return sizes

class Node:
    __slots__ = ('name', 'x', 'y', 'contents', 'edges')
    def __init__(self):
        '''
        Node class
        '''
        self.name     = None
        self.x        = None
        self.y        = None
        self.contents = None
        self.edges    = []

    def isEmpty(self):
        if self.contents:
            return False
        else:
            return True

class Edge:
    def __init__(self, weight):
        self.weight = weight

if __name__ == "__main__":
    sys.exit(main())
