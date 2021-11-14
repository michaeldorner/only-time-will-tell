import unittest
from simulation import horizon


class HorizonTest(unittest.TestCase):
    def test_horizon(self):

        data = {
            'a': {
                'participants': {1, 2},
                'start': 0,
                'end': 1
            },
            'b': {
                'participants': {2, 3},
                'start': 0,
                'end': 2
            },
            'c': {
                'participants': {3, 4},
                'start': 0,
                'end': 3
            },
        }
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

    # def test_bipartite_check(self):
    #     B = nx.Graph()
    #     B.add_edge(1, 1)

    #     with self.subTest():
    #         with self.assertRaises(Exception):
    #             horizon.time_ignoring(B, 1, check_bipartite=True)

    #     with self.subTest():
    #         with self.assertRaises(Exception):
    #             horizon.time_respecting(B, 1, 0, 't', True)
