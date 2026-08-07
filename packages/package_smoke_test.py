#!/usr/bin/env python3
"""Run a basic post-package smoke test for the monolithic wheel."""

import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def _workspace_root() -> Path:
    workspace = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
    if not workspace:
        raise RuntimeError("This target must be run with 'bazel run'.")
    return Path(workspace)


def _monolithic_wheels(root: Path) -> List[str]:
    pattern = str(root / "packages" / "lobster-monolithic" / "meta_dist" / "*.whl")
    wheels = sorted(glob.glob(pattern))
    if not wheels:
        raise RuntimeError(f"No wheels matched: {pattern}")
    return wheels


def main() -> int:
    try:
        root = _workspace_root()
        venv_dir = root / "test_install_monolithic_venv"

        # Makefile equivalent:
        #   python3 -m venv test_install_monolithic_venv
        # This creates an isolated environment to verify packaged entrypoints.
        if venv_dir.exists():
            shutil.rmtree(venv_dir)
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)], cwd=root)

        venv_python = venv_dir / "bin" / "python"

        # Makefile equivalent:
        #   . test_install_monolithic_venv/bin/activate && \
        #       pip install --upgrade pip
        # Instead of shell activation, call the venv python directly for determinism.
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], cwd=root)

        # Makefile equivalent:
        #   pip install packages/lobster-monolithic/meta_dist/*.whl
        subprocess.check_call(
            [str(venv_python), "-m", "pip", "install", *_monolithic_wheels(root)],
            cwd=root,
        )

        # Makefile equivalent tool checks:
        #   lobster-report --version && ... && lobster-rst-report --version
        # This verifies that console scripts are installed and executable.
        tools = [
            "lobster-report",
            "lobster-ci-report",
            "lobster-html-report",
            "lobster-online-report",
            "lobster-online-report-nogit",
            "lobster-cpp",
            "lobster-cpptest",
            "lobster-codebeamer",
            "lobster-gtest",
            "lobster-json",
            "lobster-python",
            "lobster-trlc",
            "lobster-pkg",
            "lobster-rst-report",
        ]
        for tool in tools:
            subprocess.check_call([str(venv_dir / "bin" / tool), "--version"], cwd=root)
    except (RuntimeError, subprocess.CalledProcessError) as err:
        print(str(err), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
