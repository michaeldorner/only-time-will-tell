from pathlib import Path

import orjson


def decode_result(result: dict) -> bytes:
    def _default(obj):
        if isinstance(obj, set):
            return {o: None for o in sorted(obj)}
        raise TypeError
    return orjson.dumps(result, default=_default, option=orjson.OPT_SORT_KEYS)  # pylint: disable=maybe-no-member


def to_json(result, file_name):
    file_path = Path('results') / file_name
    with open(file_path, 'wb') as file:
        file.write(decode_result(result))
