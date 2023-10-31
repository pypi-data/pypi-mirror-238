# -*- encoding: utf-8 -*-
from pg_common.field import FieldBase, FieldType
from pg_common.conf import GlobalRedisKey, RuntimeException, ObjectType, GLOBAL_DEBUG
from pg_common import log_info, datetime_2_str, str_2_datetime
import json

__all__ = ["ObjectBase"]
__auth__ = "baozilaji@gmail.com"

_DEBUG = False
_PRINT = False

__KEY_ORM__ = "__key_orm__"
__KEY_PRIMARY_KEY__ = "__key_primary_key__"
__KEY_REDIS_KEY__ = "__redis_key__"
__KEY_OBJ_TYPE__ = "__obj_type__"
__KEY_VALUES__ = "__key_values__"
__SELF_FIELDS__ = set([__KEY_VALUES__])


class ObjectBaseMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        if name == "ObjectBase":
            return type.__new__(mcs, name, bases, attrs)
        else:
            if __KEY_OBJ_TYPE__ in attrs and not isinstance(attrs[__KEY_OBJ_TYPE__], ObjectType):
                raise RuntimeException("ObjectInitialize",
                                       f"Object: {name} attribute __obj_type__ must be ObjectType.")

                _obj_type = attrs[__KEY_OBJ_TYPE__]
                if _obj_type == ObjectType.REDIS or _obj_type == ObjectType.BOTH:

                    if __KEY_REDIS_KEY__ not in attrs or not isinstance(attrs[__KEY_REDIS_KEY__], GlobalRedisKey):
                        raise RuntimeException("ObjectInitialize",
                                               "Object: %s must define __redis_key__ attribute as GlobalRedisKey." % (
                                                   name,))

            __orm__ = dict()
            __primary_key__ = []
            for _k, _v in attrs.items():
                if isinstance(_v, FieldBase):
                    __orm__[_k] = _v

                    if _v.primary_key:
                        __primary_key__.append(_k)

            for _k in __orm__.keys():
                attrs.pop(_k)

            attrs[__KEY_ORM__] = __orm__
            attrs[__KEY_PRIMARY_KEY__] = __primary_key__

            return type.__new__(mcs, name, bases, attrs)


class ObjectBase(object, metaclass=ObjectBaseMetaclass):
    def __init__(self):
        __orm__ = getattr(self, __KEY_ORM__)
        _values = {}
        for _k, _f in __orm__.items():
            _values[_k] = _f.dump()
        self[__KEY_VALUES__] = _values

    def __setattr__(self, key, value):
        __orm__ = getattr(self, __KEY_ORM__)

        if key not in __SELF_FIELDS__ and (not __orm__ or key not in __orm__):
            raise RuntimeException("setValue", f"attribute {key} not defined")

        if key not in __SELF_FIELDS__:
            if GLOBAL_DEBUG and _DEBUG:
                _field = __orm__[key]
                if not _field.check(value):
                    raise RuntimeException("setValue", f"key: {key}, "
                                                       f"value type error: {type(value)}, needs: {_field.type}")
            self[__KEY_VALUES__][key] = value
        else:
            self.__dict__[key] = value

        if _PRINT or (GLOBAL_DEBUG and _DEBUG):
            log_info(f"__setattr__ {key}: {value}")

    def __getattr__(self, item):
        _value = None
        if item not in __SELF_FIELDS__:
            if GLOBAL_DEBUG and _DEBUG:
                __orm__ = getattr(self, __KEY_ORM__)
                if not __orm__ or item not in __orm__:
                    raise RuntimeException("getValue", f"attribute {item} not defined")
            _value = self[__KEY_VALUES__][item]
        else:
            _value = self.__dict__[item]

        if _PRINT or (GLOBAL_DEBUG and _DEBUG):
            log_info(f"__getattr__ {item}: {_value}")
        return _value

    def __getattribute__(self, item):
        _value = object.__getattribute__(self, item)
        if _PRINT or (GLOBAL_DEBUG and _DEBUG):
            log_info(f"__getattribute__ {item}: {_value}")
        return _value

    def __setitem__(self, key, value):
        ObjectBase.__setattr__(self, key, value)

    def __getitem__(self, item):
        _value = ObjectBase.__getattr__(self, item)
        return _value

    def get_redis_key(self):
        _pk = getattr(self, __KEY_PRIMARY_KEY__)
        if len(_pk) == 0:
            raise RuntimeException("genRedisKey", f"Object {self.__name__} do not have primary key defined.")

        _k_val = [str(self[__KEY_VALUES__][_k]) for _k in _pk]

        return "%s%s" % (getattr(self, __KEY_REDIS_KEY__).value,
                         "#".join(_k_val))

    def save(self, fields=None, save_all=False):
        _changed = set([])
        _keys = set(getattr(self, __KEY_PRIMARY_KEY__))
        if not save_all:
            if fields:
                if isinstance(fields, (tuple, list, set)):
                    _changed = set(fields)
                elif isinstance(fields, str):
                    _changed.add(fields)

        _out = {}
        _orm = getattr(self, __KEY_ORM__)
        for _f_name, _f_obj in _orm.items():
            _c = True if save_all else False
            if _f_name in _changed:
                _c = True
            if _c and _f_name not in _keys:
                if _f_obj.type == FieldType.LIST or _f_obj.type == FieldType.DICT:
                    _out[_f_name] = json.dumps(self[__KEY_VALUES__][_f_name])
                elif _f_obj.type == FieldType.SET:
                    _out[_f_name] = json.dumps(list(self[__KEY_VALUES__][_f_name]))
                elif _f_obj.type == FieldType.DATETIME:
                    _out[_f_name] = datetime_2_str(self[__KEY_VALUES__][_f_name], 0, _fmt=_f_obj.fmt)
                elif _f_obj.type == FieldType.OBJECT:
                    _o = self[__KEY_VALUES__][_f_name].save(save_all=save_all)
                    _out[_f_name] = json.dumps(_o)
                else:
                    _out[_f_name] = self[__KEY_VALUES__][_f_name]
        return _out

    def load(self, data):
        if isinstance(data, dict):
            _orm = getattr(self, __KEY_ORM__)
            for _k, _f in _orm.items():
                if _f.primary_key:
                    continue
                if _f.type == FieldType.LIST or _f.type == FieldType.DICT:
                    self[__KEY_VALUES__][_k] = json.loads(data[_k])
                elif _f.type == FieldType.SET:
                    self[__KEY_VALUES__][_k] = set(json.loads(data[_k]))
                elif _f.type == FieldType.DATETIME:
                    self[__KEY_VALUES__][_k] = str_2_datetime(data[_k], _in_fmt=_f.fmt)
                elif _f.type == FieldType.OBJECT:
                    _j = json.loads(data[_k])
                    self[__KEY_VALUES__][_k].load(_j)
                else:
                    self[__KEY_VALUES__][_k] = data[_k]


if __name__ == "__main__":
    pass
