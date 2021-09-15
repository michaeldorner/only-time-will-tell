import unittest
from simulation import model


class ModelTest(unittest.TestCase):
    def test_model(self):
        self.assertEqual(len(model.participants), 37103)
        self.assertEqual(len(model.channels), 309740)

        self.assertEqual(len(model.bipartite_graph.nodes), 346843)
        self.assertEqual(len(model.bipartite_graph.edges), 695356)
