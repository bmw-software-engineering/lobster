#!/usr/bin/env python3
"""Build all lobster package wheels in Makefile-compatible order."""

import os
import subprocess
import sys
from pathlib import Path

from package_config import PACKAGE_ORDER

def main() -> int:
    workspace = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
    if not workspace:
        print("This target must be run with 'bazel run'.", file=sys.stderr)
        return 1

    root = Path(workspace)
    env = os.environ.copy()
    env["BUILD_WORKSPACE_DIRECTORY"] = str(root)

    package_script = root / "packages" / "package_builder.py"
    for package_target in PACKAGE_ORDER:
        print(f"Building {package_target}...")
        subprocess.check_call([sys.executable, str(package_script), package_target], env=env)

    print("All package wheels built successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
