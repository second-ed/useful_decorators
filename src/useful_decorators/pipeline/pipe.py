from datetime import datetime, timezone
from functools import wraps

from src.useful_decorators.metaclasses import SingletonMeta

from .constants import ActionOnFail, PipeKey


class Pipe(metaclass=SingletonMeta):
    log = {}
    stage_count = 0

    @classmethod
    def stage(
        cls,
        action_on_fail: str = ActionOnFail.BREAK.value,
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                curr_stage = cls.stage_count

                cls.log[curr_stage] = {
                    PipeKey.FUNC.value: func.__name__,
                    PipeKey.ARGS.value: args,
                    PipeKey.KWARGS.value: kwargs,
                    PipeKey.EXCEPTIONS.value: [],
                    PipeKey.START_TIME.value: str(datetime.now(timezone.utc)),
                }

                try:
                    res = func(*args, **kwargs)
                    cls.log[curr_stage][PipeKey.RETURN.value] = res
                except Exception as e:
                    cls.log[curr_stage][PipeKey.EXCEPTIONS.value].append(e)

                cls.log[curr_stage][PipeKey.END_TIME.value] = str(
                    datetime.now(timezone.utc)
                )
                cls.stage_count += 1

                if (
                    action_on_fail == ActionOnFail.CONTINUE.value
                    or not cls.log[curr_stage][PipeKey.EXCEPTIONS.value]
                ):
                    return res
                raise cls.log[curr_stage][PipeKey.EXCEPTIONS.value][-1]

            return wrapper

        return decorator

    @classmethod
    def run(cls, stages, data):
        for stage in stages:
            data = stage(data)

        return data
