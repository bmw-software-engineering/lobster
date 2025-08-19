from lobster.tools.trlc.instruction import ConstantInstruction, FieldInstruction
from lobster.tools.trlc.to_string_rules import ToStringRules
from lobster.tools.trlc.converter import Converter
from lobster.tools.trlc.conversion_rule import ConversionRule
from tests_unit.lobster_trlc.trlc_to_string_data_test_case import TrlcToStringDataTestCase


class ToStringRulesTest(TrlcToStringDataTestCase):
    """This test class focuses on ensuring that tuple fields are correctly converted to strings.

       This unit test class implements tests which use real TRLC data as input, no mocks.
       See base class for details."""

    def test_field_is_tuple_type(self):
        """Tests that a tuple field is properly converted to a string."""
        to_string_rule_sets=[
            ToStringRules(
                tuple_type_name="ship",
                package_name=self.PACKAGE_NAME,
                rules=[[
                    FieldInstruction("name"),
                    ConstantInstruction("="),
                    FieldInstruction("length"),
                    ConstantInstruction("|"),
                    FieldInstruction("WIDTH"),
                ]],
            ),
        ]

        fields = ["fast_boat", "large_boat"]

        conversion_rules = [
            ConversionRule(
                package="to_string_test",
                record_type="shipyard",
                namespace="req",
                description_fields=fields,
                tags=fields,
                justification_down_fields=fields,
                justification_up_fields=fields,
                justification_global_fields=fields,
            ),
        ]

        converter = Converter(
            conversion_rules=conversion_rules,
            to_string_rules=to_string_rule_sets,
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        expected_to_string_results = {
            f"{self.PACKAGE_NAME}.TONY": {
                "fast_boat": "Flying Cloud=30|8.5",
                "large_boat": "Sea Explorer=50|12.0",
            },
            f"{self.PACKAGE_NAME}.BOBBY": {
                "fast_boat": "Speedster=25|7.0",
                "large_boat": "Ocean Voyager=60|15.0",
            },
            f"{self.PACKAGE_NAME}.ELLEN": {
                "fast_boat": "=-25|1.0001",
                "large_boat": "Sneaky Submarine=99|999.9999",
            },
        }

        for record_object in self._trlc_data_provider.get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)

            expected_texts = set(expected_to_string_results[lobster_item.name].values())

            # verify string in "tag" of references
            self.assertSetEqual(
                set(tracing_tag.tag for tracing_tag in
                    lobster_item.unresolved_references),
                expected_texts,
            )

            # verify string in simple lists of LOBSTER item
            for data_list in (
                lobster_item.just_down,
                lobster_item.just_global,
                lobster_item.just_up,
            ):
                self.assertSetEqual(set(data_list), expected_texts)

            # verify string in "text" of LOBSTER item
            expected_text = "\n\n".join(f"{field}: {text}"
                for field, text in sorted(
                    expected_to_string_results[lobster_item.name].items(),
                )
            )
            self.assertEqual(lobster_item.text, expected_text)

    def test_field_is_tuple_array_type(self):
        """Tests that a tuple array field is properly converted to a string."""
        to_string_rule_sets=[
            ToStringRules(
                tuple_type_name="ship",
                package_name=self.PACKAGE_NAME,
                rules=[[
                    FieldInstruction("name"),
                    ConstantInstruction(" w="),
                    FieldInstruction("WIDTH"),
                    ConstantInstruction(" l="),
                    FieldInstruction("length"),
                ]],
            ),
        ]

        fields = ["berthed_ships"]

        conversion_rules = [
            ConversionRule(
                package="to_string_test",
                record_type="shipyard",
                namespace="req",
                description_fields=fields,
                tags=fields,
                justification_down_fields=fields,
                justification_up_fields=fields,
                justification_global_fields=fields,
            ),
        ]

        converter = Converter(
            conversion_rules=conversion_rules,
            to_string_rules=to_string_rule_sets,
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        expected_to_string_results = {
            f"{self.PACKAGE_NAME}.TONY": [],
            f"{self.PACKAGE_NAME}.BOBBY": [
                "Harbor Master w=5.1 l=20",
                "Wave Rider w=6.2 l=22",
            ],
            f"{self.PACKAGE_NAME}.ELLEN": [
                "Wind Sailor w=-5.01 l=999999",
                "Paradise w=12.34 l=-1234",
            ],
        }

        for record_object in self._trlc_data_provider.get_record_objects():
            lobster_item = converter.generate_lobster_object(record_object)

            expected_texts = set(expected_to_string_results[lobster_item.name])

            # verify string in "tag" of references
            self.assertSetEqual(
                set(tracing_tag.tag for tracing_tag in
                    lobster_item.unresolved_references),
                expected_texts,
            )

            # verify string in simple lists of LOBSTER item
            for data_list in (
                lobster_item.just_down,
                lobster_item.just_global,
                lobster_item.just_up,
            ):
                self.assertSetEqual(set(data_list), expected_texts)

            # verify string in "text" of LOBSTER item
            # Note: The order of the array elements in the TRLC file matters!
            # "Harbor Master" comes before "Wave Rider" in the TRLC file,
            # so it should also come first in the LOBSTER item text.
            expected_text = ", ".join(expected_to_string_results[lobster_item.name])
            self.assertEqual(lobster_item.text, expected_text)
