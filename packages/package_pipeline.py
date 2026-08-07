#!/usr/bin/env python3
"""Run the full Bazelized package pipeline in Makefile order."""

import os
import subprocess
import sys
from pathlib import Path

from package_config import PACKAGE_ORDER


def _workspace_root() -> Path:
    workspace = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
    if not workspace:
        raise RuntimeError("This target must be run with 'bazel run'.")
    return Path(workspace)


def _run_script(script: Path, args: list[str], root: Path) -> None:
    subprocess.check_call([sys.executable, str(script), *args], cwd=root)


def main() -> int:
    try:
        root = _workspace_root()
        packages_dir = root / "packages"

        builder = packages_dir / "package_builder.py"
        install_diff = packages_dir / "package_install_diff.py"
        smoke_test = packages_dir / "package_smoke_test.py"

        # Makefile equivalent:
        #   $(BAZEL) run //packages:package_core
        #   ...
        #   $(BAZEL) run //packages:package_monolithic
        # Build all wheels in the same order as the Makefile recipe.
        for package_target in PACKAGE_ORDER:
            print(f"Building {package_target}...")
            _run_script(builder, [package_target], root)

        # Makefile equivalent block (formerly lines 67-74):
        #   pip3 install --prefix test_install packages/*/dist/*.whl
        #   pip3 install --prefix test_install_monolithic \
        #       packages/lobster-monolithic/meta_dist/*.whl
        #   diff -Naur .../site-packages/lobster .../site-packages/lobster ...
        #   diff -Naur test_install/bin test_install_monolithic/bin ...
        print("Running split-vs-monolithic install equivalence checks...")
        _run_script(install_diff, [], root)

        # Makefile equivalent smoke test block:
        #   python3 -m venv test_install_monolithic_venv
        #   . test_install_monolithic_venv/bin/activate && pip install ... &&
        #   lobster-<tool> --version (for all tools)
        print("Running monolithic wheel smoke test...")
        _run_script(smoke_test, [], root)
    except (RuntimeError, subprocess.CalledProcessError) as err:
        print(str(err), file=sys.stderr)
        return 1

    print("Package pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
