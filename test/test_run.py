import unittest
from datetime import datetime

from simulation import run, model


class SimulationRunTest(unittest.TestCase):

    hedge_data = {'h1': {'end': datetime(2022, 1, 1)},
                  'h2': {'end': datetime(2022, 1, 2)},
                  'h3': {'end': datetime(2022, 1, 3)}}
    cn = model.CommunicationNetwork({'h1': ['v1', 'v2'],
                                     'h2': ['v2', 'v3'],
                                     'h3': ['v3', 'v4']}, hedge_data)

    def test_run_simulation_ignoring_time(self):
        result = run.simulation_ignoring_time(self.cn, show_progress=False)
        expected = {'v1': {'v2', 'v3', 'v4'},
                    'v2': {'v1', 'v3', 'v4'},
                    'v3': {'v1', 'v2', 'v4'},
                    'v4': {'v1', 'v2', 'v3'}}
        self.assertEqual(result, expected)

    def test_run_simulation_respecting_time(self):
        with self.subTest():
            result = run.simulation_respecting_time(self.cn, show_progress=False)
            expected = {'v1': {'v1', 'v2', 'v3', 'v4'},
                        'v3': {'v2', 'v3', 'v4'},
                        'v2': {'v1', 'v2', 'v3', 'v4'},
                        'v4': {'v3', 'v4'}}
            self.assertEqual(result, expected)

        with self.subTest():
            result = run.simulation_respecting_time(self.cn, cache=True, show_progress=False)
            expected = {'v1': {'v1', 'v2', 'v3', 'v4'},
                        'v3': {'v2', 'v3', 'v4'},
                        'v2': {'v1', 'v2', 'v3', 'v4'},
                        'v4': {'v3', 'v4'}}
            self.assertEqual(result, expected)
