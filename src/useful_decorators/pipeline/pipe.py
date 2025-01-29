import inspect
import pprint
from collections import defaultdict
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, List

from src.useful_decorators.metaclasses import SingletonMeta

from .constants import ActionOnFail, PipeKey
from .validators import InvalidArgs


# more simple decoupled implementation than the full Pipe class
def validate_args(arg_validations: dict, arg_conversions: dict):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            arg_dict = _create_arg_dict(inspect.getfullargspec(func), args, kwargs)

            if arg_conversions:
                arg_dict = _convert_args(arg_conversions, arg_dict)

            if arg_validations:
                fails = _validate_args(
                    arg_validations,
                    arg_dict,
                )

                if fails:
                    invalid_args = InvalidArgs(dict(fails))
                    raise invalid_args

            res = func(**arg_dict)

            if arg_validations and arg_validations.get("return", []):
                fails = _validate_arg(arg_validations, "return", res)

                if fails:
                    invalid_args = InvalidArgs({"return": fails})
                    raise invalid_args

            return res

        return wrapper

    return decorator


class Pipe(metaclass=SingletonMeta):
    log = {}
    stage_count = 0

    @classmethod
    def stage(
        cls,
        arg_validations: dict = None,
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

                if arg_validations:
                    fails = _validate_args(
                        arg_validations,
                        _create_arg_dict(inspect.getfullargspec(func), args, kwargs),
                    )

                    if fails:
                        invalid_args = InvalidArgs(dict(fails))
                        cls.log[curr_stage][PipeKey.EXCEPTIONS.value].append(
                            invalid_args
                        )
                        pprint.pprint(cls.log, sort_dicts=False)
                        raise invalid_args

                try:
                    # transform funcs return the transformed data for the next stage
                    # validation funcs return the data passed in + any validation errs
                    res, errs = func(*args, **kwargs)
                    if errs:
                        cls.log[curr_stage][PipeKey.EXCEPTIONS.value].append(*errs)
                except Exception as e:
                    cls.log[curr_stage][PipeKey.EXCEPTIONS.value].append(e)

                cls.log[curr_stage][PipeKey.END_TIME.value] = str(
                    datetime.now(timezone.utc)
                )
                cls.log[curr_stage][PipeKey.RETURN.value] = res

                if arg_validations and arg_validations.get(PipeKey.RETURN.value, []):
                    fails = _validate_arg(arg_validations, PipeKey.RETURN.value, res)

                    if fails:
                        invalid_args = InvalidArgs({PipeKey.RETURN.value: fails})
                        cls.log[curr_stage][PipeKey.EXCEPTIONS.value].append(
                            invalid_args
                        )
                        pprint.pprint(cls.log, sort_dicts=False)
                        raise invalid_args

                cls.stage_count += 1

                if action_on_fail == ActionOnFail.CONTINUE.value:
                    return res, []
                return res, cls.log[curr_stage][PipeKey.EXCEPTIONS.value]

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


def _convert_args(arg_conversions: Dict[str, List[Callable]], args_dict: dict):
    for arg_name, arg_value in args_dict.items():
        for conv in arg_conversions.get(arg_name, []):
            arg_value = conv(arg_name, arg_value)
        args_dict[arg_name] = arg_value
    return args_dict


def _validate_arg(
    arg_validations: Dict[str, List[Callable]], arg_name: str, arg_value: Any
):
    fails = []
    for validation in arg_validations.get(arg_name, []):
        arg_validation = validation(arg_name, arg_value)
        if arg_validation is not None:
            fails.append(repr(arg_validation))
    return fails


def _validate_args(arg_validations: Dict[str, List[Callable]], args_dict: dict):
    fails = defaultdict(list)
    for arg_name, arg_value in args_dict.items():
        arg_fails = _validate_arg(arg_validations, arg_name, arg_value)
        if arg_fails:
            fails[arg_name] = arg_fails
    return fails


def _create_arg_dict(arg_spec: inspect.FullArgSpec, args, kwargs):
    args = {i: arg for i, arg in enumerate(args)}
    arg_names = arg_spec.args
    defaults = arg_spec.defaults or ()

    num_non_defaults = len(arg_names) - len(defaults)
    default_values = dict(zip(arg_names[num_non_defaults:], defaults))
    arg_dict = {
        arg: args.get(i) or default_values.get(arg)
        for i, arg in enumerate(arg_names[: max(num_non_defaults, len(args))])
    }
    return {**arg_dict, **kwargs}
