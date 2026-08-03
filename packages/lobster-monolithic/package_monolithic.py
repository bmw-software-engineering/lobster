#!/usr/bin/env python3
"""Build the lobster-monolithic wheel by staging files expected by setup.py."""

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
    package_dir = root / "packages" / "lobster-monolithic"
    staged_lobster = package_dir / "lobster"
    dist_dir = package_dir / "dist"
    meta_dist_dir = package_dir / "meta_dist"

    # make: rm -rf lobster dist meta_dist
    for path in (staged_lobster, dist_dir, meta_dist_dir):
        if path.exists():
            shutil.rmtree(path)

    # make: cp -Rv $(LOBSTER_ROOT)/lobster lobster
    shutil.copytree(root / "lobster", staged_lobster)

    # make: @python3 -m build --wheel
    subprocess.check_call([sys.executable, "-m", "build", "--wheel"], cwd=package_dir)
    # make: mv dist meta_dist
    dist_dir.rename(meta_dist_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
