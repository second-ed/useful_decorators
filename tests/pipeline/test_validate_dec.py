import inspect
from contextlib import nullcontext as does_not_raise

import pytest

import src.useful_decorators.pipeline.converters as con
import src.useful_decorators.pipeline.validators as val
from src.useful_decorators.pipeline.validate_dec import (
    _create_arg_dict,
    validate_args,
)


@pytest.mark.parametrize(
    "validations, conversions, args, kwargs, expected_result, expected_context",
    [
        (
            {},
            {},
            (1, 2, True, "test"),
            {},
            3,
            does_not_raise(),
        ),
        (
            {"a": [val.is_type(int)], "return": [val.is_type(str)]},
            {"a": [con.to_type(int)], "c": [con.to_type(bool)]},
            (1.0, 2, 0),
            {"d": "test"},
            "-1_test",
            does_not_raise(),
        ),
        (
            {"a": [val.is_type(int)]},
            {"c": [con.to_type(bool)]},
            (1.0, 2, 0, "test"),
            {},
            None,
            pytest.raises(val.InvalidArgs),
        ),
        (
            {"a": [val.is_type(int), val.gt(0)], "return": [val.lt(1)]},
            {"c": [con.to_type(bool)]},
            (1, 2, 1, "test"),
            {},
            None,
            pytest.raises(val.InvalidArgs),
        ),
    ],
)
def test_validate_args(
    validations, conversions, args, kwargs, expected_result, expected_context
):
    with expected_context:

        @validate_args(
            validations=validations,
            conversions=conversions,
        )
        def some_func(a: int, b: float, c: bool, d: str):
            if c:
                return a + b
            return f"{a - b}_{d}"

        assert some_func(*args, **kwargs) == expected_result


@pytest.fixture
def get_mock_argspec():
    return inspect.FullArgSpec(
        args=["a", "b", "c", "d"],
        varargs=None,
        varkw=None,
        defaults=(3, True),
        kwonlyargs=[],
        kwonlydefaults=None,
        annotations={"return": int},
    )


@pytest.mark.parametrize(
    "argspec_fixt_name, args, kwargs, expected_result, expected_context",
    [
        (
            "get_mock_argspec",
            (1,),
            {"b": 2, "d": False},
            {"a": 1, "b": 2, "c": 3, "d": False},
            does_not_raise(),
        ),
        (
            "get_mock_argspec",
            (1, 2),
            {},
            {"a": 1, "b": 2, "c": 3, "d": True},
            does_not_raise(),
        ),
    ],
)
def test_create_arg_dict(
    request, argspec_fixt_name, args, kwargs, expected_result, expected_context
):
    with expected_context:
        argspec = request.getfixturevalue(argspec_fixt_name)
        assert _create_arg_dict(argspec, args, kwargs) == expected_result
