import operator
from typing import List, Optional

from lobster.common.items import Requirement, Tracing_Tag
from lobster.common.location import Location
from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.converter import Converter
from lobster.tools.trlc.errors import (
    RecordObjectComponentError,
    TupleToStringFailedError,
    TupleToStringMissingError,
)
from lobster.tools.trlc.instruction import (
    ConstantInstruction,
    FieldInstruction,
    Instruction,
)
from lobster.tools.trlc.to_string_rules import ToStringRules
from tests_unit.lobster_trlc.trlc_hierarchy_data_test_case import \
    TrlcHierarchyDataTestCase


class GenerateLobsterObjectTest(TrlcHierarchyDataTestCase):
    """This unit test class implements tests which use real TRLC data as input, no mocks.
       See base class for details. 
    """

    _NON_EXISTING_FIELD = "field_does_not_exist"

    def test_empty_rules(self):
        """ Tests that no item is generated if no conversion rules are provided."""
        converter = Converter(
            conversion_rules=[],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertIsNone(lobster_item)

    def test_one_simple_rule(self):
        """Tests that an item is always generated if a conversion rule is provided."""
        for field_name in ("field1", "field2", None):
            with self.subTest(field_name=field_name):
                conversion_rule = ConversionRule(
                    record_type="Level1",
                    package=self.PACKAGE_NAME,
                    applies_to_derived_types=True,
                    namespace="req",
                    description_fields=[field_name] if field_name else None,
                )
                converter = Converter(
                    conversion_rules=[conversion_rule],
                    to_string_rules=[],
                    symbol_table=self._trlc_data_provider.symbol_table,
                )
                for record_object in self._trlc_data_provider.get_record_objects():
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
                        if field_name else "",
                    )
                    self.assertIsNone(lobster_item.status)

    def test_description_field_missing(self):
        """Tests that an error is raised if a TRLC field is missing
        
           This means, the conversion rules tries to access a field that has not been
           defined in the *.rsl file. In that case an exception is expected.
        """
        conversion_rule = ConversionRule(
            record_type="Level1",
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            description_fields=[self._NON_EXISTING_FIELD]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
            with self.assertRaises(RecordObjectComponentError) as ctx:
                converter.generate_lobster_object(record_object)
            self.assertEqual(
                str(ctx.exception.component_name),
                self._NON_EXISTING_FIELD,
            )

    def test_optional_field_missing(self):
        """Tests that no error is raised if an optional TRLC field is missing"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            description_fields=[self._NON_EXISTING_FIELD]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
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
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            description_fields=["field1", "field2"]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
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
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            tags=[self._NON_EXISTING_FIELD]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
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
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            tags=["reference_field1"]  # this value is always empty in the input data
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertListEqual(lobster_item.unresolved_references, [])

    def test_reference_tag_field(self):
        """Tests that one unresolved reference is generated"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            tags=["reference_field2"]  # this value is always set in the input data
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
            with self.subTest(record_object=record_object.name):
                lobster_item = converter.generate_lobster_object(record_object)
                self.assertEqual(len(lobster_item.unresolved_references), 1)
                tracing_tag = lobster_item.unresolved_references[0]
                self.assertIsInstance(tracing_tag, Tracing_Tag)
                self.assertEqual(
                    tracing_tag.namespace,
                    "req",
                )
                self.assertIsInstance(tracing_tag.tag, str, "Tag must be a string")
                self.assertEqual(
                    tracing_tag.tag,
                    "hierarchy_tree_test.Level1_Item",
                    "Tag mismatch!"
                )
                self.assertIsNone(tracing_tag.version)

    def test_text_tag_field(self):
        """Tests that a text field can be used as tag field"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            tags=["field1"]  # this value is always set in the input data
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
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

        # better move this test into test_to_string_rules.py

        conversion_rule = ConversionRule(
            record_type=self.LEVEL4B_TYPE_NAME,
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            tags=["tuple_field1"]
        )
        to_string_rules = (
            ToStringRules(
                tuple_type_name="ThreeValues",
                package_name=self.PACKAGE_NAME,
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
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_filtered_record_objects(
            conversion_rule.type_name,
            operator.eq,
        ):
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
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            tags=["tuple_field1"]
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_filtered_record_objects(
            self.LEVEL4B_TYPE_NAME,
            operator.eq,
        ):
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
            package=self.PACKAGE_NAME,
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
                package_name=self.PACKAGE_NAME,
                rules=rules,
            ),
        ]
        return Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=to_string_rules,
            symbol_table=self._trlc_data_provider.symbol_table,
        )

    def test_tuple_tag_with_failing_instructions(self):
        """Tests that an error is raised if all to_string instructions fail"""
        converter = self.setup_with_failing_instructions()
        for record_object in self._trlc_data_provider.get_filtered_record_objects(
            self.LEVEL4B_TYPE_NAME,
            operator.eq,
        ):
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
        for record_object in self._trlc_data_provider.get_filtered_record_objects(
            self.LEVEL4B_TYPE_NAME,
            operator.eq,
        ):
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

    def test_justification_fields(self):
        """Tests that justification fields are handled correctly"""
        conversion_rule = ConversionRule(
            record_type="Level1",
            package=self.PACKAGE_NAME,
            applies_to_derived_types=True,
            namespace="req",
            justification_up_fields=["field1"],
            justification_down_fields=["field1", "field2"],
            justification_global_fields=["reference_field2", "TUPLE_FIELD2"],
        )
        converter = Converter(
            conversion_rules=[conversion_rule],
            to_string_rules=(
                ToStringRules(
                    tuple_type_name="ThreeValues",
                    package_name=self.PACKAGE_NAME,
                    rules=[
                        [
                            FieldInstruction(value="tuple_member2"),
                            ConstantInstruction(value="-hello-"),
                            FieldInstruction(value="tuple_member2"),
                        ]
                    ],
                ),
            ),
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        for record_object in self._trlc_data_provider.get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)
            self.assertEqual(
                lobster_item.just_up,
                [f"text of {record_object.name} in field1"]
            )
            self.assertEqual(
                lobster_item.just_down,
                [f"text of {record_object.name} in field1", f"text of {record_object.name} in field2"],
            )
            expected_just_global = ["hierarchy_tree_test.Level1_Item"]
            if record_object.n_typ.name == self.LEVEL4B_TYPE_NAME:
                expected_just_global.append("5-hello-5")
            self.assertEqual(
                lobster_item.just_global,
                expected_just_global,
            )
