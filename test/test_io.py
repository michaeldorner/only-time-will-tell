import unittest
from simulation.data import io
import os
import json


class IOFileNameTest(unittest.TestCase):
    def test_file_name(self):
        with self.subTest():
            file_name = io._create_file_name(
                is_time_respecting=True, postfix_name='horizon.json')
            self.assertEqual(file_name, os.path.join(
                io._data_dir, 'time_respecting_horizon.json'))
        with self.subTest():
            file_name = io._create_file_name(
                is_time_respecting=False, postfix_name='horizon.json')
            self.assertEqual(file_name, os.path.join(
                io._data_dir, 'time_ignoring_horizon.json'))


class IOParameterTest(unittest.TestCase):
    def test_load_simulation_parameters(self):
        params = io.load_simulation_parameters()
        self.assertEqual(len(list(params)), 309740)


class IOStoreTest(unittest.TestCase):

    def setUp(self):
        self.postfix_name = 'horizon_cardinalities_test.json'
        self.file_name = io._create_file_name(
            is_time_respecting=True, postfix_name=self.postfix_name)

    def test_store_horizon_cardinalities(self):
        horizons = {'a': {'b': 1, 'c': 2}, 'd': {}}
        horizon_cardinalities = {'a': 2, 'd': 0}
        io.store_horizon_cardinalities(
            horizons, True, self.postfix_name)

        with self.subTest():
            self.assertTrue(os.path.exists(self.file_name))

        with self.subTest():
            with open(self.file_name, 'r') as f:
                horizons_written = json.load(f)
            self.assertEqual(horizon_cardinalities, horizons_written)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)


# class IOStoreCardinalityTest(unittest.TestCase):
#     def setUp(self):
#         self.file_name = 'test_horizon_cardinalities.hdf'
#         self.file_path = os.path.join(io._data_dir, self.file_name)

#     def tearDown(self):
#         os.remove(self.file_path)

#     def test_store_cardinality(self):
#         io.store_horizon_cardinalities({1: 1}, True, self.file_name)
#         self.assertTrue(os.path.exists(self.file_path))


# class IOLoadCardinalityTest(unittest.TestCase):
#     def setUp(self):
#         self.file_name = 'test_horizon_cardinalities.hdf'
#         self.file_path = os.path.join(io._data_dir, self.file_name)
#         io.store_horizon_cardinalities({1: 1}, False, self.file_name)
#         assert os.path.exists(
#             self.file_path), 'Horizon cardinalities are not created.'

#     def tearDown(self):
#         os.remove(self.file_path)

#     def test_load_horizon_cardinality(self):
#         s = io.load_horizon_cardinalities(False, self.file_name)
#         self.assertEqual(s.size, 1)


# class IOStoreHorizonTest(unittest.TestCase):
#     def setUp(self):
#         self.file_name = 'test_horizons.hdf'
#         self.file_path = os.path.join(io._data_dir, self.file_name)

#     def tearDown(self):
#         os.remove(self.file_path)

#     def test_store_cardinality(self):
#         io.store_horizons({1: {1}}, False, self.file_name)
#         self.assertTrue(os.path.exists(self.file_path))
