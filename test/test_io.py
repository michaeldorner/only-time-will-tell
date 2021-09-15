import unittest
from simulation.data import io
import os


class HDFParamsTest(unittest.TestCase):
    def test_create_file_name(self):
        t = io._create_file_name(True, 'test', 'test')
        self.assertEqual(t, os.path.join(
            io._data_dir, 'test', 'time_respecting_test'))


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
