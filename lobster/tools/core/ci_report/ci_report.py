#!/usr/bin/env python3
#
# lobster_ci_report - Visualise LOBSTER issues for CI
# Copyright (C) 2023-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from argparse import ArgumentParser, Namespace
import os
from typing import List, Optional, Sequence

from lobster.common.report import Report
from lobster.common.items import Tracing_Status
from lobster.common.meta_data_tool_base import MetaDataToolBase


def resolve_report_path(lobster_report: str) -> str:
    # relative paths are given from where `bazel run` was invoked, not
    # from the runfiles directory the binary actually starts in
    if os.path.isabs(lobster_report):
        return lobster_report
    workdir = os.environ.get("BUILD_WORKING_DIRECTORY")
    return os.path.join(workdir, lobster_report) if workdir else lobster_report


def ensure_report_file_exists(
        argument_parser: ArgumentParser,
        lobster_report_arg: str,
        resolved_path: str,
) -> None:
    """Exits via argument_parser.error() (SystemExit) IF resolved_path does not
    name an existing file, distinguishing whether the user gave that path
    explicitly or whether it is the unmodified default value."""
    if not os.path.isfile(resolved_path):
        if lobster_report_arg == "report.lobster":
            argument_parser.error("specify report file")
        else:
            argument_parser.error(f"{lobster_report_arg} is not a file")


def report_errors_for_untraced_items(report: Report) -> None:
    """Emits an error (via report.mh) for each message of every item whose
    tracing status is neither OK nor JUSTIFIED."""
    for uid in sorted(report.items):
        item = report.items[uid]
        if item.tracing_status not in (Tracing_Status.OK,
                                       Tracing_Status.JUSTIFIED):
            for message in item.messages:
                report.mh.error(item.location,
                                message,
                                fatal = False)


def format_coverage_lines(report: Report) -> List[str]:
    """Returns one formatted coverage summary line per report level."""
    return [
        f"coverage: {level}: {coverage.coverage:.1f}% "
        f"({coverage.ok} of {coverage.items} items)"
        for level, coverage in report.coverage.items()
    ]


class CiReportTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="ci-report",
            description="Command line tool to check a LOBSTER report",
            official=True,
        )

        self._argument_parser.add_argument(
            "lobster_report",
            nargs="?",
            default="report.lobster",
        )
        self._argument_parser.add_argument(
            "--show-coverage",
            action="store_true",
            help="Print the per-level coverage summary of the report.",
        )

    def _run_impl(self, options: Namespace) -> int:
        lobster_report = resolve_report_path(options.lobster_report)
        ensure_report_file_exists(
            self._argument_parser, options.lobster_report, lobster_report,
        )

        report = Report()
        report.load_report(lobster_report)

        report_errors_for_untraced_items(report)

        if options.show_coverage:
            for line in format_coverage_lines(report):
                print(line)

        if report.mh.errors:
            return 1
        return 0


def main(args: Optional[Sequence[str]] = None) -> int:
    return CiReportTool().run(args)
