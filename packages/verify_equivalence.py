#!/usr/bin/env python3

#   IGNORE THIS FILE. IT IS USED FOR TESTING IF THE MAKEFILE 
#   AND THE PACKAGE SCRIPT PRODUCE THE SAME RESULTS.

"""Validate packaging equivalence between Makefile and package scripts.

This script verifies that each selected package under packages/ produces the
same results when built via two independent packaging paths:
1) `make package` from that package directory, and
2) the package's corresponding `package_*.py` script.

For each package, it creates isolated temporary workspaces, runs both flows,
and compares outputs at two levels:
- staged source tree (`lobster/` directory in each package), and
- wheel archive payload (`*.whl` contents).

Wheel comparison intentionally ignores only `.dist-info/RECORD`, because that
file is expected to vary due to generated metadata (hashes/sizes/order). Any
other difference (missing files, extra files, or byte-level content mismatch)
is reported as a failure.

Exit behavior:
- returns 0 only when all requested packages are equivalent in both checks;
- returns 1 if any package fails comparison or a required artifact is missing.

Usage:
    # Run for a specific package:
    python3 packages/verify_equivalence.py lobster-core

    # Run for multiple packages:
    python3 packages/verify_equivalence.py lobster-core lobster-metapackage

    # Run for ALL packages under packages/:
    python3 packages/verify_equivalence.py

    # Write a machine-readable CI summary:
    python3 packages/verify_equivalence.py --summary-json verify_summary.json

    # Ignore permission/mode comparisons (cross-platform tolerance):
    python3 packages/verify_equivalence.py --ignore-permissions
"""

import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


# Build a copy of the current environment with the active Python's bin directory
# prepended to PATH, so subprocesses use the same Python and tools.
def build_env() -> dict[str, str]:
    env = dict(os.environ)
    python_bin = str(Path(sys.executable).parent)
    env["PATH"] = f"{python_bin}:{env.get('PATH', '')}"
    return env


# Locate the one package_*.py script inside a package directory.
# Raises an error if none or more than one is found.
def find_package_script(package_dir: Path) -> Path:
    """Return the single package_*.py script in the package directory."""
    scripts = sorted(package_dir.glob("package_*.py"))
    if not scripts:
        raise RuntimeError(
            f"No package_*.py script found in {package_dir}"
        )
    if len(scripts) > 1:
        raise RuntimeError(
            f"Multiple package_*.py scripts found in {package_dir}: {scripts}"
        )
    return scripts[0]


# Find the output directory ('dist' or 'meta_dist') created after a build.
# Raises an error if neither exists.
def find_dist_dir(package_dir: Path) -> Path:
    """Return the dist directory produced by the build.

    Most packages use 'dist'; lobster-monolithic renames it to 'meta_dist'.
    """
    for candidate in ("dist", "meta_dist"):
        path = package_dir / candidate
        if path.is_dir():
            return path
    raise RuntimeError(
        f"No dist or meta_dist directory found under {package_dir}"
    )


# Copy the whole repo into a temp workspace, then build the package using
# 'make package'. This simulates the Makefile-based packaging path.
def stage_via_makefile(root: Path, dest: Path, package_name: str) -> None:
    """Run the Makefile package target for the given package."""
    work_root = dest / "make_run"
    package_dir = work_root / "packages" / package_name

    shutil.copytree(root, work_root)

    for candidate in ("dist", "meta_dist"):
        shutil.rmtree(package_dir / candidate, ignore_errors=True)

    env = build_env()

    subprocess.run(
        ["make", "package", f"LOBSTER_ROOT={work_root}"],
        cwd=package_dir,
        env=env,
        check=True,
    )


# Copy the whole repo into a separate temp workspace, then build the package by
# running its package_*.py script. This simulates the Python-script packaging path.
def stage_via_package_script(
    root: Path, dest: Path, package_name: str, script_name: str
) -> None:
    """Run the package_*.py script for the given package."""
    work_root = dest / "py_run"
    package_dir = work_root / "packages" / package_name

    shutil.copytree(root, work_root)

    for candidate in ("dist", "meta_dist"):
        shutil.rmtree(package_dir / candidate, ignore_errors=True)

    env = build_env()
    env["BUILD_WORKSPACE_DIRECTORY"] = str(work_root)

    subprocess.run(
        [sys.executable, script_name],
        cwd=package_dir,
        env=env,
        check=True,
    )


# Walk two directory trees and collect all differences: files that exist in one
# but not the other, files whose content differs, and (optionally) files whose
# Unix permissions differ. Returns a list of human-readable problem strings.
def report_diff(
    dcmp: filecmp.dircmp,
    prefix: str = "",
    check_permissions: bool = True,
) -> list[str]:
    """Recursively compare directory trees with deep file-content checks."""
    issues = []

    for name in sorted(dcmp.left_only):
        issues.append(f"Only in Makefile staging: {prefix}{name}")

    for name in sorted(dcmp.right_only):
        issues.append(f"Only in package script staging: {prefix}{name}")

    # Use deep comparison to avoid shallow stat-based false negatives.
    for name in sorted(dcmp.common_files):
        left_file = Path(dcmp.left) / name
        right_file = Path(dcmp.right) / name
        if not filecmp.cmp(left_file, right_file, shallow=False):
            issues.append(f"Content differs: {prefix}{name}")
        if check_permissions:
            left_mode = left_file.stat().st_mode & 0o777
            right_mode = right_file.stat().st_mode & 0o777
            if left_mode != right_mode:
                issues.append(
                    "Permission differs: "
                    f"{prefix}{name} "
                    f"(Makefile={left_mode:03o}, script={right_mode:03o})"
                )

    for name in sorted(dcmp.funny_files):
        issues.append(f"Uncomparable path: {prefix}{name}")

    for sub_name in sorted(dcmp.subdirs):
        sub_dcmp = dcmp.subdirs[sub_name]
        issues.extend(
            report_diff(
                sub_dcmp,
                prefix=f"{prefix}{sub_name}/",
                check_permissions=check_permissions,
            )
        )

    return issues


# Open both wheel files (they are just ZIP archives) and compare every entry
# inside them. The .dist-info/RECORD file is intentionally skipped because it
# contains generated hashes that will always differ. Returns a list of problems.
def compare_wheels(
    make_wheel: Path,
    py_wheel: Path,
    check_permissions: bool = True,
) -> list[str]:
    """Compare contents of two wheel files, ignoring RECORD metadata."""
    issues = []
    ignore_suffixes = {".dist-info/RECORD"}

    with (
        zipfile.ZipFile(make_wheel) as mw,
        zipfile.ZipFile(py_wheel) as pw,
    ):
        make_files = {
            n
            for n in mw.namelist()
            if not any(n.endswith(s) for s in ignore_suffixes)
        }
        py_files = {
            n
            for n in pw.namelist()
            if not any(n.endswith(s) for s in ignore_suffixes)
        }

        for name in sorted(make_files - py_files):
            issues.append(f"Only in Makefile wheel: {name}")

        for name in sorted(py_files - make_files):
            issues.append(f"Only in package script wheel: {name}")

        for name in sorted(make_files & py_files):
            if mw.read(name) != pw.read(name):
                issues.append(f"Wheel content differs: {name}")
            if check_permissions:
                make_mode = (mw.getinfo(name).external_attr >> 16) & 0o777
                py_mode = (pw.getinfo(name).external_attr >> 16) & 0o777
                if make_mode != py_mode:
                    issues.append(
                        "Wheel permission differs: "
                        f"{name} "
                        f"(Makefile={make_mode:03o}, script={py_mode:03o})"
                    )

    return issues


# Look for exactly one .whl file in the given dist directory.
# Raises an error if zero or more than one wheel is found.
def find_single_wheel(dist_dir: Path) -> Path:
    wheels = sorted(dist_dir.glob("*.whl"))
    if not wheels:
        raise RuntimeError(f"No wheel found in {dist_dir}")
    if len(wheels) > 1:
        raise RuntimeError(
            f"Multiple wheels found in {dist_dir}: {wheels}"
        )
    return wheels[0]


# Run both build paths (Makefile and Python script) for a single package in
# isolated temp directories, then compare their staged source tree and wheel
# output. Returns a dict with the outcome ('ok', 'mismatch', or 'error') and
# any differences found.
def verify_package(
    root: Path,
    package_name: str,
    check_permissions: bool,
) -> dict[str, object]:
    """Verify one package and return a structured result."""
    package_dir = root / "packages" / package_name
    result: dict[str, object] = {
        "package": package_name,
        "status": "error",
        "script": None,
        "staging_issues": [],
        "wheel_issues": [],
        "error": None,
        "make_wheel": None,
        "script_wheel": None,
    }

    if not package_dir.is_dir():
        msg = f"Package directory not found: {package_dir}"
        print(f"ERROR: {msg}", file=sys.stderr)
        result["error"] = msg
        return result

    try:
        script_path = find_package_script(package_dir)
        script_name = script_path.name
        result["script"] = script_name

        print(f"\n{'=' * 60}")
        print(f"Package : {package_name}")
        print(f"Script  : {script_name}")
        print(f"{'=' * 60}")

        with (
            tempfile.TemporaryDirectory(prefix="lobster_make_") as make_tmp,
            tempfile.TemporaryDirectory(prefix="lobster_py_") as py_tmp,
        ):
            make_dir = Path(make_tmp)
            py_dir = Path(py_tmp)

            print("Running Makefile...")
            stage_via_makefile(root, make_dir, package_name)

            print(f"Running {script_name}...")
            stage_via_package_script(
                root,
                py_dir,
                package_name,
                script_name,
            )

            make_pkg = make_dir / "make_run" / "packages" / package_name
            py_pkg = py_dir / "py_run" / "packages" / package_name

            make_staged = make_pkg / "lobster"
            py_staged = py_pkg / "lobster"

            print("Comparing staged trees...")
            dcmp = filecmp.dircmp(make_staged, py_staged)
            staging_issues = report_diff(
                dcmp,
                check_permissions=check_permissions,
            )
            result["staging_issues"] = staging_issues

            make_wheel = find_single_wheel(find_dist_dir(make_pkg))
            py_wheel = find_single_wheel(find_dist_dir(py_pkg))
            result["make_wheel"] = make_wheel.name
            result["script_wheel"] = py_wheel.name

            if make_wheel.name != py_wheel.name:
                result["wheel_issues"].append(
                    "Wheel filename differs: "
                    f"Makefile={make_wheel.name}, script={py_wheel.name}"
                )

            print("Comparing wheel contents...")
            wheel_issues = compare_wheels(
                make_wheel,
                py_wheel,
                check_permissions=check_permissions,
            )
            if result["wheel_issues"]:
                wheel_issues = list(result["wheel_issues"]) + wheel_issues
            result["wheel_issues"] = wheel_issues

        if staging_issues:
            print("\nSTAGING DIFFERENCES FOUND:\n")
            for issue in staging_issues:
                print(issue)

        if wheel_issues:
            print("\nWHEEL DIFFERENCES FOUND:\n")
            for issue in wheel_issues:
                print(issue)

        if staging_issues or wheel_issues:
            result["status"] = "mismatch"
            return result

        print(
            f"\nOK: {package_name} - staging and wheel contents are identical."
        )
        result["status"] = "ok"
        return result
    except Exception as exc:  # pylint: disable=broad-exception-caught
        msg = f"{type(exc).__name__}: {exc}"
        print(f"ERROR while verifying {package_name}: {msg}", file=sys.stderr)
        result["error"] = msg
        return result


# Scan the packages/ directory and return the names of all subdirectories that
# contain a Makefile — these are the buildable packages.
def discover_packages(root: Path) -> list[str]:
    """Return all package names (subdirectory names) under packages/."""
    packages_dir = root / "packages"
    return sorted(
        d.name
        for d in packages_dir.iterdir()
        if d.is_dir() and (d / "Makefile").exists()
    )


# Set up and parse the command-line arguments for this script.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare Makefile packaging and package_*.py packaging outputs "
            "for one or more lobster packages."
        )
    )
    parser.add_argument(
        "packages",
        nargs="*",
        help="Package names under packages/ (default: all packages).",
    )
    parser.add_argument(
        "--summary-json",
        dest="summary_json",
        metavar="PATH",
        help=(
            "Write a machine-readable JSON summary to PATH. "
            "Use '-' to print JSON summary to stdout."
        ),
    )
    parser.add_argument(
        "--ignore-permissions",
        action="store_true",
        help=(
            "Ignore permission/mode comparisons for staged files and wheel "
            "entries (useful for cross-platform tolerance)."
        ),
    )
    return parser.parse_args()


# Serialize the results dict to JSON and either print it to stdout (when
# summary_json is '-') or write it to the specified file path.
def write_summary(summary: dict[str, object], summary_json: str) -> None:
    text = json.dumps(summary, indent=2, sort_keys=True)

    if summary_json == "-":
        print("\nJSON SUMMARY:\n")
        print(text)
        return

    summary_path = Path(summary_json)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(text + "\n", encoding="utf-8")
    print(f"JSON summary written to: {summary_path}")


# Entry point: parse arguments, figure out which packages to check, run the
# verification for each one, and exit with 0 if everything matched or 1 if
# any package failed.
def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]

    if not (root / "lobster").is_dir():
        print(f"ERROR: {root}/lobster not found", file=sys.stderr)
        return 1

    if args.packages:
        package_names = args.packages
    else:
        package_names = discover_packages(root)
        print(f"No package specified - running all: {package_names}")

    print(f"LOBSTER_ROOT: {root}")

    results = [
        verify_package(
            root,
            name,
            check_permissions=not args.ignore_permissions,
        )
        for name in package_names
    ]
    failed = [
        str(result["package"])
        for result in results
        if result["status"] != "ok"
    ]

    summary: dict[str, object] = {
        "root": str(root),
        "check_permissions": not args.ignore_permissions,
        "requested_packages": package_names,
        "results": results,
        "failed_packages": failed,
        "success": not failed,
    }

    if args.summary_json:
        write_summary(summary, args.summary_json)

    if failed:
        print(f"\nFAILED packages: {failed}", file=sys.stderr)
        return 1

    print(f"\nAll {len(package_names)} package(s) passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Multiple packages
#python3 packages/verify_equivalence.py lobster-core lobster-metapackage

# All packages at once (no args)
#python3 packages/verify_equivalence.py

#python3 packages/verify_equivalence.py     > verify_equivalence.log 2>&1