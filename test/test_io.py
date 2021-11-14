import unittest
from simulation import io
import os


class IODirectoryValidationTest(unittest.TestCase):
    def test_invalid_file(self):
        self.assertRaises(FileNotFoundError,
                          io.validate_file, '!NOTEXISTING!')

    def test_valid_file(self):
        self.assertEqual(io.validate_file(__file__), __file__)

    def test_invalid_directory(self):
        self.assertRaises(NotADirectoryError,
                          io.validate_directory, '!NOTEXISTING!')

    def test_valid_directory(self):
        self.assertEqual(io.validate_directory('.'), '.')


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
    def setUp(self):
        super().setUp()
        self.test_file_path = './time_respecting_test.json'

    def test_store_result(self):
        postfix_name = 'test.json'
        io.store_result({'a': set()}, './', True, postfix_name)
        with open(self.test_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, '{"a":{}}')

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
