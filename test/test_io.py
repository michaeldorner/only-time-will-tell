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


class IOStoreHorizonsTest(unittest.TestCase):

    def setUp(self):
        self.postfix_name = 'horizons_test.json'
        self.file_name = io._create_file_name(
            is_time_respecting=True, postfix_name=self.postfix_name)

    def test_store_time_respecting_horizons(self):
        horizons = {'a': {'b': 1, 'c': 2}, 'd': {}}
        io.store_horizons(
            horizons, True, self.postfix_name)

        with self.subTest():
            self.assertTrue(os.path.exists(self.file_name))

        with self.subTest():
            with open(self.file_name, 'r') as f:
                horizons_written = json.load(f)
            self.assertEqual(horizons, horizons_written)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)


class IOStoreCardinalitiesTest(unittest.TestCase):

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
