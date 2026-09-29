# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from lobster.tools.trlc.converter import Converter
from lobster.tools.trlc.conversion_rule import ConversionRule
from tests_unit.lobster_trlc.trlc_optional_field_test_case import \
    TrlcOptionalFieldTestCase


class OptionalFieldTest(TrlcOptionalFieldTestCase):
    """TODO"""

    def test_optional_field_to_string(self):
        """Tests that an optional field is ignored if not set."""
        # lobster-trace: trlc_req.Optional_Field_Omitted_When_Not_Set

        fields = ["field1", "field2", "field3", "field4"]

        conversion_rules = [
            ConversionRule(
                package="optional_field_test",
                record_type="EverythingOptional",
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
            to_string_rules=[],
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        expected_to_string_results = {
            f"{self.PACKAGE_NAME}.A": {},
            f"{self.PACKAGE_NAME}.B": {
                "field1": "value of field 1 of B",
                "field2": "42",
                "field3": "True",
                "field4": "1.380649",
            },
            f"{self.PACKAGE_NAME}.C": {
                "field1": "value of field 1 of C",
                "field3": "False",
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
