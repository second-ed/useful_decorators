from contextlib import nullcontext as does_not_raise

import pytest

from src.useful_decorators.decorators import ExceptionLogger, debug, print_test_case


@pytest.mark.parametrize(
    "args, custom_exception, catch_exceptions, msg, expected_result, expected_context",
    (
        pytest.param(
            (2, "0"),
            ValueError,
            Exception,
            "no string args allowed",
            (
                None,
                ValueError(
                    {
                        "func": "div",
                        "args": (2, "0"),
                        "kwargs": {},
                        "caught_error": TypeError(
                            "unsupported operand type(s) for /: 'int' and 'str'"
                        ),
                        "msg": "no string args allowed",
                    }
                ),
            ),
            does_not_raise(),
            id="Ensure catches and transforms exception",
        ),
        pytest.param(
            (2, 1),
            ValueError,
            ZeroDivisionError,
            "no string args allowed",
            (2, None),
            does_not_raise(),
            id="Ensure catches and transforms exception",
        ),
    ),
)
def test_catch_raise(
    args, custom_exception, catch_exceptions, msg, expected_result, expected_context
):
    @ExceptionLogger.catch_raise(custom_exception, catch_exceptions, msg)
    def div(a, b):
        return a / b

    with expected_context:
        res, err = div(*args)
        exp_res, exp_err = expected_result

        assert res == exp_res

        if err and exp_err:
            assert str(err.args[0]) == str(exp_err.args[0])


@pytest.mark.parametrize(
    "args, kwargs, expected_result",
    (
        pytest.param(
            (2, 3),
            {},
            "{'func': 'some_func', 'args': (2, 3), 'kwargs': {}, 'return': 5}\n",
            id="Ensure prints debug with args",
        ),
        pytest.param(
            (3,),
            {"b": 4},
            "{'func': 'some_func', 'args': (3,), 'kwargs': {'b': 4}, 'return': 7}\n",
            id="Ensure prints debug with args and kwargs",
        ),
    ),
)
def test_debug(capsys, args, kwargs, expected_result):
    @debug
    def some_func(a, b):
        return a + b

    some_func(*args, **kwargs)
    captured = capsys.readouterr()
    assert captured.out == expected_result


@pytest.mark.parametrize(
    "kwargs, expected_result",
    (
        pytest.param(
            {"a": 2, "b": 3},
            "pytest.param({'a': 2, 'b': 3}, 5, id=''),\n",
            id="Ensure prints test case with args",
        ),
        pytest.param(
            {"a": 3, "b": 4},
            "pytest.param({'a': 3, 'b': 4}, 7, id=''),\n",
            id="Ensure prints test case with args and kwargs",
        ),
    ),
)
def test_print_test_case(capsys, kwargs, expected_result):
    @print_test_case
    def some_func(a, b):
        return a + b

    some_func(**kwargs)
    captured = capsys.readouterr()
    assert captured.out == expected_result
