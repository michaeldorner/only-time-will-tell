import argparse
from datetime import datetime

from . import simulation
from simulation import model
from simulation.data import io


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--time_ignoring_only', action='store_true',
                        help='Simulate the time-ignoring model only.')
    parser.add_argument('--time_respecting_only', action='store_true',
                        help='Simulate the time-respecting model only.')
    parser.add_argument('--skip_storing_horizon', action='store_true',
                        help='Do not store the horizons as JSON (requires ~50 GB) before calculating the cardinalities.')
    args = parser.parse_args()

    consider_time = []
    if args.time_ignoring_only == args.time_respecting_only:
        consider_time = [False, True]
    elif args.time_ignoring_only and not args.time_respecting_only:
        consider_time = [False]
    elif not args.time_ignoring_only and args.time_respecting_only:
        consider_time = [True]

    for is_time_respecting in consider_time:
        horizons = {}
        if is_time_respecting:
            horizons = simulation.time_respecting_horizons(
                model.bipartite_graph, model.participants, datetime(2020, 1, 1), 'end')
        else:
            horizons = simulation.time_ignoring_horizons(
                model.bipartite_graph, model.participants)
        if args.skip_storing_horizon is False:
            io.store_result(horizons, is_time_respecting, 'horizons.json')

        io.store_result({k: len(horizons[k]) for k in horizons},
                        is_time_respecting, 'horizon_cardinalities.json')
