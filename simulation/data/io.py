import pandas as pd
import json
from datetime import datetime
import os


_data_dir = os.path.dirname(os.path.abspath(__file__))


def _create_file_name(is_time_respecting: bool, dir_name: str, postfix_name: str):
    result_dir = os.path.join(_data_dir, dir_name)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    file_name = {
        True: 'time_respecting_',
        False: 'time_ignoring_'
    }[is_time_respecting] + postfix_name

    return os.path.join(result_dir, file_name)


def load_simulation_parameters() -> dict:
    with open(os.path.join(_data_dir, 'simulation_parameters.json'), 'r') as json_file:
        data = json.load(json_file)
    return {k: {
        'start': datetime.fromisoformat(data[k]['start']),
        'end': datetime.fromisoformat(data[k]['end']),
        'participants': set(data[k]['participants']),
    } for k in data}


def store_horizons(horizons, is_time_respecting: bool, dir_name: str, postfix_name: str = 'horizons.json'):
    if is_time_respecting:
        horizons = {str(k): {str(kk): horizons[k][kk].isoformat(
        ) for kk in horizons[k]} for k in horizons}
    else:
        horizons = {str(k): [str(kk) for kk in horizons[k]] for k in horizons}
    print('start jsonizing...')
    with open(_create_file_name(is_time_respecting, dir_name, postfix_name), 'w') as f:
        json.dump(horizons, f, sort_keys=True, indent=1)


def load_horizons(is_time_respecting: bool, dir_name: str, postfix_name: str = 'horizons.json') -> dict:
    with open(_create_file_name(is_time_respecting, dir_name, postfix_name), 'r') as f:
        d = json.load(f)
    if is_time_respecting:
        return {k: {kk: datetime.datetime.fromisoformat(d[k][kk].isoformat()) for kk in d[k]} for k in d}
    else:
        return {k: {kk for kk in d[k]} for k in d}


def store_horizon_cardinalities(horizons: dict, is_time_respecting: bool, dir_name: str, postfix_name: str = 'cardinalities.feather'):
    pd.Series({k: len(horizons[k]) for k in horizons}).to_feather(
        _create_file_name(is_time_respecting, dir_name, postfix_name))


def load_horizon_cardinalities(is_time_respecting: bool, dir_name: str, postfix_name: str = 'cardinalities.feather') -> pd.Series:
    return pd.read_feather(_create_file_name(is_time_respecting, dir_name, postfix_name))
