import argparse
from datetime import datetime

from . import simulation
from simulation import model
from simulation import io


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--time_ignoring_only', action='store_true',
                        help='Simulate the time-ignoring model only.')
    parser.add_argument('--time_respecting_only', action='store_true',
                        help='Simulate the time-respecting model only.')
    parser.add_argument('--skip_storing_horizons', action='store_true',
                        help='Do not store the horizons as JSON before calculating the cardinalities.')
    parser.add_argument('--parameter_file',
                        default='./data/simulation_parameters.json',
                        type=io.validate_file,
                        help='JSON file with the simulation parameters.')
    parser.add_argument('--out_dir',
                        type=io.validate_directory,
                        default='./data',
                        help='Store the results in this directory.')
    args = parser.parse_args()

    json_data = io.load_json(args.parameter_file)
    cn = model.CommunicationNetwork(json_data)

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
                cn, {p: datetime(2020, 1, 1) for p in cn.participants})
        else:
            horizons = simulation.time_ignoring_horizons(cn)
        if args.skip_storing_horizons is False:
            io.store_result(horizons, args.out_dir,
                            is_time_respecting, 'horizons.json')

        io.store_result({k: len(horizons[k]) for k in horizons},
                        args.out_dir, is_time_respecting, 'horizon_cardinalities.json')
