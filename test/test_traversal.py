import unittest
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
