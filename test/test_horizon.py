import unittest
from simulation import horizon


class HorizonTest(unittest.TestCase):
    def test_horizon(self):
        neighbors = {
            'a': [1, 2],
            'b': [2, 3],
            'c': [3, 4],
            1: ['a'],
            2: ['a', 'b'],
            3: ['b', 'c'],
            4: ['c']
        }

        edge_availability = {'a': 1, 'b': 2, 'c': 3}

        with self.subTest():
            h = horizon.time_ignoring(neighbors, 1)
            self.assertEqual(h, {2, 3, 4})

        with self.subTest():
            h = horizon.time_respecting(neighbors, edge_availability, 1, 0)
            self.assertEqual(h, {2: 1, 3: 2, 4: 3})
