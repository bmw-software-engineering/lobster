from typing import Iterable, List
import re
from trlc import ast
from lobster.tools.trlc.errors import TupleComponentError
from lobster.tools.trlc.instruction import (
    Instruction, InstructionType, ConstantInstruction, FieldInstruction,
)


PATTERN = re.compile(r"\$\([a-z][a-z0-9_]*\)", re.IGNORECASE)


def parse_instructions(text: str) -> List[Instruction]:
    """Parse a one-line text representing a list of instructions"""
    instructions = []
    cpos = 0
    for match in PATTERN.finditer(text):
        if match.span()[0] > cpos:
            instructions.append(ConstantInstruction(text[cpos:match.span()[0]]))
        instructions.append(FieldInstruction(match.group(0)[2:-1]))
        cpos = match.span()[1]
    if cpos < len(text):
        instructions.append(ConstantInstruction(text[cpos:]))
    return instructions


def build_text_from_instructions(
        instructions: Iterable[Instruction],
        tuple_aggregate: ast.Tuple_Aggregate,
) -> str:
    tuple_data = tuple_aggregate.to_python_object()
    if not tuple_data:
        raise ValueError("Cannot convert empty TRLC tuple to text!")
    if not instructions:
        raise ValueError(
            f"'to_string' instructions for tuple '{tuple_aggregate.typ.name}' "
            f"are empty!",
        )
    result = []
    for instruction in instructions:
        if instruction.typ == InstructionType.CONSTANT_TEXT:
            result.append(instruction.value)
        elif instruction.typ == InstructionType.FIELD:
            component_value = tuple_data.get(instruction.value)
            # Note: If the field does not exist in the record type OR if the record
            # object is not fully populated, we raise an error.
            if component_value is None:
                raise TupleComponentError(instruction.value, tuple_aggregate)
            result.append(str(component_value))
        else:
            raise ValueError(f"Unknown instruction type: {instruction.typ}")
    return "".join(result)
