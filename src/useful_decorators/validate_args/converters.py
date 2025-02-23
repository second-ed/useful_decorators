from typing import Any


def to_type(dst_type: type):
    def wrapper(arg_name: str, arg_value: Any):
        try:
            return dst_type(arg_value)
        except TypeError as e:
            print(
                f"Failed to convert type for arg '{arg_name}': {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def replace_none(default_value: Any):
    def wrapper(arg_name: str, arg_value: Any):
        return arg_value if arg_value is not None else default_value

    return wrapper


def clip_min(min_value: float):
    def wrapper(arg_name: str, arg_value: Any):
        try:
            return max(min_value, float(arg_value))
        except TypeError as e:
            print(
                f"Failed to clip '{arg_name}' to min {min_value}: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def clip_max(max_value: float):
    def wrapper(arg_name: str, arg_value: Any):
        try:
            return min(max_value, float(arg_value))
        except TypeError as e:
            print(
                f"Failed to clip '{arg_name}' to max {max_value}: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def strip_chars(chars: str):
    def wrapper(arg_name: str, arg_value: Any):
        try:
            return str(arg_value).strip(chars)
        except TypeError as e:
            print(
                f"Failed to strip chars '{chars}' from arg '{arg_name}': {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def to_lower():
    def wrapper(arg_name: str, arg_value: Any):
        try:
            return str(arg_value).lower()
        except TypeError as e:
            print(
                f"Failed to convert '{arg_name}' to lowercase: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def to_upper():
    def wrapper(arg_name: str, arg_value: Any):
        try:
            return str(arg_value).upper()
        except TypeError as e:
            print(
                f"Failed to convert '{arg_name}' to uppercase: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper
