#!/usr/bin/env python

import sys
import networkx as nx
import numpy
import matplotlib.pyplot as plt

def main():
    new_map = Mapper()
    new_map.display()

class Mapper:

    def __init__(self, dimensions=(20, 20), axes=8):
        '''
        Class for network
        '''
        self.dimensions = dimensions
        self.graph = nx.Graph()
        self.initialize_graph(dimensions)
        self.create_edges(axes)

    def initialize_graph(self, dimensions):
        '''
        Initialize the number of nodes needed
        '''
        for x in range(dimensions[0]):
            for y in range(dimensions[1]):
                new_node = Node()
                new_node.x = x
                new_node.y = y
                self.graph.add_node(new_node)

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
        nx.draw_networkx(self.graph,
                         pos=position,
                         font_size=5,
                         linewidths=0.5,
                         width=0.5)
        plt.show()

    def establish_positions(self, dimensions):
        '''
        Get grid positions
        '''
        positions = {}
        for node in self.graph:
            positions[node] = [node.x, node.y]
        return positions

class Node:
    def __init__(self):
        '''
        Node class
        '''
        self.x        = None
        self.y        = None
        self.contents = None
        self.edges    = []


if __name__ == "__main__":
    sys.exit(main())
