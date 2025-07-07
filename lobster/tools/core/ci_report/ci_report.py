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

from argparse import Namespace
import os.path

from lobster.report import Report
from lobster.items import Tracing_Status
from lobster.meta_data_tool_base import MetaDataToolBase


class CiReportTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="lobster-ci-report",
            description="Command line tool to check a LOBSTER report",
            official=True,
        )

        self._argument_parser.add_argument(
            "lobster_report",
            nargs="?",
            default="report.lobster",
        )

    def _run_impl(self, options: Namespace) -> int:
        if not os.path.isfile(options.lobster_report):
            if options.lobster_report == "report.lobster":
                self._argument_parser.error("specify report file")
            else:
                self._argument_parser.error(f"{options.lobster_report} is not a file")

        report = Report()
        report.load_report(options.lobster_report)

        for uid in sorted(report.items):
            item = report.items[uid]
            if item.tracing_status not in (Tracing_Status.OK,
                                           Tracing_Status.JUSTIFIED):
                for message in item.messages:
                    report.mh.error(item.location,
                                    message,
                                    fatal = False)

        if report.mh.errors:
            return 1
        else:
            return 0


def main() -> int:
    return CiReportTool().run()
