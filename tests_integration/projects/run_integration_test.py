"""Runs lobster-trlc and lobster-report on a project and diffs against a reference."""

import argparse
import difflib
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List

from python.runfiles import runfiles  # pylint: disable=import-error

from lobster.tools.core.report.report import main as report_main
from lobster.tools.trlc.trlc_tool import main as trlc_main


def _resolve(rlocation_path: str) -> Path:
    resolved = runfiles.Create().Rlocation(rlocation_path)
    if resolved is None or not Path(resolved).is_file():
        raise FileNotFoundError(f"runfile not found: {rlocation_path}")
    return Path(resolved)


def _read_lines(path: Path) -> List[str]:
    # Text mode normalizes CRLF to LF.
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def _stage(files: List[Path], destination: Path) -> None:
    # Files are staged flat, as in the Makefile flow.
    seen = set()
    for file in files:
        if file.name in seen:
            raise ValueError(f"duplicate staged file name {file.name}")
        seen.add(file.name)
        shutil.copy(file, destination / file.name)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", action="append", default=[])
    parser.add_argument("--trlc", action="append", default=[],
                        help="<trlc config>=<lobster file to produce>")
    parser.add_argument("--config", required=True)
    parser.add_argument("--reference", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    sources = [_resolve(path) for path in args.src]
    trlc_jobs = []
    for job in args.trlc:
        config, output = job.rsplit("=", 1)
        trlc_jobs.append((_resolve(config), output))
    config = _resolve(args.config)
    reference = _read_lines(_resolve(args.reference))

    original_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp)
        _stage(sources + [cfg for cfg, _ in trlc_jobs], stage)
        shutil.copy(config, stage / "lobster.conf")
        # Windows cannot delete the current directory.
        os.chdir(stage)
        try:
            for trlc_config, output in trlc_jobs:
                status = trlc_main(["--config", trlc_config.name, "--out", output])
                if status != 0:
                    print(f"lobster-trlc failed with status {status}")
                    return 1
            status = report_main(["--lobster-config", "lobster.conf",
                                  "--out", "report.lobster"])
            if status != 0:
                print(f"lobster-report failed with status {status}")
                return 1
            report = _read_lines(stage / "report.lobster")
        finally:
            os.chdir(original_cwd)

    if report == reference:
        return 0
    sys.stdout.writelines(
        difflib.unified_diff(report, reference,
                             fromfile="report", tofile="reference")
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
