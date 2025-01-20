import cProfile
import inspect
import pstats
from functools import wraps
from io import StringIO
from typing import Callable, Tuple, Union


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ExceptionLogger(metaclass=SingletonMeta):
    log = []

    @classmethod
    def catch_raise(
        cls,
        custom_exception: Exception = Exception,
        catch_exceptions: Union[Exception, Tuple[Exception]] = Exception,
        msg: str = "",
    ) -> Callable:
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    res = func(*args, **kwargs)
                    return res, None
                except catch_exceptions as e:
                    raise_exception = (
                        custom_exception
                        if custom_exception is not Exception
                        else type(e)
                    )
                    exc = raise_exception(
                        {
                            "func": func.__name__,
                            "args": args,
                            "kwargs": kwargs,
                            "caught_error": e,
                            "msg": msg or str(e),
                        }
                    )
                    cls.log.append(exc)
                    return None, exc

            return wrapper

        return decorator


def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print({"func": func.__name__, "args": args, "kwargs": kwargs, "return": res})
        return res

    return wrapper


def print_test_case(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        params = dict(zip(list(inspect.signature(func).parameters.keys()), args))
        params.update(**kwargs)
        res = func(*args, **kwargs)
        print(f"pytest.param({params}, {res}, id=''),")
        return res

    return wrapper


def profile_func(sort_by="cumulative"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            result = func(*args, **kwargs)
            profiler.disable()

            s = StringIO()
            ps = pstats.Stats(profiler, stream=s)
            ps.strip_dirs().sort_stats(sort_by).print_stats()
            print(s.getvalue())

            return result

        return wrapper

    return decorator
