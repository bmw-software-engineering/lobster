from typing import Dict, Iterable
from trlc import ast

from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.hierarchy_tree import HierarchyTree


def build_record_type_to_conversion_rule_lookup(
        conversion_rules: Iterable[ConversionRule],
        children_lookup: HierarchyTree,
        symbol_table: ast.Symbol_Table,
) -> Dict[ast.Record_Type, ConversionRule]:
    """Iterates over all TRLC record types and generates a lookup dictionary
       that also propagates conversion rules to derived record types (depending
       on the value of ConversionRule.applies_to_derived_types).

       That is, derived types can be looked up, too, and will return the
       conversion rule of their parent type.
       If a specific conversion rule is defined for a derived type, then the order
       of the rules in the input list does not matter.
       Only the order of the record types in the symbol table matters.
       TRLC preserves the order of record types as found in the *.rsl files.

       Example:
       *.rsl defines these types in the given order:
       type Level1 {}
       type Level2 extends Level1 {}

       Then any record object of Level2 will be converted using the
       conversion rule for Level1, unless there is a specific conversion rule
       for Level2 in the input list of conversion rules.

       Note: The ConversionRule instance specifies only the record type name and
       namespace, but not the concrete record type instance. That's why we need this
       function after all.
       This function searches for the concrete record type instance in the symbol table,
       and then builds a lookup between the record types and their conversion rules.

       If 'conversion_rules' contains a rule for a record type that is not
       present in the symbol table, then that rule is ignored.
    """
    result = {}
    # build temporary lookup based on fully qualified name of record type:
    temporary_lookup = {(rule.package_name, rule.type_name): rule
                        for rule in conversion_rules}
    # iterate over all record types in the symbol table
    # and build the final lookup:
    for record_type in get_record_types(symbol_table):
        fully_qualified_name = (record_type.n_package.name, record_type.name)
        rule = temporary_lookup.get(fully_qualified_name)
        if rule:
            result[record_type] = rule
            if rule.applies_to_derived_types:
                _propagate_rule_to_derived_types_recursively(
                    parent_extraction_rule=result[record_type],
                    parent_record_type=record_type,
                    children_lookup=children_lookup,
                    extraction_rules_lookup=result,
                )
    return result


def _propagate_rule_to_derived_types_recursively(
        parent_extraction_rule: ConversionRule,
        parent_record_type: ast.Record_Type,
        children_lookup: HierarchyTree,
        extraction_rules_lookup: Dict[ast.Record_Type, ConversionRule]
):
    child_types = children_lookup.get(parent_record_type)
    if child_types:
        for child_type in child_types:
            extraction_rules_lookup[child_type] = parent_extraction_rule
            _propagate_rule_to_derived_types_recursively(
                parent_extraction_rule,
                child_type,
                children_lookup,
                extraction_rules_lookup,
            )


def get_record_types(symbol_table: ast.Symbol_Table) -> Iterable[ast.Record_Type]:
    """Returns an iterable of all record types in the TRLC symbol table
       while preserving the order.
    """

    # Note: The intuitive way to get all record types is to iterate like this:
    # for n_pkg in symbol_table.values(ast.Package):
    #     yield from n_pkg.symbols.values(ast.Record_Type)
    # Unfortunately the "ast.Symbol_Table.values" function returns the symbols in an
    # alphabetically sorted order!
    # So we have to implement our own iteration to preserve the order

    for n_pkg in symbol_table.values(ast.Package):
        table = n_pkg.symbols.table
        for value in table.values():
            if isinstance(value, ast.Record_Type):
                yield value
