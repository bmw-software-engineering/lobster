import itertools
from pathlib import Path
from unittest import TestCase

from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.hierarchy_tree import build_children_lookup
from lobster.tools.trlc.conversion_rule_lookup import build_record_type_to_conversion_rule_lookup
from tests_unit.lobster_trlc.trlc_data_provider import TrlcDataProvider


class ConversionRulesTest(TestCase):
    """Tests in this class focus on conversion rules. They test e.g. that a conversion
       rule for a TRLC record type is correctly applied to all its derived TRLC record
       types.
    """
    # Note: This class does not inherit from `TrlcHierarchyDataTestCase` because it does
    # not need the *.trlc file, only the *.rsl file.

    _EXPECTED_CHILDREN = {
        "Level1": {"Level2A", "Level2B"},
        "Level2A": {"Level3A"},
        "Level2B": {"Level3B"},
        "Level3A": {"Level4A"},
        "Level3B": {"Level4B"},
        "Level4A": set(),
        "Level4B": set(),
    }


    def setUp(self) -> None:
        self._trlc_data_provider = TrlcDataProvider(
            callback_test_case=self,
            trlc_input_files=[
                Path(__file__).parent / "data" / "hierarchy_tree.rsl",
            ],
            expected_record_type_names=set(self._EXPECTED_CHILDREN.keys()),
        )
        super().setUp()

    def test_empty_conversion_rule_lookup(self):
        """Tests that an empty list of conversion rules results in an empty lookup."""
        result = build_record_type_to_conversion_rule_lookup(
            conversion_rules=[],
            children_lookup=build_children_lookup(self._trlc_data_provider.symbol_table),
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        self.assertDictEqual(
            result,
            {},
            "Expected empty lookup for empty list of conversion rules.",
        )

    def test_one_conversion_rule_for_all(self):
        """Tests that a single conversion rule is applied to all record types"""
        extraction_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
        )

        result = build_record_type_to_conversion_rule_lookup(
            conversion_rules=[extraction_rule],
            children_lookup=build_children_lookup(self._trlc_data_provider.symbol_table),
            symbol_table=self._trlc_data_provider.symbol_table,
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(self._EXPECTED_CHILDREN))

        for n_typ in self._trlc_data_provider.get_record_types():
            self.assertIn(
                n_typ,
                result,
                f"Record type '{n_typ.name}' not found in conversion rule lookup.",
            )
            self.assertIs(result[n_typ], extraction_rule)

    def test_many_propagating_conversion_rules(self):
        """Tests that the correct conversion rule is applied to each record type in a
           scenario where one TRLC record type is derived from another.
        """
        top_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
        )
        rule_level2a = ConversionRule(
            record_type="Level2A",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
        )
        rule_level3b = ConversionRule(
            record_type="Level3B",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
        )
        expected_rule_lookup = {
            "Level1": top_rule,
            "Level2A": rule_level2a,
            "Level3A": rule_level2a,
            "Level4A": rule_level2a,
            "Level2B": top_rule,
            "Level3B": rule_level3b,
            "Level4B": rule_level3b,
        }

        # We repeat the test for all 6 permutations of the rules to ensure that
        # the order of rules does not affect the result.
        for permutation in itertools.permutations(
            [top_rule, rule_level2a, rule_level3b],
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
                self.assertEqual(len(lookup), len(self._EXPECTED_CHILDREN))

                for n_typ in self._trlc_data_provider.get_record_types():
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

    def test_no_propagation(self):
        """Tests that a conversion rule is not propagated to derived types if
           'applies_to_derived_types' is set to False.
        """
        extraction_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=False,
            namespace="req",
        )

        result = build_record_type_to_conversion_rule_lookup(
            conversion_rules=[extraction_rule],
            children_lookup=build_children_lookup(self._trlc_data_provider.symbol_table),
            symbol_table=self._trlc_data_provider.symbol_table,
        )

        self.assertEqual(len(result), 1)

        for n_typ in self._trlc_data_provider.get_record_types():
            if n_typ.name == extraction_rule.type_name:
                self.assertIn(n_typ, result)

    def test_record_type_child_lookup(self):
        """Tests that the parent-child lookup of TRLC record types is built correctly."""
        children_lookup = build_children_lookup(self._trlc_data_provider.symbol_table)
        for n_typ in self._trlc_data_provider.get_record_types():
            children_names = {
                child.name for child in children_lookup.get(n_typ, set())
            }
            try:
                expectation = self._EXPECTED_CHILDREN[n_typ.name]
            except KeyError:
                self.fail(f"Unexpected record type '{n_typ.name}' "
                            f"found in hierarchy tree.")
            self.assertSetEqual(
                children_names,
                expectation,
                f"Children of {n_typ.name} do not match expected values."
            )
