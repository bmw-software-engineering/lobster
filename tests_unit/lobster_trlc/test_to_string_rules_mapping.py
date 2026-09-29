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

from lobster.tools.trlc.instruction import ConstantInstruction
from lobster.tools.trlc.to_string_rules import (
    ToStringRules,
    build_tuple_type_to_ruleset_map,
)
from tests_unit.lobster_trlc.trlc_hierarchy_data_test_case import \
    TrlcHierarchyDataTestCase


class BuildMapTest(TrlcHierarchyDataTestCase):
    """Tests for the 'build_tuple_type_to_ruleset_map' function.
    
       This unit test class implements tests which use real TRLC data as input, no mocks.
       See base class for details"""

    def test_build_map(self):
        """Tests that the mapping from tuple types to ToStringRules entities is built correctly."""
        # lobster-trace: trlc_req.To_String_Rules_Map_Built_From_Symbol_Table
        to_string_rule_sets=[
            ToStringRules(
                tuple_type_name="TwoValues",
                package_name=self.PACKAGE_NAME,
                rules=[[ConstantInstruction("two")]],
            ),
            ToStringRules(
                tuple_type_name="ThreeValues",
                package_name=self.PACKAGE_NAME,
                rules=[[ConstantInstruction("three")]],
            ),
            ToStringRules(
                tuple_type_name="FourValues",
                package_name=self.PACKAGE_NAME,
                rules=[[ConstantInstruction("four")]],
            ),
        ]

        result = build_tuple_type_to_ruleset_map(
            symbol_table=self._trlc_data_provider.symbol_table,
            to_string_rule_sets=to_string_rule_sets,
        )

        # verify that the mapping contains exactly the expected tuple types
        expected_types = set(self._trlc_data_provider.get_tuple_types())
        self.assertSetEqual(set(result.keys()), expected_types)

        # verify mapping between keys and values
        for key, value in result.items():
            self.assertEqual(key.name, value.tuple_type_name)
