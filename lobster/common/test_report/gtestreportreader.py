# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
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

import xml.etree.ElementTree as ET
from typing import Iterator

from lobster.common.test_report.testreportreader import TestReportReader


class GtestReportReader(TestReportReader):
    """Reads GoogleTest XML reports (``--gtest_output=xml``).

    The test cases of a GoogleTest report carry a ``status`` attribute, by which
    a GoogleTest report is told apart from other JUnit XML reports. The unique
    name of a test case is ``<suite>:<test>``.
    """

    namespace = "gtest"
    framework = "GoogleTest"

    @classmethod
    def accepts(cls, root: ET.Element) -> bool:
        return root.tag == "testsuites" and any(
            "status" in testcase.attrib for testcase in root.iter("testcase")
        )

    def suites(self, root: ET.Element) -> Iterator[ET.Element]:
        for suite in root:
            assert suite.tag == "testsuite"
            yield suite

    def uid(self, suite: ET.Element, testcase: ET.Element) -> str:
        return f"{suite.attrib['name']}:{testcase.attrib['name']}"

    def is_executed(self, testcase: ET.Element) -> bool:
        return testcase.attrib["status"] == "run"
