import typing
from pg_common import SingletonBase, log_info
import os
import importlib

__all__ = [
           "func_decorator", "FuncDecoratorManager",
           ]
__auth__ = "baozilaji@gmail.com"


class _FuncDecoratorManager(SingletonBase):
    def __init__(self):
        self._handlers: dict[str, typing.Callable] = {}

    def register(self, method: str, handler: typing.Callable):
        self._handlers[method] = handler
        log_info(f"register handler: {method}")

    def get_func(self, method: str) -> typing.Callable:
        return self._handlers[method]

    @staticmethod
    def scan_decorators(director):
        _handler_dir = director
        log_info(f"handler dirs: {_handler_dir}")

        for _root, _dirs, _files in os.walk(_handler_dir):
            for _file in _files:
                if _file.endswith(".py"):
                    _module_name = _root.replace("/", ".")
                    _module_name = f"{_module_name}.{_file[:-3]}"
                    _module = importlib.import_module(_module_name)
                    log_info(f"load handler {_module_name}")


FuncDecoratorManager = _FuncDecoratorManager()


def func_decorator(func_key: str) -> typing.Callable:
    def decorator(func: typing.Callable) -> typing.Callable:
        FuncDecoratorManager.register(func_key, func)
    return decorator
