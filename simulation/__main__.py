import argparse
from . import simulation


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='Name of the simulation run.')
    parser.add_argument('--cache', action='store_true',
                        help='Cache full simulation results in JSON file; requires about 45 GB of storage.')
    parser.add_argument('--time_ignoring_only', action='store_true',
                        help='Simulate the time-ignoring model only.')
    parser.add_argument('--time_respecting_only', action='store_true',
                        help='Simulate the time-respecting model only.')
    args = parser.parse_args()

    consider_time = []
    if args.time_ignoring_only == args.time_respecting_only:
        consider_time = [False, True]
    elif args.time_ignoring_only and not args.time_respecting_only:
        consider_time = [False]
    elif not args.time_ignoring_only and args.time_respecting_only:
        consider_time = [True]

    simulation.run(args.name, consider_time, args.cache)
