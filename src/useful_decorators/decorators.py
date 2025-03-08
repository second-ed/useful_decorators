from __future__ import annotations

import cProfile
import inspect
import pstats
import threading
from functools import wraps
from io import StringIO
from typing import Any, Callable

from useful_decorators.metaclasses import SingletonMeta  # type ignore[import-untyped]


class ExceptionLogger(metaclass=SingletonMeta):
    _log_lock = threading.Lock()
    log: list[Exception] = []

    @classmethod
    def catch_raise(
        cls,
        custom_exception: Exception = Exception,  # type: ignore[assignment]
        catch_exceptions: Exception | tuple[Exception] = Exception,  # type: ignore[assignment]
        msg: str = "",
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
                try:
                    res = func(*args, **kwargs)
                    return res, None
                except catch_exceptions as e:  # type: ignore[misc]
                    raise_exception = (
                        custom_exception
                        if custom_exception is not Exception
                        else type(e)
                    )
                    exc = raise_exception(  # type: ignore[operator]
                        {
                            "func": func.__name__,
                            "args": args,
                            "kwargs": kwargs,
                            "caught_error": e,
                            "msg": msg or str(e),
                        }
                    )
                    with cls._log_lock:
                        cls.log.append(exc)
                    return None, exc

            return wrapper

        return decorator


def debug(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
        res = func(*args, **kwargs)
        print({"func": func.__name__, "args": args, "kwargs": kwargs, "return": res})
        return res

    return wrapper


def print_test_case(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
        params = dict(zip(list(inspect.signature(func).parameters.keys()), args))
        params.update(**kwargs)
        res = func(*args, **kwargs)
        print(f"pytest.param({params}, {res}, id=''),")
        return res

    return wrapper


def profile_func(sort_by: str = "cumulative") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
            profiler = cProfile.Profile()
            profiler.enable()
            res = func(*args, **kwargs)
            profiler.disable()

            s = StringIO()
            ps = pstats.Stats(profiler, stream=s)
            ps.strip_dirs().sort_stats(sort_by).print_stats()
            print(s.getvalue())

            return res

        return wrapper

    return decorator
