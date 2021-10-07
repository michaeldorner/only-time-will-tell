import unittest
from simulation.data import io
import os


class IOFileNameTest(unittest.TestCase):
    def test_file_name(self):
        with self.subTest():
            file_name = io.absolute_file_path(
                is_time_respecting=True, postfix_name='horizon.json')
            self.assertEqual(file_name, os.path.join(
                io._data_dir, 'time_respecting_horizon.json'))
        with self.subTest():
            file_name = io.absolute_file_path(
                is_time_respecting=False, postfix_name='horizon.json')
            self.assertEqual(file_name, os.path.join(
                io._data_dir, 'time_ignoring_horizon.json'))


class IOParameterTest(unittest.TestCase):
    def test_load_simulation_parameters(self):
        params = io.load_simulation_parameters()
        self.assertEqual(len(list(params)), 309740)


class IODecodeResultTest(unittest.TestCase):
    def test_decode_result(self):
        mapping = [
            (0, {'a': {'b', 'c'}, 'd': set()},
             b'{"a":{"b":null,"c":null},"d":{}}'),
            (1, {'a': {'d', 'c'}, 'd': set()},
             b'{"a":{"c":null,"d":null},"d":{}}'),
            (2, {'d': set(), 'a': {'d', 'c'}},
             b'{"a":{"c":null,"d":null},"d":{}}'),
            (3, {'a': {'b': 1, 'c': 2}, 'd': {}},
             b'{"a":{"b":1,"c":2},"d":{}}'),
            (4, {'a': 2, 'd': 0}, b'{"a":2,"d":0}'),
            (5, {'d': 0, 'a': 2}, b'{"a":2,"d":0}')
        ]

        for i, result, reference in mapping:
            with self.subTest(i=i):
                b = io.decode_result(result)
                self.assertEqual(b, reference)


class IOStoreResultTest(unittest.TestCase):
    def test_store_result(self):
        postfix_name = 'test.json'
        io.store_result({'a': set()}, True, postfix_name)
        test_file_path = io.absolute_file_path(True, postfix_name)
        with open(test_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, '{"a":{}}')

    def tearDown(self):
        test_file_path = io.absolute_file_path(True, 'test.json')
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
