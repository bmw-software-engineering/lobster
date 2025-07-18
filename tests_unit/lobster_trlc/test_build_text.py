import operator

from lobster.tools.trlc.instruction import ConstantInstruction, FieldInstruction
from lobster.tools.trlc.item_wrapper import ItemWrapper
from lobster.tools.trlc.text_generation import build_text
from tests_unit.lobster_trlc.integration_test_case_base import IntegrationTestCaseBase


class BuildTextTest(IntegrationTestCaseBase):
    """This unit test class implements tests which use real TRLC data as input, no mocks.
       See base class for details. 
    """
    def test_build_text_from_string_field(self):
        for record_object in self._get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("field1", "field2"):
                with self.subTest(field_name=field_name, record_object=record_object.name):
                    text = build_text(
                        field_name=field_name,
                        item_wrapper=item_wrapper,
                        to_string_rules={},
                    )
                    self.assertEqual(
                        text,
                        f"text of {record_object.name} in {field_name}",
                    )

    def test_build_text_from_empty_tuple_field(self):
        # iterate over all record objects except those of type Level4B
        # Level4B instances do have tuple values, all others do not
        for record_object in self._get_filtered_record_objects("Level4B", operator.ne):
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("tuple_field1", "TUPLE_FIELD2"):
                with self.subTest(field_name=field_name):
                    with self.assertRaises(ValueError) as ctx:
                        build_text(
                            field_name=field_name,
                            item_wrapper=item_wrapper,
                            to_string_rules=[],
                        )
                    self.assertEqual(
                        str(ctx.exception),
                        f"Component '{field_name}' is None in item "
                        f"{record_object.fully_qualified_name()}",
                    )

    def test_build_text_from_tuple_field_missing_tostring(self):
        for record_object in self._get_filtered_record_objects("Level4B", operator.eq):
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("tuple_field1", "TUPLE_FIELD2"):
                with self.subTest(field_name=field_name, record_object=record_object.name):
                    with self.assertRaises(ValueError) as ctx:
                        build_text(
                            field_name=field_name,
                            item_wrapper=item_wrapper,
                            to_string_rules=[],
                        )
                    self.assertEqual(
                        str(ctx.exception),
                        "'to_string' instructions for tuple 'ThreeValues' are empty!",
                    )

    def test_build_text_from_tuple_field(self):
        instructions = [
            FieldInstruction("tuple_member3"),
            ConstantInstruction("-"),
            FieldInstruction("tuple_member2"),
            ConstantInstruction("."),
            FieldInstruction("tuple_member1"),
        ]
        for record_object in self._get_filtered_record_objects("Level4B", operator.eq):
            item_wrapper = ItemWrapper(record_object)
            for field_name, expectation in (
                ("tuple_field1", "3-2.1"),
                ("TUPLE_FIELD2", "6-5.4"),
            ):
                with self.subTest(field_name=field_name, record_object=record_object.name):
                    text = build_text(
                        field_name=field_name,
                        item_wrapper=item_wrapper,
                        to_string_rules=instructions,
                    )
                    self.assertEqual(text, expectation)
