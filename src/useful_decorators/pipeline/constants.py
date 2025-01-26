from enum import StrEnum, auto


class PipeKey(StrEnum):
    FUNC = auto()
    ARGS = auto()
    KWARGS = auto()
    RETURN = auto()
    EXCEPTIONS = auto()
    START_TIME = auto()
    END_TIME = auto()


class ActionOnFail(StrEnum):
    CONTINUE = auto()
    BREAK = auto()
