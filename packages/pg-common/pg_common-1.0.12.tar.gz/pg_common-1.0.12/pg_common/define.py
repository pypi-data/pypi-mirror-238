from typing import Dict, Union, Tuple, Optional
from pg_common import datetime_now, datetime_2_timestamp, DictValType
from pydantic import BaseModel


__all__ = [
    "Container", "FieldContainer",
    "RequestMap", "RequestHeader", "RequestData",
    "ResponseMap", "ResponseHeader", "ResponseData",
]
__auth__ = "baozilaji@gmail.com"



class FieldContainer(object):
    def __init__(self):
        self._content: dict[str, set[str]] = {}

    def add(self, obj:str, field: str):
        if obj not in self._content:
            self._content[obj] = set()
        self._content[obj].add(field)

    def add_many(self, obj: str, fields: Union[set[str], list[str], Tuple[str]]):
        if obj not in self._content:
            self._content[obj] = set()
        self._content[obj].update(fields)

    def __str__(self):
        return str(self._content)


class ResponseMap(BaseModel):
    method: str = ""
    retCode: int = 0


class ResponseHeader(BaseModel):
    datas: list[ResponseMap] = []
    retCode: int = 0 # 错误码
    st: int = 0 # 自增计数
    token: str = "" # 单点登陆的token
    ts: int = int(datetime_2_timestamp(datetime_now())) # 时间（秒）
    offSt: int = 0 # 离线请求自增计数
    msg: str = "" # 消息


class ResponseData(BaseModel):
    head: ResponseHeader
    body: dict


class RequestMap(BaseModel):
    method: str = ""
    data: str = ""
    param: dict = {}


class RequestHeader(BaseModel):
    datas: list[RequestMap] = []
    method: str = ""
    uid: int = 0
    v: int = 0 # 客户端版本号
    mv: int = 0 # meta版本号
    ct: int = 0 # 客户端类型, 1: ios, 2: android, 3: wp
    uuid: str = "" # session key
    st: int = 0 # 自增计数
    channel: str = "" # 区分不同包
    lang: str = "" # 语言
    token: str = "" # 单点登陆的token
    offSt: int = 0 # 离线请求自增计数
    rv: int = 0 # res版本号
    extra: str = "" # 额外数据，如network环境等
    pj: str = "" # 项目名称


class RequestData(BaseModel):
    head: RequestHeader
    body: dict


class Container(BaseModel):
    log: dict[str, DictValType] = {}
    req: Optional[RequestData]
    resp: Optional[ResponseData]