import networkx as nx


class CommunicationNetwork(nx.Graph):

    def __init__(self, data: dict):
        super().__init__()

        self.participants = {participant for channel in data.values()
                             for participant in channel['participants']}
        self.channels = set(data.keys())

        self.add_nodes_from(
            self.participants, bipartite='participants')
        self.add_nodes_from(self.channels, bipartite='channels')

        for channel_id, channel in data.items():
            self.nodes[channel_id]['start'] = channel['start']
            self.nodes[channel_id]['end'] = channel['end']
            for p in channel['participants']:
                self.add_edge(p, channel_id)
