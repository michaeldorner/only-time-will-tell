import argparse

from simulation import run, model, store

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--time_ignoring_only', action='store_true',
                        help='Simulate the time-ignoring model only.')
    parser.add_argument('--time_respecting_only', action='store_true',
                        help='Simulate the time-respecting model only.')
    parser.add_argument('--skip_storing_reachable', action='store_true',
                        help='Do not store the all reachable participants \
                            as JSON before calculating the cardinalities. \
                            This saves about 50 GB on your disk.')

    args = parser.parse_args()

    simulation_runs = []
    if args.time_ignoring_only == args.time_respecting_only:
        simulation_runs = [False, True]
    elif args.time_ignoring_only and not args.time_respecting_only:
        simulation_runs = [False]
    elif not args.time_ignoring_only and args.time_respecting_only:
        simulation_runs = [True]

    cn = model.CommunicationNetwork.from_json('data/simulation_parameters.json')

    for consider_time in simulation_runs:
        if consider_time:
            reachables = run.simulation_respecting_time(cn, cache=True)
            file_prefix = 'time_respecting'
        else:
            reachables = run.simulation_ignoring_time(cn)
            file_prefix = 'time_ignoring'

        if args.skip_storing_reachable is False:
            store.to_json(reachables, f'{file_prefix}_reachables.json')

        upper_bound = {v: len(reachable) for v, reachable in reachables.items()}
        store.to_json(upper_bound, f'{file_prefix}_upper_bound.json')
