import argparse
from . import simulation


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--time_ignoring_only', action='store_true',
                        help='Simulate the time-ignoring model only.')
    parser.add_argument('--time_respecting_only', action='store_true',
                        help='Simulate the time-respecting model only.')
    parser.add_argument('--skip_storing_horizon', action='store_false',
                        help='Do not store the horizons as JSON (~50 GB needed) before calculating the cardinalities.')
    args = parser.parse_args()

    consider_time = []
    if args.time_ignoring_only == args.time_respecting_only:
        consider_time = [False, True]
    elif args.time_ignoring_only and not args.time_respecting_only:
        consider_time = [False]
    elif not args.time_ignoring_only and args.time_respecting_only:
        consider_time = [True]
    simulation.run(consider_time, args.skip_storing_horizon)
