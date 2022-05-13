from datetime import datetime

import orjson
import networkx as nx


class Hypergraph:

    def __init__(self, hedge_vertices: dict, hedges_data=None, vertices_data=None):
        self._vertices = set()
        self._hyperedges = set()
        for hedge, vertices in hedge_vertices.items():
            self._vertices.update(vertices)
            self._hyperedges.add(hedge)

        self._bipartite_graph = nx.Graph()

        self._bipartite_graph.add_nodes_from(
            self._vertices, bipartite='vertex')
        self._bipartite_graph.add_nodes_from(
            self._hyperedges, bipartite='hyperedge')

        if hedges_data:
            assert not (set(hedges_data.keys()) - self._hyperedges), 'hedge_data contain non-hyperedges'
            nx.set_node_attributes(self._bipartite_graph, hedges_data)

        if vertices_data:
            assert not (set(vertices_data) - self._vertices), 'vertices_data contain non-vertices'
            nx.set_node_attributes(self._bipartite_graph, vertices_data)

        for hedge, vertices in hedge_vertices.items():
            for vertex in vertices:
                self._bipartite_graph.add_edge(vertex, hedge)

    def get_hedge_data(self, distance_attribute, hedge=None):
        if hedge:
            return self._bipartite_graph.nodes[hedge][distance_attribute]
        else:
            return {hedge: self._bipartite_graph.nodes[hedge][distance_attribute]
                    for hedge in self._hyperedges}

    def hyperedges(self, vertex=None):
        if vertex:
            return set(self._bipartite_graph[vertex])
        return set(self._hyperedges)

    def vertices(self, hedge=None):
        if hedge:
            return set(self._bipartite_graph[hedge])
        return set(self._vertices)


class CommunicationNetwork(Hypergraph):

    def __init__(self, channel_dict, channel_data=None, name=None):
        super().__init__(channel_dict, channel_data)
        self.name = name

    def channels(self, participant=None):
        return self.hyperedges(participant)

    def participants(self, channel=None):
        return self.vertices(channel)

    @classmethod
    def from_json(cls, file_path: str, name=None):
        with open(file_path, 'r', encoding='utf8') as json_file:
            raw_data = orjson.loads(json_file.read())  # pylint: disable=maybe-no-member
        hedge_dict = {chan_id: {
            str(p) for p in channel['participants']} for chan_id, channel in raw_data.items()}
        hedge_data = {chan_id: {
            'start': datetime.fromisoformat(channel['start']),
            'end': datetime.fromisoformat(channel['end']),
        } for chan_id, channel in raw_data.items()}

        return cls(hedge_dict, hedge_data, name=name)
