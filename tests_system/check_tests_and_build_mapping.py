"""Detect tests_system test files not mapped to any py_test target."""

import re
import sys
from pathlib import Path


def _iter_py_test_blocks(build_text):
    """Return each py_test(...) block from the given BUILD file text."""
    blocks = []
    lines = build_text.splitlines()
    line_index = 0

    while line_index < len(lines):
        current_line = lines[line_index]
        if not re.match(r"^\s*py_test\s*\(", current_line):
            line_index += 1
            continue

        block_lines = [current_line]
        open_parens = current_line.count("(") - current_line.count(")")
        line_index += 1

        while line_index < len(lines) and open_parens > 0:
            current_line = lines[line_index]
            block_lines.append(current_line)
            open_parens += current_line.count("(") - current_line.count(")")
            line_index += 1

        blocks.append("\n".join(block_lines))

    return blocks


def _extract_test_srcs(build_text):
    """Return the test_*.py files referenced by py_test srcs lists."""
    test_names = set()

    for block in _iter_py_test_blocks(build_text):
        match = re.search(r"srcs\s*=\s*\[(.*?)\]", block, flags=re.DOTALL)
        if not match:
            continue

        for src in re.findall(r'"([^"]+\.py)"', match.group(1)):
            src_name = Path(src).name
            if src_name.startswith("test_"):
                test_names.add(src_name)

    return test_names


def _tool_directories(tests_system_dir):
    """Return the immediate subdirectories in tests_system that may contain tests."""
    tool_dirs = []

    for entry in sorted(tests_system_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith((".", "__")):
            continue
        tool_dirs.append(entry)

    return tool_dirs


def main():
    workspace_root = Path(__file__).resolve().parent.parent
    tests_system_dir = workspace_root / "tests_system"

    missing_build_dirs = []
    missing_test_files = []
    stale_test_entries = []
    discovered_tests = set()
    declared_tests = set()

    for tool_dir in _tool_directories(tests_system_dir):
        test_files = set()
        for test_file in tool_dir.glob("test_*.py"):
            test_files.add(test_file.relative_to(workspace_root).as_posix())

        if not test_files:
            continue

        discovered_tests.update(test_files)

        build_file = tool_dir / "BUILD.bazel"
        tool_name = tool_dir.relative_to(workspace_root).as_posix()

        if not build_file.is_file():
            missing_build_dirs.append(tool_name)
            continue

        listed_tests = set()
        for test_name in _extract_test_srcs(build_file.read_text(encoding="utf-8")):
            listed_tests.add(f"{tool_name}/{test_name}")

        declared_tests.update(listed_tests)

        for test_path in sorted(test_files - listed_tests):
            missing_test_files.append(test_path)

        for test_path in sorted(listed_tests - test_files):
            stale_test_entries.append(test_path)

    has_errors = any([
        missing_build_dirs,
        missing_test_files,
        stale_test_entries,
        len(discovered_tests) != len(declared_tests),
    ])
    if not has_errors:
        return 0

    print("ERROR: tests_system BUILD mapping check failed.")
    if len(discovered_tests) != len(declared_tests):
        print(
            "Mismatch between tests_system test file count "
            "and BUILD.bazel py_test target count."
        )
    if missing_build_dirs:
        print("These folders contain tests but are missing a BUILD.bazel file:")
        for tool_name in missing_build_dirs:
            print(f"  - {tool_name}")
    if missing_test_files:
        print("These test files exist, but are not listed in BUILD.bazel:")
        for test_path in missing_test_files:
            print(f"  - {test_path}")
    if stale_test_entries:
        print("BUILD.bazel lists these tests, but their test files are missing:")
        for test_path in stale_test_entries:
            print(f"  - {test_path}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
