import itertools
from pathlib import Path
from unittest import TestCase

from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.hierarchy_tree import build_children_lookup
from lobster.tools.trlc.conversion_rule_lookup import (
    build_record_type_to_conversion_rule_lookup,
    get_record_types,
)
from tests_unit.lobster_trlc.trlc_data_provider import TrlcDataProvider


class RuleOrderTest(TestCase):
    def setUp(self) -> None:
        self._trlc_data_provider = TrlcDataProvider(
            callback_test_case=self,
            trlc_input_files=[
                Path(__file__).parent / "data" / "order_addon.rsl",
                Path(__file__).parent / "data" / "order.rsl",
            ],
            expected_record_type_names=set((
                "AA_Type",
                "AA_Type_Addon",
                "BB_Type",
                "ZZ_Type",
                "Some_Unused_Type",
            )),
        )
        super().setUp()

    def test_order(self):
        """Tests that the TRLC record types are extracted in the order given in the *.rsl
           file, and that the rule for type ZZ_Type does not override the rules for its
           derived types.
           Note: This happens if the wrong TRLC api function is used to get the
           record types, which returns them in alphabetical order.
        """
        top_rule = ConversionRule(
            record_type="ZZ_Type",
            package="order_test",
            applies_to_derived_types=True,
            namespace="req",
        )
        rule_bb = ConversionRule(
                record_type="BB_Type",
                package="order_test",
                applies_to_derived_types=True,
                namespace="req",
        )
        rule_aa = ConversionRule(
                record_type="AA_Type",
                package="order_test",
                applies_to_derived_types=True,
                namespace="req",
        )
        expected_rule_lookup = {
            "ZZ_Type": top_rule,
            "BB_Type": rule_bb,
            "AA_Type": rule_aa,
            "AA_Type_Addon": rule_aa,
        }

        # We repeat the test for all 6 permutations of the rules to ensure that
        # the order of rules does not affect the result.
        for permutation in itertools.permutations(
            [top_rule, rule_bb, rule_aa],
        ):
            permutation_name = ", ".join(rule.type_name for rule in permutation)
            with self.subTest(permutation=permutation_name):
                print(f"Testing permutation: {permutation_name}")
                lookup = build_record_type_to_conversion_rule_lookup(
                    conversion_rules=permutation,
                    children_lookup=build_children_lookup(
                        self._trlc_data_provider.symbol_table,
                    ),
                    symbol_table=self._trlc_data_provider.symbol_table,
                )
                self.assertIsInstance(lookup, dict)
                self.assertEqual(len(lookup), len(expected_rule_lookup))

                for n_typ in self._trlc_data_provider.get_record_types():
                    if n_typ.name == "Some_Unused_Type":
                        self.assertNotIn(n_typ, lookup)
                    else:
                        self.assertIn(
                            n_typ,
                            lookup,
                            f"Record type '{n_typ.name}' not found in conversion rule lookup.",
                        )
                        self.assertIs(
                            lookup[n_typ],
                            expected_rule_lookup[n_typ.name],
                            f"Expected rule '{expected_rule_lookup[n_typ.name].type_name}' "
                            f"for type '{n_typ.name}', "
                            f"but got rule '{lookup[n_typ].type_name}' "
                            f"(while testing permutation '{permutation_name}')!"
                        )

    def test_get_record_types(self):
        """Test that the TRLC record types are extracted in the order given in the *.rsl"""
        expected_order = [
            "ZZ_Type",
            "Some_Unused_Type",
            "AA_Type",
            "BB_Type",
            "AA_Type_Addon",
        ]
        actual = [record_type.name for record_type
                  in get_record_types(self._trlc_data_provider.symbol_table)]
        self.assertListEqual(actual, expected_order)
