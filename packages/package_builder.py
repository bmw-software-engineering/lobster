#!/usr/bin/env python3
"""Build lobster wheels by staging files expected by each setup.py."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

from package_config import PACKAGE_DIR_MAP, PACKAGE_ORDER, TOOL_PACKAGE_MAP

def _workspace_root() -> Path:
    workspace = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
    if not workspace:
        raise RuntimeError("This target must be run with 'bazel run'.")
    return Path(workspace)


def _build_wheel(package_dir: Path) -> None:
    # Makefile equivalent: @python3 -m build --wheel
    subprocess.check_call([sys.executable, "-m", "build", "--wheel"], cwd=package_dir)


def _prepare_tool_package(root: Path, package_dir: Path, tool_name: str) -> None:
    # Makefile template used by tool packages (trlc/codebeamer/cpp/cpptest/gtest/json/python):
    #   rm -rf lobster
    #   mkdir -p lobster/tools
    #   cp $(LOBSTER_ROOT)/lobster/__init__.py lobster
    #   cp -Rv $(LOBSTER_ROOT)/lobster/common lobster
    #   cp -Rv $(LOBSTER_ROOT)/lobster/tools/<tool_name> lobster/tools
    staged_lobster = package_dir / "lobster"
    staged_tools = staged_lobster / "tools"

    if staged_lobster.exists():
        shutil.rmtree(staged_lobster)

    staged_tools.mkdir(parents=True, exist_ok=True)

    shutil.copy2(root / "lobster" / "__init__.py", staged_lobster)
    shutil.copytree(root / "lobster" / "common", staged_lobster / "common")
    shutil.copytree(root / "lobster" / "tools" / tool_name, staged_tools / tool_name)


def _prepare_core_package(root: Path, package_dir: Path) -> None:
    # Makefile equivalent for lobster-core:
    #   rm -rf lobster
    #   mkdir -p lobster/tools
    #   cp $(LOBSTER_ROOT)/lobster/*.py lobster
    #   cp -Rv $(LOBSTER_ROOT)/lobster/common lobster
    #   cp -Rv $(LOBSTER_ROOT)/lobster/htmldoc lobster
    #   cp $(LOBSTER_ROOT)/lobster/tools/*.py lobster/tools
    #   cp -Rv $(LOBSTER_ROOT)/lobster/tools/core lobster/tools
    staged_lobster = package_dir / "lobster"
    staged_tools = staged_lobster / "tools"

    if staged_lobster.exists():
        shutil.rmtree(staged_lobster)

    staged_tools.mkdir(parents=True, exist_ok=True)

    for src_file in (root / "lobster").glob("*.py"):
        shutil.copy2(src_file, staged_lobster)

    shutil.copytree(root / "lobster" / "common", staged_lobster / "common")
    shutil.copytree(root / "lobster" / "htmldoc", staged_lobster / "htmldoc")

    for src_file in (root / "lobster" / "tools").glob("*.py"):
        shutil.copy2(src_file, staged_tools)

    shutil.copytree(root / "lobster" / "tools" / "core", staged_tools / "core")


def _prepare_metapackage(root: Path, package_dir: Path) -> None:
    # Makefile equivalent for lobster-metapackage:
    #   rm -rf lobster
    #   mkdir -p lobster
    #   cp $(LOBSTER_ROOT)/lobster/__init__.py lobster
    #   cp -Rv $(LOBSTER_ROOT)/lobster/common lobster
    staged_lobster = package_dir / "lobster"

    if staged_lobster.exists():
        shutil.rmtree(staged_lobster)

    staged_lobster.mkdir(parents=True, exist_ok=True)

    shutil.copy2(root / "lobster" / "__init__.py", staged_lobster)
    shutil.copytree(root / "lobster" / "common", staged_lobster / "common")


def _prepare_monolithic(root: Path, package_dir: Path) -> None:
    # Makefile equivalent for lobster-monolithic pre-build stage:
    #   rm -rf lobster dist meta_dist
    #   cp -Rv $(LOBSTER_ROOT)/lobster lobster
    staged_lobster = package_dir / "lobster"
    dist_dir = package_dir / "dist"
    meta_dist_dir = package_dir / "meta_dist"

    for path in (staged_lobster, dist_dir, meta_dist_dir):
        if path.exists():
            shutil.rmtree(path)

    shutil.copytree(root / "lobster", staged_lobster)


def build_package(package_target: str) -> None:
    root = _workspace_root()

    if package_target not in PACKAGE_DIR_MAP:
        raise KeyError(f"Unknown package target: {package_target}")

    package_dir = root / "packages" / PACKAGE_DIR_MAP[package_target]

    if package_target in TOOL_PACKAGE_MAP:
        _prepare_tool_package(root, package_dir, TOOL_PACKAGE_MAP[package_target])
        _build_wheel(package_dir)
        return

    if package_target == "package_core":
        _prepare_core_package(root, package_dir)
        _build_wheel(package_dir)
        return

    if package_target == "package_metapackage":
        _prepare_metapackage(root, package_dir)
        _build_wheel(package_dir)
        return

    if package_target == "package_monolithic":
        _prepare_monolithic(root, package_dir)
        _build_wheel(package_dir)
        # Makefile post-build equivalent: mv dist meta_dist
        dist_dir = package_dir / "dist"
        meta_dist_dir = package_dir / "meta_dist"

        if not dist_dir.exists():
            raise RuntimeError("Wheel build did not produce dist directory")

        if meta_dist_dir.exists():
            shutil.rmtree(meta_dist_dir)

        dist_dir.rename(meta_dist_dir)
        return

    raise KeyError(f"Unsupported package target: {package_target}")


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        targets = ", ".join(PACKAGE_ORDER)
        print(f"Usage: {argv[0]} <package-target>", file=sys.stderr)
        print(f"Known targets: {targets}", file=sys.stderr)
        return 2

    try:
        build_package(argv[1])
    except (RuntimeError, KeyError) as err:
        print(str(err), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
