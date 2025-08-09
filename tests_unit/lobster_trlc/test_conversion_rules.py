from pathlib import Path
from unittest import TestCase
from trlc.errors import Message_Handler
from trlc.trlc import Source_Manager
from trlc import ast

from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.hierarchy_tree import build_children_lookup
from lobster.tools.trlc.conversion_rule_lookup import build_record_type_to_conversion_rule_lookup


class ConversionRulesTest(TestCase):
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
        self._sm = Source_Manager(Message_Handler())
        rsl_file = Path(__file__).parent / "data" / "hierarchy_tree.rsl"
        self._sm.register_file(str(rsl_file))
        self._symbol_table = self._sm.process()
        self.assertIsNotNone(
            self._symbol_table,
            "Invalid test setup: Failed to process TRLC data!",
        )

    def test_empty_conversion_rule_lookup(self):
        result = build_record_type_to_conversion_rule_lookup(
            conversion_rules=[],
            children_lookup=build_children_lookup(self._symbol_table),
            symbol_table=self._symbol_table,
        )
        self.assertDictEqual(
            result,
            {},
            "Expected empty conversion rule lookup for empty extraction rules.",
        )

    def test_one_conversion_rule_for_all(self):
        extraction_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=True,
            namespace="req",
        )

        result = build_record_type_to_conversion_rule_lookup(
            conversion_rules=[extraction_rule],
            children_lookup=build_children_lookup(self._symbol_table),
            symbol_table=self._symbol_table,
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(self._EXPECTED_CHILDREN))

        for n_pkg in self._symbol_table.values(ast.Package):
            for n_typ in n_pkg.symbols.values(ast.Record_Type):
                self.assertIn(
                    n_typ,
                    result,
                    f"Record type '{n_typ.name}' not found in conversion rule lookup.",
                )
                self.assertIs(result[n_typ], extraction_rule)

    def test_many_conversion_rules(self):
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
            "Level2B": top_rule,
            "Level3A": top_rule,
            "Level3B": rule_level3b,
            "Level4A": top_rule,
            "Level4B": top_rule,
        }

        result = build_record_type_to_conversion_rule_lookup(
            conversion_rules=[top_rule, rule_level2a, rule_level3b],
            children_lookup=build_children_lookup(self._symbol_table),
            symbol_table=self._symbol_table,
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(self._EXPECTED_CHILDREN))

        for n_pkg in self._symbol_table.values(ast.Package):
            for n_typ in n_pkg.symbols.values(ast.Record_Type):
                self.assertIn(
                    n_typ,
                    result,
                    f"Record type '{n_typ.name}' not found in conversion rule lookup.",
                )
                self.assertIs(result[n_typ], expected_rule_lookup[n_typ.name])

    def test_no_propagation(self):
        extraction_rule = ConversionRule(
            record_type="Level1",
            package="hierarchy_tree_test",
            applies_to_derived_types=False,
            namespace="req",
        )

        result = build_record_type_to_conversion_rule_lookup(
            conversion_rules=[extraction_rule],
            children_lookup=build_children_lookup(self._symbol_table),
            symbol_table=self._symbol_table,
        )

        self.assertEqual(len(result), 1)

        for n_pkg in self._symbol_table.values(ast.Package):
            for n_typ in n_pkg.symbols.values(ast.Record_Type):
                if n_typ.name == extraction_rule.type_name:
                    self.assertIn(n_typ, result)

    def test_record_type_child_lookup(self):
        children_lookup = build_children_lookup(self._symbol_table)
        for n_pkg in self._symbol_table.values(ast.Package):
            for n_typ in n_pkg.symbols.values(ast.Record_Type):
                children_names = {child.name for child in children_lookup.get(n_typ, set())}
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
