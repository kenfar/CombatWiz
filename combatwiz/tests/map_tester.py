#!/usr/bin/env python

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import combatwiz.map  as map

class MapTester(unittest.TestCase):

    def setUp(self):
        self.map1 = map.Mapper()
        self.map2 = map.Mapper()
        self.map3 = map.Mapper()
        self.maps = [self.map1, self.map2, self.map3]

    def test_nodes(self):
        new_map = map.Mapper()
        assert(len(new_map.graph) == 400)

    def test_edges(self):
        for graph in self.maps:
            for node in graph.graph:
                edge = (node.x in [0, 19] or node.y in [0, 19])
                corner = (node.x in [0, 19] and node.y in [0, 19])
                if edge:
                    if corner:
                        edge_assert(node, 3)
                    else:
                        edge_assert(node, 5)
                else:
                    edge_assert(node, 8)

def edge_assert(node, count):
    '''
    Custon assert statement
    '''
    if len(node.edges) != count:
        print "Node: ", node.x, node.y
        print "Edges: ", [(item.x, item.y) for item in node.edges]
        print "Count: %i / %i" % (len(node.edges), count)
        raise AssertionError, "Wrong Edge Count"

if __name__ == "__main__":
    unittest.main()
