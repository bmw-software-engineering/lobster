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
