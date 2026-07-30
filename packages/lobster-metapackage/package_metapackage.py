#!/usr/bin/env python3
"""Build the lobster-metapackage wheel by staging files expected by setup.py."""

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
    package_dir = root / "packages" / "lobster-metapackage"
    staged_lobster = package_dir / "lobster"

    if staged_lobster.exists():
        shutil.rmtree(staged_lobster)

    staged_lobster.mkdir(parents=True, exist_ok=True)

    shutil.copy2(root / "lobster" / "__init__.py", staged_lobster)
    shutil.copytree(root / "lobster" / "common", staged_lobster / "common")

    subprocess.check_call([sys.executable, "-m", "build", "--wheel"], cwd=package_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
