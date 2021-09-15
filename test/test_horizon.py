import unittest
import networkx as nx
from simulation import horizon


class HorizonTest(unittest.TestCase):
    def test_horizon(self):
        B = nx.Graph()
        nodes_1 = [1, 2, 3, 4]
        nodes_2 = ['a', 'b', 'c']
        B.add_nodes_from(nodes_1, bipartite=0)
        B.add_nodes_from(nodes_2, bipartite=1)
        B.add_edges_from([(1, 'a'), (2, 'a'), (2, 'b'),
                         (3, 'b'), (3, 'c'), (4, 'c')])

        for i, n in enumerate(nodes_2):
            B.nodes[n]['t'] = i+1

        with self.subTest():
            h = horizon.time_ignoring(B, 1)
            self.assertEqual(h, {2, 3, 4})

        with self.subTest():
            h = horizon.time_respecting(B, 1, 0, node_presence_attr='t')
            self.assertEqual(h, {2: 1, 3: 2, 4: 3})

    def test_bipartite_check(self):
        B = nx.Graph()
        B.add_edge(1, 1)

        with self.subTest():
            with self.assertRaises(Exception):
                horizon.time_ignoring(B, 1, check_bipartite=True)

        with self.subTest():
            with self.assertRaises(Exception):
                horizon.time_respecting(B, 1, 0, 't', True)
