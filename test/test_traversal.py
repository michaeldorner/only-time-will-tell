import unittest
import random

import networkx as nx

from simulation.model import Hypergraph
from simulation.traversal import bfs


class TraversalTest(unittest.TestCase):
    h = Hypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': {'t': 1}, 'h2': {'t': 2}, 'h3': {'t': 3}})

    def test_time_ignoring_bfs(self):

        with self.subTest():
            ti_bfs = bfs(self.h, 'v1')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            ti_bfs = bfs(self.h, 'v2')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            ti_bfs = bfs(self.h, 'v3')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            ti_bfs = bfs(self.h, 'v4')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

    def test_time_respecting_bfs(self):

        with self.subTest():
            tr_bfs = bfs(self.h, 'v1', 't', lambda d: d <= 0)
            self.assertEqual(tr_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            tr_bfs = bfs(self.h, 'v2', 't', lambda d: d <= 0)
            self.assertEqual(tr_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            tr_bfs = bfs(self.h, 'v3', 't', lambda d: d <= 0)
            self.assertEqual(tr_bfs, {'v2', 'v3', 'v4'})

        with self.subTest():
            tr_bfs = bfs(self.h, 'v4', 't', lambda d: d <= 0)
            self.assertEqual(tr_bfs, {'v3', 'v4'})

    def test_bfs_networkx(self):

        bipartite = self.h._bipartite_graph
        for source_node in random.choices(list(self.h.vertices()), k=10):
            r_networkx = {n for n in nx.node_connected_component(bipartite, source_node) if n in self.h.vertices()}
            r_bfs = bfs(self.h, source_node)
            self.assertEqual(r_networkx, r_bfs)
