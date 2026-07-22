"""Entrypoint to run pip-installed TRLC as a Bazel py_test."""

import runpy


def main() -> None:
    # Prefer package-as-script, then fall back to the historical module path.
    try:
        runpy.run_module("trlc", run_name="__main__")
    except ImportError:
        runpy.run_module("trlc.trlc", run_name="__main__")


if __name__ == "__main__":
    main()
