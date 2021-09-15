import networkx as nx
from datetime import datetime
from .data import io


def __load_bipartite_graph(raw_data: dict, participants: set, channels: set) -> nx.Graph:
    bipartite_graph = nx.Graph()
    bipartite_graph.add_nodes_from(participants, bipartite='participants')
    bipartite_graph.add_nodes_from(channels, bipartite='channels')

    for channel_id, channel in raw_data.items():
        bipartite_graph.nodes[channel_id]['start'] = channel['start']
        bipartite_graph.nodes[channel_id]['end'] = channel['end']
        for p in channel['participants']:
            bipartite_graph.add_edge(p, channel_id)

    return nx.freeze(bipartite_graph)


simulation_parameters = io.load_simulation_parameters()
participants = {participant for channel in simulation_parameters.values()
                for participant in channel['participants']}
channels = set(simulation_parameters.keys())
bipartite_graph = __load_bipartite_graph(
    simulation_parameters, participants, channels)
