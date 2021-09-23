from datetime import datetime
import os
import orjson

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


def store_horizon_cardinalities(horizons, is_time_respecting: bool, postfix_name: str = 'horizon_cardinalities.json'):
    b = orjson.dumps({k: len(horizons[k]) for k in horizons})
    with open(_create_file_name(is_time_respecting, postfix_name), 'wb') as f:
        f.write(b)
