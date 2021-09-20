from datetime import datetime
import os
import orjson


_data_dir = os.path.dirname(os.path.abspath(__file__))

def _default(obj):
    if isinstance(obj, set):
        return {o: None for o in obj}
    raise TypeError

def _create_file_name(is_time_respecting: bool, postfix_name: str):
    file_name = {
        True: 'time_respecting_',
        False: 'time_ignoring_'
    }[is_time_respecting] + postfix_name

    return os.path.join(_data_dir, file_name)


def load_simulation_parameters() -> dict:
    with open(os.path.join(_data_dir, 'simulation_parameters.json'), 'r') as json_file:
        data = orjson.loads(json_file.read())
    return {k: {
        'start': datetime.fromisoformat(data[k]['start']),
        'end': datetime.fromisoformat(data[k]['end']),
        'participants': set(data[k]['participants']),
    } for k in data}


def store_horizons(horizons, is_time_respecting: bool, postfix_name: str = 'horizons.json'):
    if is_time_respecting:
        horizons = {str(k): {str(kk): horizons[k][kk].isoformat(
        ) for kk in horizons[k]} for k in horizons}
    else:
        horizons = {str(k): [str(kk) for kk in horizons[k]] for k in horizons}
    print('start jsonizing...')
    b = orjson.dumps(horizons, default=_default)
    with open(_create_file_name(is_time_respecting, postfix_name), 'wb') as f:
        f.write(b)


def load_horizons(is_time_respecting: bool, postfix_name: str = 'horizons.json') -> dict:
    with open(_create_file_name(is_time_respecting, postfix_name), 'r') as f:
        d = orjson.loads(f.read())
    if is_time_respecting:
        return {k: {kk: datetime.datetime.fromisoformat(d[k][kk].isoformat()) for kk in d[k]} for k in d}
    else:
        return {k: {kk for kk in d[k]} for k in d}
