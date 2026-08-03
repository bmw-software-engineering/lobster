#!/usr/bin/env python3
"""Build the lobster-tool-trlc wheel by staging files expected by setup.py."""

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
    package_dir = root / "packages" / "lobster-tool-trlc"
    staged_lobster = package_dir / "lobster"
    staged_tools = staged_lobster / "tools"

    # make: rm -rf lobster
    if staged_lobster.exists():
        shutil.rmtree(staged_lobster)

    # make: mkdir -p lobster/tools
    staged_tools.mkdir(parents=True, exist_ok=True)

    # make: cp $(LOBSTER_ROOT)/lobster/__init__.py lobster
    shutil.copy2(root / "lobster" / "__init__.py", staged_lobster)
    # make: cp -Rv $(LOBSTER_ROOT)/lobster/common lobster
    shutil.copytree(root / "lobster" / "common", staged_lobster / "common")
    # make: cp -Rv $(LOBSTER_ROOT)/lobster/tools/trlc lobster/tools
    shutil.copytree(root / "lobster" / "tools" / "trlc", staged_tools / "trlc")

    # make: @python3 -m build --wheel
    subprocess.check_call([sys.executable, "-m", "build", "--wheel"], cwd=package_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
