from tqdm import tqdm

from . import horizon


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
