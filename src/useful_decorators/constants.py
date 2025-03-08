from enum import Enum


class PipeKey(Enum):
    FUNC = "func"
    ARGS = "args"
    KWARGS = "kwargs"
    RETURN = "return"
    EXCEPTIONS = "exceptions"
    START_TIME = "start_time"
    END_TIME = "end_time"


class ActionOnFail(Enum):
    CONTINUE = "continue"
    BREAK = "break"
