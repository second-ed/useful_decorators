import cProfile
import inspect
import pstats
from functools import wraps
from io import StringIO


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
