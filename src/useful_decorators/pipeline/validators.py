import json
import re
from functools import wraps
from typing import Any, Callable, Iterable


class InvalidArgs(Exception):
    def __init__(self, fails):
        self.fails = fails

    def __str__(self):
        return json.dumps(self.fails, indent=4, sort_keys=False)


def catch_type_error(func: Callable):
    @wraps(func)
    def wrapper(arg_name: str, arg_value: Any):
        try:
            return func(arg_name, arg_value)
        except TypeError as e:
            return e

    return wrapper


def is_type(arg_type: type):
    def wrapper(arg_name: str, arg_value: Any):
        if not isinstance(arg_value, arg_type):
            return TypeError(
                f"`{arg_name}` must be type {arg_type}. Got: {type(arg_value)}"
            )

    return wrapper


def eq(value: int):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not arg_value == value:
            return ValueError(f"`{arg_name}` must equal {value}. Got: {arg_value}.")

    return wrapper


def gt(limit: int):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not arg_value > limit:
            return ValueError(
                f"`{arg_name}` must be greater than {limit}. Got: {arg_value}."
            )

    return wrapper


def lt(limit: int):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not arg_value < limit:
            return ValueError(
                f"`{arg_name}` must be less than {limit}. Got: {arg_value}."
            )

    return wrapper


def ge(limit: int):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not arg_value >= limit:
            return ValueError(
                f"`{arg_name}` must be greater than or equal to {limit}. Got: {arg_value}."
            )

    return wrapper


def le(limit: int):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not arg_value <= limit:
            return ValueError(
                f"`{arg_name}` must be less than or equal to {limit}. Got: {arg_value}."
            )

    return wrapper


def max_len(limit: int):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not len(arg_value) <= limit:
            return ValueError(
                f"`{arg_name}` must have a length less than or equal to {limit}. Got length: {len(arg_value)}."
            )

    return wrapper


def min_len(limit: int):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not len(arg_value) >= limit:
            return ValueError(
                f"`{arg_name}` must have a length greater than or equal to {limit}. Got length: {len(arg_value)}."
            )

    return wrapper


def re_match(pattern: str):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not re.fullmatch(pattern, arg_value):
            return ValueError(
                f"`{arg_name}` must match the regex pattern `{pattern}`. Got: {arg_value}."
            )

    return wrapper


def re_search(pattern: str):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if not re.search(pattern, arg_value):
            return ValueError(
                f"`{arg_name}` must contain a match for the regex pattern `{pattern}`. Got: {arg_value}."
            )

    return wrapper


def is_in(valid_values: Iterable):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Any):
        if arg_value not in valid_values:
            return ValueError(
                f"`{arg_name}` must be one of {valid_values}. Got: {arg_value}."
            )

    return wrapper


def contains(required_values: Iterable):
    @catch_type_error
    def wrapper(arg_name: str, arg_value: Iterable):
        missing = [val for val in required_values if val not in arg_value]
        if missing:
            return ValueError(
                f"`{arg_name}` must contain all of {required_values}. Missing: {missing}."
            )

    return wrapper
