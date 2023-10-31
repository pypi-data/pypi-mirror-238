from enum import Enum, unique


__all__ = ["GlobalRedisKey", "ObjectType", "RuntimeException", "GLOBAL_DEBUG", "GameErrorCode", "GameException"]
__auth__ = "baozilaji@gmail.com"


GLOBAL_DEBUG = False


class GlobalRedisKey(Enum):
    """
      redis key的父类，枚举类型，方便统一命名，避免冲突
    """
    pass


@unique
class ObjectType(Enum):
    REDIS = 0
    MONGO = 1
    BOTH = 2


class GameErrorCode(object):
    RECEIVE_INPUT_ERROR = -100000
    NO_MATCHED_METHOD_ERROR = -100001
    OTHER_EXCEPTION = -100002

class RuntimeException(Exception):
    """
      全局运行时异常
    """
    def __init__(self, name: str, msg: str):
        self.name = name
        self.msg = msg


class GameException(Exception):

    def __init__(self, state: int, msg: str):
        self.state = state
        self.msg = msg

    def __str__(self):
        return f"\"{self.state}, {self.msg}\""

    def __repr__(self):
        return self.__str__()
