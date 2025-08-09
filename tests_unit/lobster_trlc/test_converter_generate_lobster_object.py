import operator
from typing import List, Optional

from lobster.items import Requirement, Tracing_Tag
from lobster.location import Location
from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.converter import Converter
from lobster.tools.trlc.errors import (
    RecordObjectComponentError, TupleToStringFailedError, TupleToStringMissingError,
)
from lobster.tools.trlc.instruction import ConstantInstruction, FieldInstruction, Instruction
from lobster.tools.trlc.to_string_rules import ToStringRules
from tests_unit.lobster_trlc.integration_test_case_base import IntegrationTestCaseBase


class GenerateLobsterObjectTest(IntegrationTestCaseBase):
    """This unit test class implements tests which use real TRLC data as input, no mocks.
       See base class for details. 
    """

    _NON_EXISTING_FIELD = "field_does_not_exist"

    def test_empty_rules(self):
        """ Tests that no item is generated if no conversion rules are provided."""
        converter = Converter(
            conversion_rules=[],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertIsNone(lobster_item)

    def test_one_simple_rule(self):
        """Tests that an item is always generated if a conversion rule is provided."""
        for field_name in ("field1", "field2", None):
            with self.subTest(field_name=field_name):
                conversion_rule = ConversionRule(
                    record_type="Level1",
                    package="hierarchy_tree_test",
                    applies_to_derived_types=True,
                    namespace="req",
                    description_fields=[field_name] if field_name else None,
                )
                converter = Converter(
                    conversion_rules=[conversion_rule],
                    to_string_rules=[],
                    symbol_table=self._symbol_table,
                )
                for record_object in self._get_record_objects():
                    lobster_item = converter.generate_lobster_object(record_object)
                    self.assertIsInstance(lobster_item, Requirement)
                    self.assertIsInstance(lobster_item.tag, Tracing_Tag)
                    self.assertIsInstance(lobster_item.location, Location)
                    self.assertEqual(lobster_item.framework, "TRLC")
                    self.assertEqual(lobster_item.kind, record_object.n_typ.name)
                    self.assertEqual(
                        lobster_item.name,
                        record_object.fully_qualified_name(),
                    )
                    self.assertEqual(
                        lobster_item.text,
                        f"text of {record_object.name} in {field_name}"
                        if field_name else None,
                    )
                    self.assertIsNone(lobster_item.status)

    def test_description_field_missing(self):
        """Tests that an error is raised if a component is missing"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            description_fields=[self._NON_EXISTING_FIELD]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_record_objects():
            with self.assertRaises(RecordObjectComponentError) as ctx:
                converter.generate_lobster_object(record_object)
            self.assertEqual(
                str(ctx.exception.component_name),
                self._NON_EXISTING_FIELD,
            )

    def test_many_description_fields(self):
        """Tests that multiple description fields are handled correctly"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            description_fields=["field1", "field2"]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertEqual(
                lobster_item.text,
                f"field1: text of {record_object.name} in field1\n\n"
                f"field2: text of {record_object.name} in field2"
            )

    def test_tag_field_missing(self):
        """Tests that an error is raised if a required tag field is missing"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            tags=[self._NON_EXISTING_FIELD]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_record_objects():
            with self.assertRaises(RecordObjectComponentError) as ctx:
                converter.generate_lobster_object(record_object)
            self.assertEqual(
                str(ctx.exception.component_name),
                self._NON_EXISTING_FIELD,
            )

    def test_empty_reference_tag_field(self):
        """Tests that generation succeeds with zero unresolved references"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            tags=["reference_field1"]  # this value is always empty in the input data
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertListEqual(lobster_item.unresolved_references, [])

    def test_reference_tag_field(self):
        """Tests that one unresolved reference is generated"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            tags=["reference_field2"]  # this value is always set in the input data
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertEqual(len(lobster_item.unresolved_references), 1)
            tracing_tag = lobster_item.unresolved_references[0]
            self.assertIsInstance(tracing_tag, Tracing_Tag)
            self.assertEqual(
                tracing_tag.namespace,
                "req",
            )
            self.assertEqual(
                tracing_tag.tag,
                "hierarchy_tree_test.Level1_Item",
            )
            self.assertIsNone(tracing_tag.version)

    def test_text_tag_field(self):
        """Tests that a text field can be used as tag field"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            tags=["field1"]  # this value is always set in the input data
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertEqual(len(lobster_item.unresolved_references), 1)
            tracing_tag = lobster_item.unresolved_references[0]
            self.assertIsInstance(tracing_tag, Tracing_Tag)
            self.assertEqual(
                tracing_tag.namespace,
                "req",
            )
            self.assertEqual(
                tracing_tag.tag,
                f"text of {record_object.name} in field1",
            )
            self.assertIsNone(tracing_tag.version)

    def test_tuple_tag_field(self):
        """Tests that a tuple field can be used as tag field"""
        conversion_rule = ConversionRule(
            record_type=self.LEVEL4B_TYPE_NAME,
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            tags=["tuple_field1"]
        )
        to_string_rules = (
            ToStringRules(
                tuple_type_name="ThreeValues",
                package_name="hierarchy_tree_test",
                rules=[
                    [
                        ConstantInstruction(value="huhu"),
                        FieldInstruction(value="tuple_member2"),
                    ]
                ]
            ),
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=to_string_rules,
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_filtered_record_objects(conversion_rule.type_name, operator.eq):
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertEqual(len(lobster_item.unresolved_references), 1)
            tracing_tag = lobster_item.unresolved_references[0]
            self.assertIsInstance(tracing_tag, Tracing_Tag)
            self.assertEqual(
                tracing_tag.namespace,
                "req",
            )
            self.assertEqual(
                tracing_tag.tag,
                "huhu2",
            )
            self.assertIsNone(tracing_tag.version)

    def test_tuple_tag_field_without_to_string(self):
        """Tests that an error is raised if to_string instructions are missing"""
        conversion_rule = ConversionRule(
            record_type=self.LEVEL4B_TYPE_NAME,
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            tags=["tuple_field1"]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._symbol_table,
        )
        for record_object in self._get_filtered_record_objects(self.LEVEL4B_TYPE_NAME, operator.eq):
            with self.assertRaises(TupleToStringMissingError) as ctx:
                converter.generate_lobster_object(record_object)
            self.assertEqual(ctx.exception.tuple_aggregate.typ.name, "ThreeValues")

    def setup_with_failing_instructions(
            self,
            append_rules: Optional[List[Instruction]] = None,
        ):
        """Sets up a converter with to_string rules that will fail, but extra
           ToStringRules can be appended."""
        conversion_rule = ConversionRule(
            record_type=self.LEVEL4B_TYPE_NAME,
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
            tags=["tuple_field1"]
        )
        rules=[
            [FieldInstruction(value=self._NON_EXISTING_FIELD)],
            [FieldInstruction(value="tuple_member1"),  # this will succeed
             FieldInstruction(value="another_non_existing_field")],  # but this will fail
        ]
        if append_rules:
            rules.append(append_rules)
        to_string_rules = [
            ToStringRules(
                tuple_type_name="ThreeValues",
                package_name="hierarchy_tree_test",
                rules=rules,
            ),
        ]
        return Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=to_string_rules,
            symbol_table=self._symbol_table,
        )

    def test_tuple_tag_with_failing_instructions(self):
        """Tests that an error is raised if all to_string instructions fail"""
        converter = self.setup_with_failing_instructions()
        for record_object in self._get_filtered_record_objects(self.LEVEL4B_TYPE_NAME, operator.eq):
            with self.assertRaises(TupleToStringFailedError) as ctx:
                converter.generate_lobster_object(record_object)
            self.assertEqual(ctx.exception.tuple_aggregate.typ.name, "ThreeValues")

    def test_tuple_tag_with_failing_and_succeeding_instructions(self):
        """Tests success if the last to_string instructions succeed"""
        converter = self.setup_with_failing_instructions(
            append_rules=[
                ConstantInstruction(value="huhu"),
                FieldInstruction(value="tuple_member2"),
                ],
        )
        for record_object in self._get_filtered_record_objects(self.LEVEL4B_TYPE_NAME, operator.eq):
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertEqual(len(lobster_item.unresolved_references), 1)
            tracing_tag = lobster_item.unresolved_references[0]
            self.assertIsInstance(tracing_tag, Tracing_Tag)
            self.assertEqual(
                tracing_tag.namespace,
                "req",
            )
            self.assertEqual(
                tracing_tag.tag,
                "huhu2",
            )
            self.assertIsNone(tracing_tag.version)
