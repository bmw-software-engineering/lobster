from unittest import TestCase
from lobster.tools.trlc.text_generation import (
    parse_instructions,
    ConstantInstruction,
    FieldInstruction,
)


class InstructionParsingTest(TestCase):
    def test_parse_text_generator(self):
        text = "Hello $(name), your age is $(age) and ID is " \
               "$(user_id_part1)$(user_id_part2)!"
        expected = [
            ConstantInstruction("Hello "),
            FieldInstruction("name"),
            ConstantInstruction(", your age is "),
            FieldInstruction("age"),
            ConstantInstruction(" and ID is "),
            FieldInstruction("user_id_part1"),
            FieldInstruction("user_id_part2"),
            ConstantInstruction("!"),
        ]
        result = parse_instructions(text)
        self.assertListEqual(result, expected)

    def test_parse_text_generator_with_no_fields(self):
        text = "Just a constant text without fields."
        expected = [ConstantInstruction(text)]
        result = parse_instructions(text)
        self.assertListEqual(result, expected)

    def test_parse_text_generator_only_fields(self):
        text = "$(a)$(bcd)$(e123)$(FG_HI)"
        expected = [
            FieldInstruction("a"),
            FieldInstruction("bcd"),
            FieldInstruction("e123"),
            FieldInstruction("FG_HI"),
        ]
        result = parse_instructions(text)
        self.assertListEqual(result, expected)
