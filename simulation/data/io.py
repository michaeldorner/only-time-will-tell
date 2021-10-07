from datetime import datetime
import os
import orjson

_data_dir = os.path.dirname(os.path.abspath(__file__))


def absolute_file_path(is_time_respecting: bool, postfix_name: str):
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


def decode_result(result: dict) -> bytes:
    def _default(obj):
        if isinstance(obj, set):
            return {o: None for o in sorted(obj)}
        raise TypeError
    return orjson.dumps(result, default=_default, option=orjson.OPT_SORT_KEYS)


def store_result(result: dict, time_respecting: bool, postfix_name: str):
    file_path = absolute_file_path(time_respecting, postfix_name=postfix_name)
    b = decode_result(result)
    with open(file_path, 'wb') as f:
        f.write(b)
