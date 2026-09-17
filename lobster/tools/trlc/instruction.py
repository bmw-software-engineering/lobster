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

from enum import Enum, auto
from dataclasses import dataclass


class InstructionType(Enum):
    CONSTANT_TEXT = auto()
    FIELD = auto()


@dataclass
class Instruction:
    """Specification how to convert a TRLC tuple field to string"""
    typ: InstructionType
    value: str


# pylint: disable=invalid-name
# The below functions use the CamelCase style instead of snake_case, so that the
# look and feel for the developer is that of using a class constructor, because the
# functions are essentially just wrappers around the constructor of the Instruction
# class.

def ConstantInstruction(value: str) -> Instruction:
    """Convenience function for constant text."""
    return Instruction(InstructionType.CONSTANT_TEXT, value)


def FieldInstruction(value: str) -> Instruction:
    """Convenience function for field."""
    return Instruction(InstructionType.FIELD, value)
