import unittest
from simulation import simulation
import networkx as nx


class SimulationTest(unittest.TestCase):
    def test_horizons(self):
        B = nx.Graph()
        B.add_edge(1, 2)
        B.add_edge(2, 3)
        B.nodes[2]['t'] = 1

        with self.subTest():
            r = simulation.time_ignoring_horizons(B, [1, 3])
            self.assertEqual(r, {1: {3}, 3: {1}})

        with self.subTest():
            r = simulation.time_respecting_horizons(B, [1, 3], 0, 't')
            self.assertEqual(r, {1: {3: 1}, 3: {1: 1}})

        with self.subTest():
            r = simulation.time_respecting_horizons(B, [1, 3], 1, 't')
            self.assertEqual(r, {1: {}, 3: {}})
