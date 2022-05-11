from datetime import timedelta

from tqdm.auto import tqdm

from simulation.model import CommunicationNetwork
from simulation.traversal import bfs


def simulation_ignoring_time(communication_network: CommunicationNetwork, show_progress=True):
    disable = not show_progress
    participants = communication_network.participants()
    result = {}
    with tqdm(total=len(participants), desc='Simulating ignoring time', disable=disable) as pbar:
        for participant in participants:
            if participant not in result:
                reachable_participants = bfs(communication_network, participant)
                for p in reachable_participants:
                    if p not in result:
                        result[p] = reachable_participants - {p}
                        pbar.update()
    return result


def simulation_respecting_time(communication_network: CommunicationNetwork, cache=False, show_progress=True):
    disable = not show_progress
    def filter_distance(distance): return distance <= timedelta(seconds=0)
    if cache:
        for channel in tqdm(communication_network.channels(), desc='Caching channel neighbors', disable=disable):
            communication_network.channel_neighbors(channel, 'end', filter_distance)
    result = {}
    for participant in tqdm(communication_network.participants(), desc='Simulating respecting time', disable=disable):
        result[participant] = bfs(communication_network, participant, 'end', filter_distance)
    return result
