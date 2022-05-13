import unittest
from datetime import datetime

import networkx as nx

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
        result = run.simulation_respecting_time(self.cn, show_progress=False)
        expected = {'v1': {'v1', 'v2', 'v3', 'v4'},
                    'v3': {'v2', 'v3', 'v4'},
                    'v2': {'v1', 'v2', 'v3', 'v4'},
                    'v4': {'v3', 'v4'}}
        self.assertEqual(result, expected)


class BFSTest(unittest.TestCase):

    def test_time_ignoring_bfs(self):
        hypergraph = model.Hypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': {'t': 1}, 'h2': {'t': 2}, 'h3': {'t': 3}})
        vertices = hypergraph.vertices()
        hyperedges = hypergraph.hyperedges()
        vertex_hyperedges = {vertex: hypergraph.hyperedges(vertex) for vertex in vertices}
        hyperedge_vertices = {hedge: hypergraph.vertices(hedge) for hedge in hyperedges}

        available_hyperedges = {}
        for hedge in hypergraph.hyperedges():
            next_hedges: set = set()
            for next_vertex in hypergraph.vertices(hedge):
                for next_hedge in hypergraph.hyperedges(next_vertex):
                    next_hedges.add(next_hedge)
            available_hyperedges[hedge] = next_hedges - {hedge}

        with self.subTest():
            ti_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v1')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            ti_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v2')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            ti_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v3')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            ti_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v4')
            self.assertEqual(ti_bfs, {'v1', 'v2', 'v3', 'v4'})

    def test_time_respecting_bfs(self):
        hypergraph = model.Hypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': {'t': 1}, 'h2': {'t': 2}, 'h3': {'t': 3}})
        vertices = hypergraph.vertices()
        hyperedges = hypergraph.hyperedges()
        vertex_hyperedges = {vertex: hypergraph.hyperedges(vertex) for vertex in vertices}
        hyperedge_vertices = {hedge: hypergraph.vertices(hedge) for hedge in hyperedges}

        hedge_data = hypergraph.get_hedge_data('t')

        available_hyperedges = {}
        for hedge in hypergraph.hyperedges():
            next_hedges: set = set()
            for next_vertex in hypergraph.vertices(hedge):
                for next_hedge in hypergraph.hyperedges(next_vertex):
                    if hedge_data[hedge] < hedge_data[next_hedge]:
                        next_hedges.add(next_hedge)
            available_hyperedges[hedge] = next_hedges - {hedge}

        with self.subTest():
            tr_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v1')
            self.assertEqual(tr_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            tr_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v2')
            self.assertEqual(tr_bfs, {'v1', 'v2', 'v3', 'v4'})

        with self.subTest():
            tr_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v3')
            self.assertEqual(tr_bfs, {'v2', 'v3', 'v4'})

        with self.subTest():
            tr_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, 'v4')
            self.assertEqual(tr_bfs, {'v3', 'v4'})

    def test_bfs_networkx(self):
        hypergraph = model.Hypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': {'t': 1}, 'h2': {'t': 2}, 'h3': {'t': 3}})
        vertices = hypergraph.vertices()
        hyperedges = hypergraph.hyperedges()
        vertex_hyperedges = {vertex: hypergraph.hyperedges(vertex) for vertex in vertices}
        hyperedge_vertices = {hedge: hypergraph.vertices(hedge) for hedge in hyperedges}

        available_hyperedges = {}
        for hedge in hypergraph.hyperedges():
            next_hedges: set = set()
            for next_vertex in hypergraph.vertices(hedge):
                for next_hedge in hypergraph.hyperedges(next_vertex):
                    next_hedges.add(next_hedge)
            available_hyperedges[hedge] = next_hedges - {hedge}

        bipartite = hypergraph._bipartite_graph  # pylint: disable=protected-access
        for source_vertex in vertices:
            r_networkx = {n for n in nx.node_connected_component(bipartite, source_vertex) if n in vertices}
            r_bfs = run.bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, source_vertex)

            self.assertEqual(r_networkx, r_bfs)
