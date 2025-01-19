import pytest

from src.useful_decorators.decorators import debug, print_test_case


@pytest.mark.parametrize(
    "args, kwargs, expected_result",
    [
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
    ],
)
def test_debug(capsys, args, kwargs, expected_result):
    @debug
    def some_func(a, b):
        return a + b

    some_func(*args, **kwargs)
    captured = capsys.readouterr()
    assert captured.out == expected_result


@pytest.mark.parametrize(
    "args, kwargs, expected_result",
    [
        pytest.param(
            (2, 3),
            {},
            "pytest.param({'a': 2, 'b': 3}, 5, id=''),\n",
            id="Ensure prints test case with args",
        ),
        pytest.param(
            (3,),
            {"b": 4},
            "pytest.param({'a': 3, 'b': 4}, 7, id=''),\n",
            id="Ensure prints test case with args and kwargs",
        ),
    ],
)
def test_print_test_case(capsys, args, kwargs, expected_result):
    @print_test_case
    def some_func(a, b):
        return a + b

    some_func(*args, **kwargs)
    captured = capsys.readouterr()
    assert captured.out == expected_result
