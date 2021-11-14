import unittest
from simulation import model, io


class ModelTest(unittest.TestCase):
    def test_model(self):
        data = io.load_json('./data/simulation_parameters.json')
        cn = model.CommunicationNetwork(data)
        self.assertEqual(len(cn.participants), 37103)
        self.assertEqual(len(cn.channels), 309740)

        self.assertEqual(len(cn.nodes), 346843)
        self.assertEqual(len(cn.edges), 695356)
