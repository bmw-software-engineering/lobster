from dataclasses import dataclass
from typing import Dict, Iterable, List
from trlc import ast

from lobster.tools.trlc.instruction import Instruction


@dataclass
class ToStringRules:
    """A set of rules for converting TRLC tuples to strings."""
    tuple_type_name: str
    package_name: str
    rules: List[List[Instruction]]


def build_tuple_type_to_ruleset_map(
    symbol_table: ast.Symbol_Table,
    to_string_rule_sets: Iterable[ToStringRules],
) -> Dict[ast.Tuple_Type, ToStringRules]:
    result = {}
    for n_pkg in symbol_table.values(ast.Package):
        for tuple_type in n_pkg.symbols.values(ast.Tuple_Type):
            for rule_set in to_string_rule_sets:
                if (tuple_type.name == rule_set.tuple_type_name) \
                        and (n_pkg.name == rule_set.package_name):
                    result[tuple_type] = rule_set
                    break
    return result
