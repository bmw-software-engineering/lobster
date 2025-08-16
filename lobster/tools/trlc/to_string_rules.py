from dataclasses import dataclass
from typing import Dict, Iterable, List
from trlc import ast

from lobster.tools.trlc.instruction import Instruction
from lobster.tools.trlc.text_generation import parse_instructions


@dataclass
class ToStringRules:
    """A set of rules for converting TRLC tuples to strings."""
    tuple_type_name: str
    package_name: str
    rules: List[List[Instruction]]

    @staticmethod
    def from_dict(data: dict) -> "ToStringRules":
        return ToStringRules(
            tuple_type_name=data["tuple-type"],
            package_name=data["package"],
            rules=[parse_instructions(to_string_line)
                   for to_string_line in data.get("to-string", [])],
        )


def build_tuple_type_to_ruleset_map(
    symbol_table: ast.Symbol_Table,
    to_string_rule_sets: Iterable[ToStringRules],
) -> Dict[ast.Tuple_Type, ToStringRules]:
    """Iterates over all tuple types in the symbol table and returns a mapping
       from tuple types to their corresponding ToStringRules.
    """
    result = {}
    for n_pkg in symbol_table.values(ast.Package):
        for tuple_type in n_pkg.symbols.values(ast.Tuple_Type):
            for rule_set in to_string_rule_sets:
                if (tuple_type.name == rule_set.tuple_type_name) \
                        and (n_pkg.name == rule_set.package_name):
                    result[tuple_type] = rule_set
                    break
    return result
