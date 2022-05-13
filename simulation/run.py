from tqdm.auto import tqdm

from simulation.model import CommunicationNetwork


def bfs(hyperedge_vertices, vertex_hyperedges, available_hyperedges, source_vertex):
    backlog = set()
    for source_hedge in vertex_hyperedges[source_vertex]:
        backlog.add(source_hedge)

    visited_hedges = set()
    seen_vertices = set()

    while backlog:
        hedge = backlog.pop()
        seen_vertices.update(hyperedge_vertices[hedge])
        for next_hedge in available_hyperedges[hedge]:
            if next_hedge not in visited_hedges:
                visited_hedges.add(next_hedge)
                backlog.add(next_hedge)

    return seen_vertices


def simulation_ignoring_time(communication_network: CommunicationNetwork, show_progress=True):
    disable = not show_progress
    participants = communication_network.participants()
    channels = communication_network.channels()
    channel_participants = {channel: communication_network.vertices(channel) for channel in channels}
    participant_channels = {participant: communication_network.hyperedges(participant) for participant in participants}

    available_channels = {}
    for channel in tqdm(channels, desc='Caching available channels', disable=disable):
        next_channels: set = set()
        for participant in channel_participants[channel]:
            for next_channel in participant_channels[participant]:
                next_channels.add(next_channel)
        available_channels[channel] = next_channels - {channel}

    result = {}
    with tqdm(total=len(participants), desc='Simulating ignoring time', disable=disable) as pbar:
        for participant in participants:
            if participant not in result:
                reachable_participants = bfs(channel_participants, participant_channels, available_channels, participant)
                for cc_p in reachable_participants:  # we take advantage of symmetry
                    if cc_p not in result:
                        result[cc_p] = reachable_participants - {cc_p}
                        pbar.update()
    return result


def simulation_respecting_time(communication_network: CommunicationNetwork, show_progress=True):
    disable = not show_progress
    participants = communication_network.participants()
    channels = communication_network.channels()
    channel_participants = {channel: communication_network.vertices(channel) for channel in channels}
    participant_channels = {participant: communication_network.hyperedges(participant) for participant in participants}
    channel_distance = communication_network.get_hedge_data('end')

    available_channels = {}
    for channel in tqdm(communication_network.channels(), desc='Caching available channels', disable=disable):
        next_channels: set = set()
        for participant in channel_participants[channel]:
            for next_channel in participant_channels[participant]:
                if channel_distance[channel] < channel_distance[next_channel]:
                    next_channels.add(next_channel)
        available_channels[channel] = next_channels - {channel}

    result = {}
    for participant in tqdm(participants, desc='Simulating respecting time', disable=disable):
        result[participant] = bfs(channel_participants, participant_channels, available_channels, participant)
    return result
