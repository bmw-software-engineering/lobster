#!/usr/bin/env python3
#
# lobster_junit - Extract tracing tags from JUnit XML test reports for LOBSTER
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from typing import Optional, Sequence

from lobster.common.test_report.gtestreportreader import GtestReportReader
from lobster.common.test_report.junitreportreader import JunitReportReader
from lobster.common.test_report.pytestreportreader import PytestReportReader
from lobster.common.test_report.testreporttool import TestReportTool


class JunitTool(TestReportTool):
    def __init__(self):
        super().__init__(
            name="junit",
            description="Extract tracing tags from JUnit XML test reports, e.g. of "
            "GoogleTest or pytest",
            readers=[GtestReportReader, PytestReportReader, JunitReportReader],
            generator="lobster_junit",
        )


def main(args: Optional[Sequence[str]] = None) -> int:
    return JunitTool().run(args)
