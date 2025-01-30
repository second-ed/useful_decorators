from contextlib import nullcontext as does_not_raise

import pytest

import src.useful_decorators.pipeline.converters as conv


@pytest.mark.parametrize(
    "arg_type, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            int,
            "a",
            1.0,
            1,
            does_not_raise(),
            id="Ensure converts to int successfully",
        ),
        pytest.param(
            float,
            "a",
            1,
            1.0,
            does_not_raise(),
            id="Ensure converts to float successfully",
        ),
        pytest.param(
            str,
            "a",
            1,
            "1",
            does_not_raise(),
            id="Ensure converts to str successfully",
        ),
        pytest.param(
            list,
            "a",
            1,
            [1],
            does_not_raise(),
            id="Ensure converts to list successfully",
        ),
    ],
)
def test_to_type(arg_type, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        conv.to_type(arg_type)(arg_name, arg_value) == expected_result


@pytest.mark.parametrize(
    "arg_type, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            "default",
            "a",
            None,
            "default",
            does_not_raise(),
            id="Ensure converts to default successfully",
        ),
        pytest.param(
            "default",
            "a",
            "initial",
            "initial",
            does_not_raise(),
            id="Ensure retains initial value successfully",
        ),
    ],
)
def test_replace_none(arg_type, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        conv.replace_none(arg_type)(arg_name, arg_value) == expected_result


@pytest.mark.parametrize(
    "arg_type, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            0,
            "a",
            -1,
            0,
            does_not_raise(),
            id="Ensure clips to min successfully",
        ),
        pytest.param(
            0,
            "a",
            1,
            1,
            does_not_raise(),
            id="Ensure retains initial value successfully",
        ),
        pytest.param(
            0,
            "a",
            [-1],
            [-1],
            does_not_raise(),
            id="Ensure returns initial value if given uncastable type",
        ),
    ],
)
def test_clip_min(arg_type, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        conv.clip_min(arg_type)(arg_name, arg_value) == expected_result


@pytest.mark.parametrize(
    "arg_type, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            0,
            "a",
            1,
            0,
            does_not_raise(),
            id="Ensure clips to max successfully",
        ),
        pytest.param(
            0,
            "a",
            -1,
            -1,
            does_not_raise(),
            id="Ensure retains initial value successfully",
        ),
        pytest.param(
            0,
            "a",
            [1],
            [1],
            does_not_raise(),
            id="Ensure returns initial value if given uncastable type",
        ),
    ],
)
def test_clip_max(arg_type, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        conv.clip_max(arg_type)(arg_name, arg_value) == expected_result


@pytest.mark.parametrize(
    "arg_type, arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            "  ",
            "a",
            " ",
            "",
            does_not_raise(),
            id="Ensure strips whitespace successfully",
        ),
        pytest.param(
            " blah ",
            "a",
            " ",
            "blah",
            does_not_raise(),
            id="Ensure strips whitespace successfully",
        ),
        pytest.param(
            [1, 2, 3, 4],
            "a",
            "[]",
            "1, 2, 3, 4",
            does_not_raise(),
            id="Ensure casts to string and strips other character successfully",
        ),
    ],
)
def test_strip_chars(arg_type, arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        conv.strip_chars(arg_type)(arg_name, arg_value) == expected_result


@pytest.mark.parametrize(
    "arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            "a",
            "BLAH",
            "blah",
            does_not_raise(),
            id="Ensure strips whitespace successfully",
        ),
        pytest.param(
            "a",
            1,
            "1",
            does_not_raise(),
            id="Ensure strips whitespace successfully",
        ),
        pytest.param(
            "a",
            "Some_Thing_With_Punc!",
            "some_thing_with_punc!",
            does_not_raise(),
            id="Ensure casts to string and strips other character successfully",
        ),
    ],
)
def test_to_lower(arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        conv.to_lower()(arg_name, arg_value) == expected_result


@pytest.mark.parametrize(
    "arg_name, arg_value, expected_result, expected_context",
    [
        pytest.param(
            "a",
            "blah",
            "BLAH",
            does_not_raise(),
            id="Ensure strips whitespace successfully",
        ),
        pytest.param(
            "a",
            1,
            "1",
            does_not_raise(),
            id="Ensure strips whitespace successfully",
        ),
        pytest.param(
            "a",
            "Some_Thing_With_Punc!",
            "SOME_THING_WITH_PUNC!",
            does_not_raise(),
            id="Ensure casts to string and strips other character successfully",
        ),
    ],
)
def test_to_upper(arg_name, arg_value, expected_result, expected_context):
    with expected_context:
        conv.to_upper()(arg_name, arg_value) == expected_result
