#!/usr/bin/env python3
"""Build the lobster-core wheel by staging files expected by setup.py."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    workspace = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
    if not workspace:
        print("This target must be run with 'bazel run'.", file=sys.stderr)
        return 1

    root = Path(workspace)
    package_dir = root / "packages" / "lobster-core"
    staged_lobster = package_dir / "lobster"
    staged_tools = staged_lobster / "tools"

    # make: rm -rf lobster
    if staged_lobster.exists():
        shutil.rmtree(staged_lobster)

    # make: mkdir -p lobster/tools
    staged_tools.mkdir(parents=True, exist_ok=True)

    # make: cp $(LOBSTER_ROOT)/lobster/*.py lobster
    for src_file in (root / "lobster").glob("*.py"):
        shutil.copy2(src_file, staged_lobster)

    # make: cp -Rv $(LOBSTER_ROOT)/lobster/common lobster
    shutil.copytree(root / "lobster" / "common", staged_lobster / "common")
    # make: cp -Rv $(LOBSTER_ROOT)/lobster/htmldoc lobster
    shutil.copytree(root / "lobster" / "htmldoc", staged_lobster / "htmldoc")

    # make: cp $(LOBSTER_ROOT)/lobster/tools/*.py lobster/tools
    for src_file in (root / "lobster" / "tools").glob("*.py"):
        shutil.copy2(src_file, staged_tools)

    # make: cp -Rv $(LOBSTER_ROOT)/lobster/tools/core lobster/tools
    shutil.copytree(root / "lobster" / "tools" / "core", staged_tools / "core")

    # make: @python3 -m build --wheel
    subprocess.check_call([sys.executable, "-m", "build", "--wheel"], cwd=package_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
