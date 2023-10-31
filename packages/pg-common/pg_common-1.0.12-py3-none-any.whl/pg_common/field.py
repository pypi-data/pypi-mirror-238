from enum import Enum, unique
from abc import ABC, abstractmethod
from pg_common.date import datetime_now
from pg_common import GLOBAL_DEBUG, RuntimeException
import datetime
import copy

__all__ = [
           "FieldBase", "FieldType",
           "BooleanField", "IntField", "FloatField", "StringField", "DatetimeField",
           "ListField", "SetField", "DictField", "ObjectField"
           ]
__auth__ = "baozilaji@gmail.com"


_DEBUG = False


@unique
class FieldType(Enum):
    BOOLEAN = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    DATETIME = 5
    LIST = 6
    SET = 7
    DICT = 8
    OBJECT = 9


class FieldBase(ABC, object):

    def __init__(self,
                 _type,
                 _default,
                 _name,
                 primary_key=False):
        self.name = _name
        self.type = _type
        self.value = _default
        self.primary_key = primary_key
        if GLOBAL_DEBUG and _DEBUG:
            if not isinstance(self.type, FieldType):
                raise RuntimeException("Init Field", "field type must be FieldType.")
            if not self.name:
                raise RuntimeException("Init Field", "field name must be defined.")
            if not self.check(self.value):
                raise RuntimeException(f"Init {self.name}", f"error value type: {type(self.value)}, needs: {self.type}")

    @abstractmethod
    def check(self, val):
        pass

    def dump(self):
        return copy.deepcopy(self.value)


class BooleanField(FieldBase):

    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.BOOLEAN, kwargs.pop("default", False), _name, **kwargs)

    def check(self, value):
        return type(value) == bool


class IntField(FieldBase):

    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.INT, kwargs.pop("default", 0), _name, **kwargs)

    def check(self, value):
        return type(value) == int


class FloatField(FieldBase):

    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.FLOAT, kwargs.pop("default", 0.0), _name, **kwargs)

    def check(self, value):
        return type(value) == float


class StringField(FieldBase):

    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.STRING, kwargs.pop("default", ""), _name, **kwargs)

    def check(self, value):
        return type(value) == str


class DatetimeField(FieldBase):

    def __init__(self, _name, fmt="%Y-%m-%d %H:%M:%S", **kwargs):
        self.fmt = fmt
        FieldBase.__init__(self, FieldType.DATETIME, kwargs.pop("default", datetime_now()), _name, **kwargs)

    def check(self, value):
        return type(value) == datetime.datetime


class ListField(FieldBase):

    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.LIST, kwargs.pop("default", list()), _name, **kwargs)

    def check(self, value):
        return type(value) == list


class SetField(FieldBase):

    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.SET, kwargs.pop("default", set()), _name, **kwargs)

    def check(self, value):
        return type(value) == set


class DictField(FieldBase):

    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.DICT, kwargs.pop("default", dict()), _name, **kwargs)

    def check(self, value):
        return type(value) == dict


class ObjectField(FieldBase):
    def __init__(self, _name, **kwargs):
        FieldBase.__init__(self, FieldType.OBJECT, kwargs.pop("default", None), _name, **kwargs)

    def check(self, value):
        if not callable(value):
            return False
        from pg_common import ObjectBase
        return issubclass(value, ObjectBase)

    def dump(self):
        return self.value()
