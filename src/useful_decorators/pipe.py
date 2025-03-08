from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Iterable, Type, TypeVar

from useful_decorators.constants import (
    ActionOnFail,
    PipeKey,
)  # type ignore[import-untyped]
from useful_decorators.metaclasses import SingletonMeta  # type ignore[import-untyped]

T = TypeVar("T")


class Pipe(metaclass=SingletonMeta):
    log: dict = {}
    stage_count = 0

    @classmethod
    def stage(
        cls,
        action_on_fail: str = ActionOnFail.BREAK.value,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
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
    def run(cls, stages: Iterable[Callable], data: Type[T]) -> Type[T]:
        for stage in stages:
            data = stage(data)

        return data
