import operator

from lobster.tools.trlc.errors import TupleToStringMissingError
from lobster.tools.trlc.instruction import ConstantInstruction, FieldInstruction
from lobster.tools.trlc.item_wrapper import ItemWrapper
from lobster.tools.trlc.converter import Converter, ToStringRules
from tests_unit.lobster_trlc.trlc_hierarchy_data_test_case import \
    TrlcHierarchyDataTestCase


class GenerateTextEmptyRulesTest(TrlcHierarchyDataTestCase):
    """Tests for the 'Converter._generate_text' function.
    
       This unit test class implements tests which use real TRLC data as input, no mocks.
       See base class for details. 
    """

    def setUp(self) -> None:
        super().setUp()
        self._converter = Converter(
           symbol_table=self._trlc_data_provider.symbol_table,
           to_string_rules=[],
           conversion_rules=[],
        )

    def test_generate_text_from_string_array_field(self):
        """Test that a string array field can be converted to text."""
        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            text = self._converter._generate_text(item_wrapper, "string_array_field1")
            self.assertListEqual(
                text,
                [f"{record_object.name}+string_{i}" for i in range(1, 4)],
            )

            text = self._converter._generate_text(item_wrapper, "integer_array_field1")
            self.assertListEqual(
                text,
                [str(i) for i in range(1, 4)],
            )

            text = self._converter._generate_text(item_wrapper, "decimal_array_field1")
            self.assertListEqual(
                text,
                [f"{i}.{i}" for i in range(1, 4)],
            )

            text = self._converter._generate_text(item_wrapper, "boolean_array_field1")
            self.assertListEqual(
                text,
                list(map(str, [True, False, True, True])),
            )
            # There is only one record object with 'string_array_field1' field in the
            # test data, so we can break after the first iteration
            break

    def test_generate_text_from_string_field(self):
        """Test that a string field can be converted to text."""
        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("field1", "field2"):
                with self.subTest(
                    field_name=field_name,
                    record_object=record_object.name,
                ):
                    text = self._converter._generate_text(item_wrapper, field_name)
                    self.assertListEqual(
                        text,
                        [f"text of {record_object.name} in {field_name}"],
                    )

    def test_generate_text_from_empty_tuple_field(self):
        """Test that a tuple field with no values results in an empty list ."""
        # iterate over all record objects except those of type Level4B
        # Level4B instances do have tuple values, all others do not
        for record_object in self._trlc_data_provider.get_filtered_record_objects(
            self.LEVEL4B_TYPE_NAME,
            operator.ne,
        ):
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("tuple_field1", "TUPLE_FIELD2"):
                with self.subTest(field_name=field_name):
                    text = self._converter._generate_text(item_wrapper, field_name)
                    self.assertListEqual(text, [])


    def test_generate_text_from_tuple_field_missing_tostring(self):
        """Test that a tuple field with no 'to_string' instructions raises an error."""
        for record_object in self._trlc_data_provider.get_filtered_record_objects(
            self.LEVEL4B_TYPE_NAME,
            operator.eq,
        ):
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("tuple_field1", "TUPLE_FIELD2"):
                with self.subTest(
                    field_name=field_name,
                    record_object=record_object.name,
                ):
                    with self.assertRaises(TupleToStringMissingError) as ctx:
                        self._converter._generate_text(item_wrapper, field_name)
                    self.assertIn(
                        "No 'to-string' function defined for tuple 'ThreeValues'",
                        str(ctx.exception),
                    )


class GenerateTextGivenRulesTest(TrlcHierarchyDataTestCase):
    """Tests for the 'Converter._generate_text' function.
    
       The difference to the above test class is that, here we define
       'to_string_rules' for the tuple type, where above we did not.
    """

    def setUp(self) -> None:
        super().setUp()
        instructions = [
            FieldInstruction("tuple_member3"),
            ConstantInstruction("-"),
            FieldInstruction("tuple_member2"),
            ConstantInstruction("."),
            FieldInstruction("tuple_member1"),
        ]
        to_string_rules = ToStringRules(
            rules=[instructions],
            tuple_type_name="ThreeValues",
            package_name=self.PACKAGE_NAME,
        )
        self._converter = Converter(
            symbol_table=self._trlc_data_provider.symbol_table,
            to_string_rules=[to_string_rules],
            conversion_rules=[],
        )

    def test_generate_text_from_tuple_field(self):
        """Test that tuple field is converted to text by adhering to the instructions."""

        for record_object in self._trlc_data_provider.get_filtered_record_objects(
            self.LEVEL4B_TYPE_NAME,
            operator.eq,
        ):
            item_wrapper = ItemWrapper(record_object)
            for field_name, expectation in (
                ("tuple_field1", "3-2.1"),
                ("TUPLE_FIELD2", "6-5.4"),
            ):
                with self.subTest(
                    field_name=field_name,
                    record_object=record_object.name,
                ):
                    text = self._converter._generate_text(item_wrapper, field_name)
                    self.assertListEqual(text, [expectation])
