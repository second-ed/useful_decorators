from typing import Callable, Sequence

import attrs


def make_type(
    name: str,
    validators: Callable | Sequence[Callable] | None = None,
    converters: Callable | Sequence[Callable] | None = None,
    frozen: bool = True,
) -> type:
    def to_list(value: Callable | Sequence[Callable]) -> list:
        return list(value) if isinstance(value, Sequence) else [value] if value else []  # type: ignore[truthy-function]

    kwargs = {}

    if validators:
        kwargs["validator"] = to_list(validators)
    if converters:
        kwargs["converter"] = to_list(converters)

    return attrs.define(frozen=frozen)(
        type(
            name,
            (),
            {
                "inner": attrs.field(**kwargs),  # type: ignore[call-overload]
                "new": classmethod(lambda cls, val: cls(val)),
                "clone": lambda self: type(self)(self.inner),
                "map": lambda self, fn: type(self)(fn(self.inner)),
                "apply": lambda self, fn: fn(self.inner),
            },
        )
    )
