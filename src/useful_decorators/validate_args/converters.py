from typing import Any, Callable


def to_type(dst_type: type) -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> Callable:
        try:
            return dst_type(arg_value)
        except TypeError as e:
            print(
                f"Failed to convert type for arg '{arg_name}': {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def replace_none(default_value: Any) -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> Callable:
        return arg_value if arg_value is not None else default_value

    return wrapper


def clip_min(min_value: float) -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> float | str:
        try:
            return max(min_value, float(arg_value))
        except TypeError as e:
            print(
                f"Failed to clip '{arg_name}' to min {min_value}: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def clip_max(max_value: float) -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> float | str:
        try:
            return min(max_value, float(arg_value))
        except TypeError as e:
            print(
                f"Failed to clip '{arg_name}' to max {max_value}: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def strip_chars(chars: str) -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> str:
        try:
            return str(arg_value).strip(chars)
        except TypeError as e:
            print(
                f"Failed to strip chars '{chars}' from arg '{arg_name}': {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def to_lower() -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> str:
        try:
            return str(arg_value).lower()
        except TypeError as e:
            print(
                f"Failed to convert '{arg_name}' to lowercase: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper


def to_upper() -> Callable:
    def wrapper(arg_name: str, arg_value: Any) -> str:
        try:
            return str(arg_value).upper()
        except TypeError as e:
            print(
                f"Failed to convert '{arg_name}' to uppercase: {arg_value}. Error: {e}"
            )
            return arg_value

    return wrapper
