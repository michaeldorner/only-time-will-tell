from datetime import datetime, time
import os
import orjson # for encoding because of performance
import json # for decoding because of scalability

_data_dir = os.path.dirname(os.path.abspath(__file__))

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
    def _default(obj):
        if isinstance(obj, set):
            return {o: None for o in obj}
        raise TypeError
    b = orjson.dumps(horizons, default=_default)
    with open(_create_file_name(is_time_respecting, postfix_name), 'wb') as f:
        f.write(b)


def load_horizons(is_time_respecting: bool, time_parsing: bool, postfix_name: str = 'horizons.json') -> dict:
    print('The loading can take several minutes')
    with open(_create_file_name(is_time_respecting, postfix_name), 'r') as f:
        d = json.loads(f.read())
    if time_parsing and is_time_respecting:
        for k in (d):
            for kk in d[k]:
                d[k][kk] = datetime.datetime.fromisoformat(d[k][kk])
    else:
        return d
    if is_time_respecting:
        return {k: {kk: datetime.datetime.fromisoformat(d[k][kk]) for kk in d[k]} for k in d}
    else:
        return {k: {kk for kk in d[k]} for k in d}
