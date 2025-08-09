from typing import Iterable, List
import re
from trlc import ast
from lobster.tools.trlc.errors import TupleComponentError
from lobster.tools.trlc.instruction import (
    Instruction, InstructionType, ConstantInstruction, FieldInstruction,
)
from lobster.tools.trlc.item_wrapper import ItemWrapper


PATTERN = re.compile(r"\$\([a-z][a-z0-9_]*\)", re.IGNORECASE)


def parse_instructions(text: str) -> List[Instruction]:
    """Parse a text representing a list of instructions"""
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
            if instruction.value not in tuple_data:
                raise TupleComponentError(instruction.value, tuple_aggregate)
            result.append(str(tuple_data[instruction.value]))
        else:
            raise ValueError(f"Unknown instruction type: {instruction.typ}")
    return "".join(result)


def build_text(
        field_name: str,
        item_wrapper: ItemWrapper,
        to_string_rules: Iterable[Instruction],
) -> str:
    value_type = item_wrapper.get_field_raw(field_name).typ
    if isinstance(value_type, ast.Array_Type):
        raise ValueError(
            "Cannot generate text for array types!"
        )
    if isinstance(value_type, ast.Tuple_Type):
        return build_text_from_instructions(
            to_string_rules,
            item_wrapper.get_field_raw(field_name),
        )

    value = item_wrapper.get_field(field_name)
    if value is None:
        raise ValueError(
            f"Component '{field_name}' is None in item "
            f"{item_wrapper.n_obj.fully_qualified_name()}",
        )

    return str(value)
