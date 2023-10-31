from datetime import datetime, timedelta
import time


__all__ = ["datetime_now", "datetime_delta", "datetime_2_str", "datetime_2_timestamp",
           "str_delta_str", "str_2_datetime", "timestamp_2_str", "get_interval_days",
           "get_days"]
__auth__ = "baozilaji@gmail.com"


def datetime_now()->datetime:
    return datetime.now()


def datetime_delta(_date_time: datetime, _delta_hours: int=0)->datetime:
    return _date_time + timedelta(hours=_delta_hours)


def datetime_2_str(_date_time_base: datetime, _delta_hours: int, _fmt: str="%Y-%m-%d %H:%M:%S")->str:
    return datetime_delta(_date_time_base, _delta_hours).strftime(_fmt)


def datetime_2_timestamp(_datetime: datetime)->float:
    return datetime.timestamp(_datetime)


def str_delta_str(_str, _delta=0, _in_fmt="%Y-%m-%d %H:%M:%S", _out_fmt="%Y-%m-%d %H:%M:%S"):
    return (str_2_datetime(_str, _delta, _in_fmt)).strftime(_out_fmt)


def str_2_datetime(_str:str, _delta:int=0, _in_fmt:str="%Y-%m-%d %H:%M:%S")->datetime:
    return datetime_delta(datetime.strptime(_str, _in_fmt), _delta)


def timestamp_2_str(_timestamp, _fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(_timestamp).strftime(_fmt)


def get_interval_days(day1_sec:int, day2_sec:int):
    return abs(int((day2_sec - day1_sec) / 3600 / 24))

def get_days(ts_sec:int=int(time.time())):
    return get_interval_days(ts_sec, 0)

