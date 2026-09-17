# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

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
