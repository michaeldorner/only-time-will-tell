from collections import deque
from .model import Hypergraph


def bfs(hypergraph: Hypergraph, source_vertex, distance_attr=None, filter_distance=lambda distance: False):
    d = deque()
    for source_hedge in hypergraph.hyperedges(source_vertex):
        d.append(source_hedge)

    visited_hedges = set()
    seen_vertices = set()
    while d:
        hedge = d.pop()
        seen_vertices |= hypergraph.vertices(hedge)
        for next_hedge in hypergraph.hyperedge_neighbors(hedge, distance_attr, filter_distance):
            if next_hedge not in visited_hedges:
                visited_hedges.add(next_hedge)
                d.append(next_hedge)

    return seen_vertices
