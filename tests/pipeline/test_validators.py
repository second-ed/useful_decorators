from contextlib import nullcontext as does_not_raise

import pytest

from src.useful_decorators.pipeline import validators

NoneType = type(None)


@pytest.mark.parametrize(
    "arg_type, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            int,
            "a",
            1,
            NoneType,
            does_not_raise(),
            id="Ensure does not raise when `arg_type` is valid",
        ),
        pytest.param(
            (int, float),
            "a",
            1.0,
            NoneType,
            does_not_raise(),
            id="Ensure does not raise when `arg_type` is tuple containing a valid type",
        ),
        pytest.param(
            int,
            "a",
            1.0,
            TypeError,
            does_not_raise(),
            id="Ensure raises(TypeError) when `arg_type` is invalid",
        ),
    ],
)
def test_is_type(arg_type, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.is_type(arg_type)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "limit, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            1,
            "a",
            1,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is correct",
        ),
        pytest.param(
            1,
            "a",
            0,
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is incorrect",
        ),
    ],
)
def test_eq(limit, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.eq(limit)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "limit, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            1,
            "a",
            2,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is correct",
        ),
        pytest.param(
            1,
            "a",
            1,
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is incorrect",
        ),
        pytest.param(
            1,
            "a",
            "1",
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is wrong type",
        ),
    ],
)
def test_gt(limit, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.gt(limit)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "limit, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            1,
            "a",
            0,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is correct",
        ),
        pytest.param(
            1,
            "a",
            1,
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is incorrect",
        ),
        pytest.param(
            1,
            "a",
            "1",
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is wrong type",
        ),
    ],
)
def test_lt(limit, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.lt(limit)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "limit, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            1,
            "a",
            1,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is correct",
        ),
        pytest.param(
            1,
            "a",
            2,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is correct",
        ),
        pytest.param(
            1,
            "a",
            0,
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is incorrect",
        ),
        pytest.param(
            1,
            "a",
            "1",
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is wrong type",
        ),
    ],
)
def test_ge(limit, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.ge(limit)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "limit, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            1,
            "a",
            1,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is correct",
        ),
        pytest.param(
            1,
            "a",
            0,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is correct",
        ),
        pytest.param(
            1,
            "a",
            2,
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is incorrect",
        ),
        pytest.param(
            1,
            "a",
            "1",
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is wrong type",
        ),
    ],
)
def test_le(limit, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.le(limit)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "limit, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            3,
            "a",
            "000",
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is on limit",
        ),
        pytest.param(
            3,
            "a",
            "00",
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is below limit",
        ),
        pytest.param(
            3,
            "a",
            "0000",
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is above limit",
        ),
        pytest.param(
            3,
            "a",
            1,
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is wrong type",
        ),
    ],
)
def test_max_len(limit, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.max_len(limit)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "limit, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            3,
            "a",
            "000",
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is on limit",
        ),
        pytest.param(
            3,
            "a",
            "0000",
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is above limit",
        ),
        pytest.param(
            3,
            "a",
            "00",
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is above limit",
        ),
        pytest.param(
            3,
            "a",
            1,
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is wrong type",
        ),
    ],
)
def test_min_len(limit, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.min_len(limit)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "pattern, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            "[0-9]+",
            "a",
            "012345",
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `pattern` is valid",
        ),
        pytest.param(
            "[0-9]+",
            "a",
            "01234abc",
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is invalid",
        ),
        pytest.param(
            "[0-9]+",
            "a",
            1,
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is invalid",
        ),
    ],
)
def test_re_match(pattern, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.re_match(pattern)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "pattern, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            "[0-9]+",
            "a",
            "0123asfd45",
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `pattern` is valid",
        ),
        pytest.param(
            "[0-9]+",
            "a",
            "abc",
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is invalid",
        ),
        pytest.param(
            "[0-9]+",
            "a",
            1,
            TypeError,
            does_not_raise(),
            id="Ensure returns TypeError when `arg_value` is invalid",
        ),
    ],
)
def test_re_search(pattern, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.re_search(pattern)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "valid_values, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            [0, 1, 2],
            "a",
            1,
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is valid",
        ),
        pytest.param(
            [0, 1, 2],
            "a",
            3,
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is invalid",
        ),
    ],
)
def test_is_in(valid_values, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        res = validators.is_in(valid_values)(arg_name, arg_value)
        assert isinstance(res, expected_result)


@pytest.mark.parametrize(
    "required_values, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            [2],
            "a",
            [1, 2, 3],
            NoneType,
            does_not_raise(),
            id="Ensure returns None when `arg_value` is valid",
        ),
        pytest.param(
            [4],
            "a",
            [1, 2, 3],
            ValueError,
            does_not_raise(),
            id="Ensure returns ValueError when `arg_value` is invalid",
        ),
    ],
)
def test_contains(
    required_values, arg_name, arg_value, expected_result, expected_context
):
    with expected_context:
        res = validators.contains(required_values)(arg_name, arg_value)
        assert isinstance(res, expected_result)
