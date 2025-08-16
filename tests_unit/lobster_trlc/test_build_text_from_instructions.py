from unittest import TestCase
from unittest.mock import Mock
from trlc import ast
from lobster.tools.trlc.errors import TupleComponentError
from lobster.tools.trlc.text_generation import (
    ConstantInstruction,
    FieldInstruction,
    Instruction,
    build_text_from_instructions,
)


class TextBuildingTest(TestCase):
    """Tests for the 'build_text_from_instructions' function."""

    def setUp(self):
        self._tuple_aggregate_mock = Mock(spec=ast.Tuple_Aggregate)
        self._tuple_aggregate_mock.location = Mock(spec=ast.Location)
        self._tuple_aggregate_mock.typ = Mock(spec=ast.Type)
        self._tuple_aggregate_mock.typ.location = Mock(spec=ast.Location)
        self._tuple_aggregate_mock.typ.name = "flute"

    def test_build_text_from_instructions(self):
        instructions = [
            ConstantInstruction("piano"),
            ConstantInstruction("guitar"),
            ConstantInstruction("violin"),
            FieldInstruction("harmonium"),
            FieldInstruction("sitar"),
        ]
        self._tuple_aggregate_mock.to_python_object.return_value = {
            "piano": "1",
            "guitar": "2",
            "violin": "3",
            "harmonium": 4,
            "sitar": 5.5,
        }
        result = build_text_from_instructions(instructions, self._tuple_aggregate_mock)
        self.assertEqual(result, "pianoguitarviolin45.5")

    def test_build_text_with_missing_field(self):
        instruction = FieldInstruction("music")
        self._tuple_aggregate_mock.to_python_object.return_value = {"noise": "loud"}
        with self.assertRaises(TupleComponentError) as e:
            build_text_from_instructions([instruction], self._tuple_aggregate_mock)
        self.assertEqual(
            e.exception.component_name,
            "music",
        )
        self.assertIs(e.exception.tuple_aggregate, self._tuple_aggregate_mock)

    def test_build_text_with_empty_instructions(self):
        instructions = []
        self._tuple_aggregate_mock.to_python_object.return_value = {"hi": "there"}
        with self.assertRaises(ValueError):
            build_text_from_instructions(instructions, self._tuple_aggregate_mock)

    def test_invalid_instruction_type(self):
        """Test that an invalid instruction type raises a ValueError."""
        instruction = Instruction(typ="Electric", value="Engine")
        with self.assertRaises(ValueError) as ctx:
            build_text_from_instructions([instruction], self._tuple_aggregate_mock)
        self.assertEqual(
            str(ctx.exception),
            f"Unknown instruction type: {instruction.typ}",
        )

    def test_empty_tuple_data(self):
        """Test that an invalid instruction type raises a ValueError."""
        instruction = ConstantInstruction(value="Otto")
        self._tuple_aggregate_mock.to_python_object.return_value = {}
        with self.assertRaises(ValueError) as ctx:
            build_text_from_instructions([instruction], self._tuple_aggregate_mock)
        self.assertEqual(
            str(ctx.exception),
            "Cannot convert empty TRLC tuple to text!",
        )
