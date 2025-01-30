import inspect
import pprint
from datetime import datetime, timezone
from functools import wraps

from src.useful_decorators.metaclasses import SingletonMeta

from .constants import ActionOnFail, PipeKey
from .validate_dec import _create_arg_dict, _validate_arg, _validate_args
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
