import inspect
from collections import defaultdict
from functools import wraps
from typing import Any, Callable, Dict, List

from .validators import InvalidArgs


# more simple decoupled implementation than the full Pipe class
def validate_args(validations: dict = None, conversions: dict = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            arg_dict = _create_arg_dict(inspect.getfullargspec(func), args, kwargs)

            if conversions:
                arg_dict = _convert_args(conversions, arg_dict)

            if validations:
                fails = _validate_args(
                    validations,
                    arg_dict,
                )

                if fails:
                    invalid_args = InvalidArgs(dict(fails))
                    raise invalid_args

            res = func(**arg_dict)

            if validations and validations.get("return", []):
                fails = _validate_arg(validations, "return", res)

                if fails:
                    invalid_args = InvalidArgs({"return": fails})
                    raise invalid_args

            return res

        return wrapper

    return decorator


def _convert_args(conversions: Dict[str, List[Callable]], args_dict: dict):
    for arg_name, arg_value in args_dict.items():
        for conv in conversions.get(arg_name, []):
            arg_value = conv(arg_name, arg_value)
        args_dict[arg_name] = arg_value
    return args_dict


def _validate_arg(
    validations: Dict[str, List[Callable]], arg_name: str, arg_value: Any
):
    fails = []
    for validation in validations.get(arg_name, []):
        arg_validation = validation(arg_name, arg_value)
        if arg_validation is not None:
            fails.append(repr(arg_validation))
    return fails


def _validate_args(validations: Dict[str, List[Callable]], args_dict: dict):
    fails = defaultdict(list)
    for arg_name, arg_value in args_dict.items():
        arg_fails = _validate_arg(validations, arg_name, arg_value)
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
    return {**default_values, **arg_dict, **kwargs}
