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
       that also propagates conversion rules to derived record types.

       That is, derived types can be looked up, too, and will return the
       conversion rule of their parent type.
       If a specific conversion rule is defined for a derived type, then the order
       of the rules in the input matters. The last rule for a record type wins.

       The ConversionRule instance specifies only the record type name and namespace,
       but not the concrete record type instance.

       This class searches for the concrete record type instance in the symbol table,
       and then builds a lookup between the record types and their conversion rules.
    """
    # build the plain lookup
    extraction_rules_lookup = _build_type_to_rule_map(symbol_table, conversion_rules)
    # enrich the lookup with rules for derived record types
    _extend_with_derived_types(symbol_table, extraction_rules_lookup, children_lookup)
    return extraction_rules_lookup


def _extend_with_derived_types(
        symbol_table: ast.Symbol_Table,
        extraction_rules_lookup: Dict[ast.Record_Type, ConversionRule],
        children_lookup: HierarchyTree,
):
    for n_pkg in symbol_table.values(ast.Package):
        for n_typ in n_pkg.symbols.values(ast.Record_Type):
            extraction_rule = extraction_rules_lookup.get(n_typ)
            if extraction_rule and extraction_rule.applies_to_derived_types:
                _propagate_rule_to_derived_types_recursively(
                    extraction_rule,
                    n_typ,
                    children_lookup,
                    extraction_rules_lookup,
                )


def _build_type_to_rule_map(
    symbol_table: ast.Symbol_Table,
    extraction_rules: Iterable[ConversionRule],
) -> Dict[ast.Record_Type, ConversionRule]:
    result = {}
    for n_pkg in symbol_table.values(ast.Package):
        for n_typ in n_pkg.symbols.values(ast.Record_Type):
            for rule in extraction_rules:
                if (n_typ.name == rule.type_name) and (n_pkg.name == rule.package_name):
                    result[n_typ] = rule
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
            extraction_rules_lookup.setdefault(child_type, parent_extraction_rule)
            _propagate_rule_to_derived_types_recursively(
                parent_extraction_rule,
                child_type,
                children_lookup,
                extraction_rules_lookup,
            )
