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
