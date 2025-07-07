from typing import Iterable, Optional, Tuple


def arguments_to_list(
        key_value_args: Optional[Iterable[Tuple[str, Optional[str]]]] = None,
        flags: Optional[Iterable[Tuple[str, Optional[bool]]]] = None,
):
    result = []
    if key_value_args:
        for key, value in key_value_args:
            if value is not None:
                result.append(f"{key}={value}")
    if flags:
        for flag, activate in flags:
            if activate:
                result.append(flag)
    return result
