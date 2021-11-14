import orjson
from datetime import datetime
from pathlib import Path


def abs_dir_path(file):
    return Path(file).parent.absolute()


def validate_file(string):
    path = Path(string).absolute()
    if path.is_file():
        return path
    else:
        raise FileNotFoundError(string)


def validate_directory(string: str):
    path = Path(string).absolute()
    if path.is_dir():
        return path
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
    file_path = Path(out_dir) / file_name
    with open(file_path, 'wb') as f:
        f.write(decode_result(result))
