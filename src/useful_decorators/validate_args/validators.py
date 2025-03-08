import json
import re
from functools import wraps
from typing import Any, Callable, Iterable


class InvalidArgs(Exception):
    def __init__(self, fails: dict | list) -> None:
        self.fails = fails

    def __str__(self) -> str:
        return json.dumps(self.fails, indent=4, sort_keys=False)


def catch_type_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(arg_name: str, arg_value: Any) -> Any | TypeError:
        try:
            return func(arg_name, arg_value)
        except TypeError as e:
            return e

    return wrapper


def is_type(arg_type: type) -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> TypeError | None:
        if not isinstance(arg_value, arg_type):
            return TypeError(
                f"`{arg_name}` must be type {arg_type}. Got: {type(arg_value)}"
            )
        return None

    return wrapper


def eq(value: int) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not arg_value == value:
            return ValueError(f"`{arg_name}` must equal {value}. Got: {arg_value}.")
        return None

    return wrapper


def gt(limit: int) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not arg_value > limit:
            return ValueError(
                f"`{arg_name}` must be greater than {limit}. Got: {arg_value}."
            )
        return None

    return wrapper


def lt(limit: int) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not arg_value < limit:
            return ValueError(
                f"`{arg_name}` must be less than {limit}. Got: {arg_value}."
            )
        return None

    return wrapper


def ge(limit: int) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not arg_value >= limit:
            return ValueError(
                f"`{arg_name}` must be greater than or equal to {limit}. Got: {arg_value}."
            )
        return None

    return wrapper


def le(limit: int) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not arg_value <= limit:
            return ValueError(
                f"`{arg_name}` must be less than or equal to {limit}. Got: {arg_value}."
            )
        return None

    return wrapper


def max_len(limit: int) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not len(arg_value) <= limit:
            return ValueError(
                f"`{arg_name}` must have a length less than or equal to {limit}. Got length: {len(arg_value)}."
            )
        return None

    return wrapper


def min_len(limit: int) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not len(arg_value) >= limit:
            return ValueError(
                f"`{arg_name}` must have a length greater than or equal to {limit}. Got length: {len(arg_value)}."
            )
        return None

    return wrapper


def re_match(pattern: str) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not re.fullmatch(pattern, arg_value):
            return ValueError(
                f"`{arg_name}` must match the regex pattern `{pattern}`. Got: {arg_value}."
            )
        return None

    return wrapper


def re_search(pattern: str) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if not re.search(pattern, arg_value):
            return ValueError(
                f"`{arg_name}` must contain a match for the regex pattern `{pattern}`. Got: {arg_value}."
            )
        return None

    return wrapper


def is_in(valid_values: Iterable) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any) -> ValueError | None:
        if arg_value not in valid_values:
            return ValueError(
                f"`{arg_name}` must be one of {valid_values}. Got: {arg_value}."
            )
        return None

    return wrapper


def contains(required_values: Iterable) -> Callable:
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Iterable) -> ValueError | None:
        missing = [val for val in required_values if val not in arg_value]
        if missing:
            return ValueError(
                f"`{arg_name}` must contain all of {required_values}. Missing: {missing}."
            )
        return None

    return wrapper
