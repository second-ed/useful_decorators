import inspect
import pprint
from collections import defaultdict
from datetime import datetime, timezone
from functools import wraps

from .constants import ActionOnFail, PipeKey
from .metaclasses import SingletonMeta
from .validators import InvalidArgs


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
                        inspect.getfullargspec(func).args,
                        [*args, *list(kwargs.values())],
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
