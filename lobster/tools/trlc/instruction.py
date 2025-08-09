from enum import Enum, auto
from dataclasses import dataclass


class InstructionType(Enum):
    CONSTANT_TEXT = auto()
    FIELD = auto()


@dataclass
class Instruction:
    typ: InstructionType
    value: str


# pylint: disable=invalid-name

def ConstantInstruction(value: str) -> Instruction:
    """Convenience function for constant text."""
    return Instruction(InstructionType.CONSTANT_TEXT, value)


def FieldInstruction(value: str) -> Instruction:
    """Convenience function for field."""
    return Instruction(InstructionType.FIELD, value)
