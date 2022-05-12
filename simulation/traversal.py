from .model import Hypergraph


def bfs(hypergraph: Hypergraph, source_vertex, distance_attr=None, filter_distance=lambda distance: False):
    backlog = set()
    for source_hedge in hypergraph.hyperedges(source_vertex):
        backlog.add(source_hedge)

    visited_hedges = set()
    seen_vertices = set()

    while backlog:
        hedge = backlog.pop()
        for vertex in hypergraph.vertices(hedge):
            if vertex not in seen_vertices:
                seen_vertices.add(vertex)
                for next_hedge in hypergraph.hyperedges(vertex):
                    if distance_attr:
                        distance = hypergraph.get_hedge_data(distance_attr, next_hedge) - \
                            hypergraph.get_hedge_data(distance_attr, hedge)
                    else:
                        distance = None
                    if next_hedge not in visited_hedges and not filter_distance(distance):
                        visited_hedges.add(next_hedge)
                        backlog.add(next_hedge)
    return seen_vertices
