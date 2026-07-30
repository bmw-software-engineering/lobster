#!/usr/bin/env python3
"""Build all lobster package wheels in Makefile-compatible order."""

import os
import subprocess
import sys
from pathlib import Path


PACKAGE_ORDER = [
    ("lobster-core", "package_core.py"),
    ("lobster-tool-trlc", "package_trlc.py"),
    ("lobster-tool-codebeamer", "package_codebeamer.py"),
    ("lobster-tool-cpp", "package_cpp.py"),
    ("lobster-tool-cpptest", "package_cpp_test.py"),
    ("lobster-tool-gtest", "package_gtest.py"),
    ("lobster-tool-json", "package_json.py"),
    ("lobster-tool-python", "package_python.py"),
    ("lobster-metapackage", "package_metapackage.py"),
    ("lobster-monolithic", "package_monolithic.py"),
]


def main() -> int:
    workspace = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
    if not workspace:
        print("This target must be run with 'bazel run'.", file=sys.stderr)
        return 1

    root = Path(workspace)
    env = os.environ.copy()
    env["BUILD_WORKSPACE_DIRECTORY"] = str(root)

    for package, script_name in PACKAGE_ORDER:
        package_script = root / "packages" / package / script_name
        print(f"Building {package}...")
        subprocess.check_call([sys.executable, str(package_script)], env=env)

    print("All package wheels built successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
