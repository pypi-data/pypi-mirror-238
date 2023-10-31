# pg common

python game common lib

## desc

```shell script
date.py
utils for datetime

func.py
basic functons

singleton.py
defination of singleton class.
```

## usage
date.py
```shell script
from pg_common import date
from pg_common import func
func.log_print("INFO", date.datetime_now())

func.log_print("WARN", date.str_delta_str("2023/03/01", _delta=3*24, _in_fmt="%Y/%m/%d", _out_fmt="%Y-%m-%d"))
```

func.py
```shell script
from pg_common import func
A = {"A": 1}
func.merge_dict(A, {"B": 2})
func.log_print("INFO", A)


func.log_print("INFO", func.rand_str(10))
func.log_print("INFO", func.rand_num(4))

func.log_print("INFO", func.json_pretty({"A": 1, "B": [1,2,3]}))

func.log_info(func.is_valid_ip("0.0.0.0"))
func.log_info(func.is_valid_ip("0.0.0."))
```

singleton.py
```shell script
from pg_common import singleton

class A(singleton.SingletonBase):
    pass

A() == A()
```