#!/usr/bin/env python3
"""Install split/monolithic wheels and compare their installed payloads."""

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


def _collect_wheels(pattern: str) -> List[str]:
    wheels = sorted(glob.glob(pattern))
    if not wheels:
        raise RuntimeError(f"No wheels matched: {pattern}")
    return wheels


def _install_wheels(prefix: Path, wheels: List[str], root: Path) -> None:
    if prefix.exists():
        shutil.rmtree(prefix)

    # Makefile used `PYTHONPATH=` before each pip install invocation.
    env = os.environ.copy()
    env["PYTHONPATH"] = ""

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--prefix",
            str(prefix),
            *wheels,
        ],
        cwd=root,
        env=env,
    )


def _find_site_packages_lobster(prefix: Path) -> Path:
    matches = sorted(prefix.glob("lib/python*/site-packages/lobster"))
    if not matches:
        raise RuntimeError(f"No installed lobster package found under {prefix}")
    return matches[0]


def _run_diff(left: Path, right: Path, exclude: List[str]) -> None:
    cmd = ["diff", "-Naur", str(left), str(right)]
    for item in exclude:
        cmd.extend(["-x", item])
    subprocess.check_call(cmd)


def main() -> int:
    try:
        root = _workspace_root()

        # Makefile equivalent:
        #   pip3 install --prefix test_install packages/*/dist/*.whl
        split_wheels = _collect_wheels(str(root / "packages" / "*" / "dist" / "*.whl"))
        # Makefile equivalent:
        #   pip3 install --prefix test_install_monolithic \
        #       packages/lobster-monolithic/meta_dist/*.whl
        monolithic_wheels = _collect_wheels(
            str(root / "packages" / "lobster-monolithic" / "meta_dist" / "*.whl")
        )

        split_prefix = root / "test_install"
        monolithic_prefix = root / "test_install_monolithic"

        _install_wheels(split_prefix, split_wheels, root)
        _install_wheels(monolithic_prefix, monolithic_wheels, root)

        # Makefile equivalent:
        #   diff -Naur test_install/lib/python*/site-packages/lobster \
        #       test_install_monolithic/lib/python*/site-packages/lobster \
        #       -x "*.pyc" -x "*pkg*" -x "pkg/*"
        _run_diff(
            _find_site_packages_lobster(split_prefix),
            _find_site_packages_lobster(monolithic_prefix),
            ["*.pyc", "*pkg*", "pkg/*"],
        )

        # Makefile equivalent:
        #   diff -Naur test_install/bin test_install_monolithic/bin \
        #       -x "*pkg*" -x "pkg/*"
        _run_diff(
            split_prefix / "bin",
            monolithic_prefix / "bin",
            ["*pkg*", "pkg/*"],
        )
    except (RuntimeError, subprocess.CalledProcessError) as err:
        print(str(err), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
