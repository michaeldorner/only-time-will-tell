import os
import orjson
from datetime import datetime


def validate_file(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def validate_directory(string: str):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as json_file:
        raw_data = orjson.loads(json_file.read())
    return {k: {
        'start': datetime.fromisoformat(raw_data[k]['start']),
        'end': datetime.fromisoformat(raw_data[k]['end']),
        'participants': set(raw_data[k]['participants']),
    } for k in raw_data}


def decode_result(result: dict) -> bytes:
    def _default(obj):
        if isinstance(obj, set):
            return {o: None for o in sorted(obj)}
        raise TypeError
    return orjson.dumps(result, default=_default, option=orjson.OPT_SORT_KEYS)


def store_result(result: dict, out_dir: str, is_time_respecting: bool, postfix_name: str):
    file_name = {
        True: 'time_respecting_',
        False: 'time_ignoring_'
    }[is_time_respecting] + postfix_name

    with open(os.path.join(out_dir, file_name), 'wb') as f:
        f.write(decode_result(result))
