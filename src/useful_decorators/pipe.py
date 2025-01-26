import inspect
import pprint
from collections import defaultdict
from datetime import datetime, timezone
from functools import wraps

from .metaclasses import SingletonMeta
from .validators import InvalidArgs


class Pipe(metaclass=SingletonMeta):
    log = {}
    stage_count = 0

    @classmethod
    def stage(cls, arg_validations: dict = None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                curr_stage = cls.stage_count

                cls.log[curr_stage] = {
                    "func": func.__name__,
                    "args": args,
                    "kwargs": kwargs,
                    "exceptions": [],
                    "start_time": str(datetime.now(timezone.utc)),
                }

                if arg_validations:
                    fails = _validate_args(
                        arg_validations,
                        inspect.getfullargspec(func).args,
                        [*args, *list(kwargs.values())],
                    )

                    if fails:
                        invalid_args = InvalidArgs(dict(fails))
                        cls.log[curr_stage]["exceptions"].append(invalid_args)
                        pprint.pprint(cls.log, sort_dicts=False)
                        raise invalid_args

                try:
                    res = func(*args, **kwargs)
                except Exception as e:
                    cls.log[curr_stage]["exceptions"].append(e)

                cls.log[curr_stage]["end_time"] = str(datetime.now(timezone.utc))
                cls.log[curr_stage]["return"] = res

                if arg_validations and arg_validations.get("return", []):
                    fails = _validate_arg(arg_validations, "return", res)

                    if fails:
                        invalid_args = InvalidArgs({"return": fails})
                        cls.log[curr_stage]["exceptions"].append(invalid_args)
                        pprint.pprint(cls.log, sort_dicts=False)
                        raise invalid_args

                cls.stage_count += 1

                return res, cls.log[curr_stage]["exceptions"]

            return wrapper

        return decorator

    @classmethod
    def run(cls, stages, data):
        for stage in stages:
            data, errs = stage(data)

            if errs:
                print(cls.log)
                raise errs[-1]
        return True


def _validate_arg(arg_validations, arg_name, arg_value):
    fails = []
    for validation in arg_validations.get(arg_name, []):
        arg_validation = validation(arg_name, arg_value)
        if arg_validation is not None:
            fails.append(repr(arg_validation))
    return fails


def _validate_args(arg_validations: dict, arg_spec, arg_values):
    fails = defaultdict(list)
    for arg_name, arg_value in zip(arg_spec, arg_values):
        arg_fails = _validate_arg(arg_validations, arg_name, arg_value)
        if arg_fails:
            fails[arg_name] = arg_fails
    return fails
