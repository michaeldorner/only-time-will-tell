from tqdm import tqdm
from datetime import datetime

from . import horizon
from . import model
from .data import io


def time_ignoring_horizons(bipartite_graph, nodes):
    horizons = {}
    with tqdm(total=len(nodes), desc='Time-ignoring simulation') as pbar:
        for node in nodes:
            if node not in horizons:
                h = horizon.time_ignoring(
                    bipartite_graph, node) | {node}
                # this works because of the symmetry characteristic of horizon in undirected graphs
                for n in h:
                    horizons[n] = h - {n}
                    pbar.update()
    return horizons


def time_respecting_horizons(bipartite_graph, nodes, seed_time, node_presence_attr):
    horizons = {}
    for node in tqdm(nodes, desc='Time-respecting simulation'):
        horizons[node] = horizon.time_respecting(
            bipartite_graph, node, seed_time, node_presence_attr)

    return horizons


def run(consider_time: list, skip_storing_horizon: bool):
    for is_time_respecting in consider_time:
        horizons = {}
        if is_time_respecting:
            horizons = time_respecting_horizons(
                model.bipartite_graph, model.participants, datetime(2020, 1, 1), 'end')
        else:
            horizons = time_ignoring_horizons(
                model.bipartite_graph, model.participants)
        if not skip_storing_horizon:
            io.store_horizons(horizons, is_time_respecting)
        io.store_horizon_cardinalities(horizons, is_time_respecting)
