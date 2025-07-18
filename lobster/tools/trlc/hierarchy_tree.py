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
