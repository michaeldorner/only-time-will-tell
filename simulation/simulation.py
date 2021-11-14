import concurrent.futures
from . import horizon
from . import model
from tqdm import tqdm


def time_ignoring_horizons(cn: model.CommunicationNetwork) -> dict:
    neighbors: dict = {n: list(cn.neighbors(n)) for n in cn.nodes}
    horizons: set = dict()
    with tqdm(total=len(cn.participants), desc='Time-ignoring simulation') as pbar:
        for participant in cn.participants:
            if participant not in horizons:
                h = horizon.time_ignoring(neighbors, participant) | {
                    participant}
                # this works because of the symmetry characteristic of horizon in undirected graphs
                for p in h:
                    horizons[p] = h - {p}
                    pbar.update()
    return horizons


def time_respecting_horizons(cn: model.CommunicationNetwork, timings: dict) -> dict:
    neighbors: dict = {n: list(cn.neighbors(n)) for n in cn.nodes}
    edge_availability: dict = {c: cn.nodes[c]['end'] for c in cn.channels}
    horizons: dict = dict()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(
            horizon.time_respecting, neighbors, edge_availability, p, timings[p]): p for p in cn.participants}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc='Time-respecting simulation'):
            n = futures[future]
            horizons[n] = future.result()
    return horizons
