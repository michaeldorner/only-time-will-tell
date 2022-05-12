import argparse

from simulation import run, model, store

FILE_PREFIX = {
    True: 'time_respecting',
    False: 'time_ignoring'
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--time_ignoring_only', action='store_true',
                        help='Simulate the time-ignoring model only.')
    parser.add_argument('--time_respecting_only', action='store_true',
                        help='Simulate the time-respecting model only.')
    parser.add_argument('--skip_storing_reachables', action='store_true',
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

    microsoft_code_review = model.CommunicationNetwork.from_json('data/microsoft_code_review.json')

    for consider_time in simulation_runs:
        reachables = {}
        if consider_time:
            reachables = run.simulation_respecting_time(microsoft_code_review)
        else:
            reachables = run.simulation_ignoring_time(microsoft_code_review)

        if args.skip_storing_reachables is False:
            store.to_json(reachables, f'{FILE_PREFIX[consider_time]}_reachables.json')

        upper_bound = {v: len(reachable) for v, reachable in reachables.items()}
        store.to_json(upper_bound, f'{FILE_PREFIX[consider_time]}_upper_bound.json')
        reachables = {}
        upper_bound = {}
