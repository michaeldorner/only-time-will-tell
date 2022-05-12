import unittest

from simulation.model import CommunicationNetwork, Hypergraph


class ModelTest(unittest.TestCase):
    hedge_data = {'h1': {'t': 1}, 'h2': {'t': 2}, 'h3': {'t': 3}}
    vertex_data = {f'v{i}': {} for i in range(1, 5)}
    h = Hypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, hedge_data, vertex_data)

    def test_vertices(self):
        self.assertEqual(len(self.h.vertices()), 4)
        self.assertEqual(self.h.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges(self):
        self.assertEqual(len(self.h.hyperedges()), 3)
        self.assertEqual(self.h.vertices('v2'), {'h1', 'h2'})

    def test_hedge_attributes(self):
        hedge_data = {'h1': 1, 'h2': 2, 'h3': 3}
        self.assertEqual(self.h.get_hedge_data('t'), hedge_data)


class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/microsoft_code_review.json')
        self.assertEqual(len(communciation_network.channels()), 309740)
        self.assertEqual(len(communciation_network.hyperedges()), 309740)

        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.vertices()), 37103)
