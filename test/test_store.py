import unittest
from simulation import store
from pathlib import Path
import os


class DecodeResultTest(unittest.TestCase):
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
                b = store._decode_result(result)
                self.assertEqual(b, reference)


class StoreResultTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.test_file_path = Path('results') / 'test.json'

    def test_store_result(self):
        store.to_json({'a': set()}, 'test.json')
        with open(self.test_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, '{"a":{}}')

    def tearDown(self):
        if self.test_file_path.exists():
            os.remove(self.test_file_path)
