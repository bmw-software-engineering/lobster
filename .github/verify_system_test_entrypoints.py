#!/usr/bin/env python3
"""Verify that all system tests have a proper unittest main guard."""

import ast
import pathlib
import sys


def _collect_unittest_aliases(tree):
    unittest_names = {"unittest"}
    main_names = set()

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "unittest":
                    unittest_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "unittest":
            for alias in node.names:
                if alias.name == "main":
                    main_names.add(alias.asname or alias.name)

    return unittest_names, main_names


def _is_main_guard_test(expr):
    if not isinstance(expr, ast.Compare):
        return False
    if len(expr.ops) != 1 or not isinstance(expr.ops[0], ast.Eq):
        return False
    if len(expr.comparators) != 1:
        return False

    left = expr.left
    right = expr.comparators[0]

    left_name = isinstance(left, ast.Name) and left.id == "__name__"
    right_name = isinstance(right, ast.Name) and right.id == "__name__"
    left_main = isinstance(left, ast.Constant) and left.value == "__main__"
    right_main = isinstance(right, ast.Constant) and right.value == "__main__"

    return (left_name and right_main) or (left_main and right_name)


def _contains_main_call(node, unittest_names, main_names):
    if not isinstance(node, ast.Call):
        return False

    func = node.func
    if (isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id in unittest_names
            and func.attr == "main"):
        return True

    if isinstance(func, ast.Name) and func.id in main_names:
        return True

    for arg in node.args:
        if _contains_main_call(arg, unittest_names, main_names):
            return True
    for kw in node.keywords:
        if _contains_main_call(kw.value, unittest_names, main_names):
            return True
    return False


def has_main_guard(path):
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (OSError, UnicodeDecodeError, SyntaxError) as exc:
        return False, f"parse error: {exc}"

    unittest_names, main_names = _collect_unittest_aliases(tree)

    for node in tree.body:
        if isinstance(node, ast.If) and _is_main_guard_test(node.test):
            body = node.body
            if len(body) != 1:
                return False, "__main__ guard must contain exactly one statement"

            stmt = body[0]
            call = stmt.value if isinstance(stmt, ast.Expr) else None
            if isinstance(stmt, ast.Return):
                call = stmt.value

            if call is None or not _contains_main_call(call, unittest_names, main_names):
                return False, "__main__ guard must call unittest.main()"
            return True, ""

    return False, "missing __main__ guard"


missing = []
for p in pathlib.Path("tests_system").rglob("test_*.py"):
    ok, reason = has_main_guard(p)
    if not ok:
        missing.append((p, reason))

if missing:
    print("ERROR: one or more system tests are missing unittest main guard.")
    print("\n".join(f"Missing unittest entrypoint: {p} ({reason})" for p, reason in missing))
    sys.exit(1)
