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

from typing import List


class CmdArgs:
    def __init__(self) -> None:
        self._args: List[str] = []

    def reset(self):
        """Resets the command line arguments"""
        self._args = []

    def append_arg(self, arg: str):
        """Appends an argument to the command line arguments"""
        self._args.append(arg)

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        return self._args
