import unittest
from simulation import simulation, model


class SimulationTest(unittest.TestCase):
    def test_horizons(self):

        data = {
            2: {
                'participants': {1, 3},
                'start': 0,
                'end': 1
            }
        }

        cn = model.CommunicationNetwork(data)
        # cn.add_nodes_from(
        #     cn.participants, bipartite='participants')
        # cn.add_nodes_from(channels, bipartite='channels')

        # cn.add_edge(1, 2)
        # cn.add_edge(2, 3)
        # cn.nodes[2]['t'] = 1

        with self.subTest():
            r = simulation.time_ignoring_horizons(cn)
            self.assertEqual(r, {1: {3}, 3: {1}})

        with self.subTest():
            seed_times = {1: 0, 3: 0}
            r = simulation.time_respecting_horizons(cn, seed_times)
            self.assertEqual(r, {1: {3: 1}, 3: {1: 1}})

        with self.subTest():
            seed_times = {1: 1, 3: 1}
            r = simulation.time_respecting_horizons(cn, seed_times)
            self.assertEqual(r, {1: {}, 3: {}})
