import asyncio
from pg_common.date import datetime_now
import random
import json
from datetime import date, datetime
import re
import prettytable as pt


_STR_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
_NUM_CHARS = "0123456789"
_IP_PATTERN = r'^(\d{1,3}\.){3}\d{1,3}$'


__all__ = ["merge_dict", "log_print", "start_coroutines", "rand_str", "rand_num",
           "log_debug", "log_error", "log_info", "log_warn",
           "is_valid_ip", 'clear_none',
           "ComplexEncoder", "json_pretty", "json_prettytable"]
__auth__ = "baozilaji@gmail.com"


def is_valid_ip(ip):
    return re.match(_IP_PATTERN, ip) is not None


def _random(_len: int = 6, _type: int = 0):
    _ret = ""
    _chars = _STR_CHARS if _type == 0 else _NUM_CHARS
    _len_total = len(_chars)
    for i in range(_len):
        _ret += _chars[random.randint(0, _len_total-1)]
    return _ret


def rand_str(_len: int = 6):
    return _random(_len)


def rand_num(_len: int = 4):
    return int(_random(_len, _type=1))


def merge_dict(_to, _from):
    if isinstance(_to, dict) and isinstance(_from, dict):
        for _key, _value in _to.items():
            if _key in _from:
                _fv = _from[_key]
                if type(_value) == type(_fv):
                    if type(_value) == dict:
                        merge_dict(_value, _fv)
                    else:
                        _to[_key] = _fv
        for _key in _from:
            if _key not in _to:
                _to[_key] = _from[_key]


def clear_none(obj):
    if isinstance(obj, list):
        return [clear_none(o) for o in obj if o is not None]
    elif isinstance(obj, dict):
        return {k: clear_none(v) for k, v in obj.items() if v is not None}
    return obj


def log_print(tag, msg):
    print(f"{datetime_now()} - {tag} - {msg}")


def log_info(msg):
    log_print("INFO", msg)


def log_error(msg):
    log_print("ERROR", msg)


def log_warn(msg):
    log_print("WARN", msg)


def log_debug(msg):
    log_print("DEBUG", msg)


def start_coroutines(_all_coroutines):
    if _all_coroutines:
        _temp = None
        if isinstance(_all_coroutines, list):
            _temp = _all_coroutines
        else:
            _temp = [_all_coroutines]

        for _c in _temp:
            if asyncio.iscoroutinefunction(_c):
                _c = _c()

            if not asyncio.iscoroutine(_c):
                raise ValueError(f"parameter must be coroutine instance, now is {type(_c)}")

            asyncio.create_task(_c)


class ComplexEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        else:
            return super().default(o)


def json_pretty(json_obj: dict):
    return json.dumps(json_obj, indent=2, cls=ComplexEncoder)


def json_prettytable(json_obj):
    tb = pt.PrettyTable()
    if json_obj:
        if isinstance(json_obj, dict):
            tb.field_names = json_obj.keys()
            tb.add_row(json_obj.values())
        elif isinstance(json_obj, list):
            if isinstance(json_obj[0], dict):
                tb.field_names = json_obj[0].keys()
                for _val in json_obj:
                    tb.add_row(_val.values())
    return tb
