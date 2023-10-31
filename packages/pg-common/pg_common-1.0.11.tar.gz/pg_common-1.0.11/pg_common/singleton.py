__all__ = ["SingletonMetaclass", "SingletonBase"]
__auth__ = "baozilaji@gmail.com"


class SingletonMetaclass(type):

    def __init__(cls, *args, **kwargs):
        cls.__instance__ = None
        super(SingletonMetaclass, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
        return cls.__instance__


class SingletonBase(metaclass=SingletonMetaclass):
    ...
