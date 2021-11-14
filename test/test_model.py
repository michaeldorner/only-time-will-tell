import unittest
from simulation import model, io


class ModelTest(unittest.TestCase):
    def test_model(self):
        json_file_path = io.abs_dir_path(
            __file__).parent / 'data/simulation_parameters.json'
        data = io.load_json(json_file_path)
        cn = model.CommunicationNetwork(data)
        self.assertEqual(len(cn.participants), 37103)
        self.assertEqual(len(cn.channels), 309740)

        self.assertEqual(len(cn.nodes), 346843)
        self.assertEqual(len(cn.edges), 695356)
