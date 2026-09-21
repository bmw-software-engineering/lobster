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

from collections import defaultdict
from typing import Dict, Set
from trlc import ast


HierarchyTree = Dict[ast.Record_Type, Set[ast.Record_Type]]


def build_children_lookup(symbol_table: ast.Symbol_Table) -> HierarchyTree:
    """Builds a lookup dictionary for child record types of each record type in the
       symbol table."""
    lookup = defaultdict(set)
    for n_pkg in symbol_table.values(ast.Package):
        for n_typ in n_pkg.symbols.values(ast.Record_Type):
            if n_typ.parent:
                lookup[n_typ.parent].add(n_typ)
    return dict(lookup)
