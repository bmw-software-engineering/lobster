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

import re
import xml.etree.ElementTree as ET
from typing import List

from lobster.common.items import Tracing_Tag
from lobster.common.test_report.testreportreader import TestReportReader

_REFERENCE_SEPARATOR = re.compile(r"[,\s]+")


class JunitReportReader(TestReportReader):
    """Reads JUnit XML reports of test frameworks without a dedicated reader.

    The root is either ``<testsuites>`` or a single ``<testsuite>``, and test
    suites may be nested. A skipped test case has a ``<skipped>`` element, and an
    errored one an ``<error>`` element. The unique name of a test case is
    ``<classname>:<name>``, so that equally named tests of different classes or
    modules stay apart.
    """

    namespace = "junit"
    framework = "JUnit"

    @classmethod
    def accepts(cls, root: ET.Element) -> bool:
        return root.tag in ("testsuites", "testsuite")

    def suites(self, root: ET.Element) -> List[ET.Element]:
        return [
            suite
            for suite in root.iter("testsuite")
            if any(child.tag == "testcase" for child in suite)
        ]

    def uid(self, suite: ET.Element, testcase: ET.Element) -> str:
        scope = testcase.attrib.get("classname") or suite.attrib.get("name", "")
        return f"{scope}:{testcase.attrib['name']}"

    def is_executed(self, testcase: ET.Element) -> bool:
        return all(child.tag != "skipped" for child in testcase)

    def has_failed(self, testcase: ET.Element) -> bool:
        return any(child.tag in ("failure", "error") for child in testcase)

    def references(self, value: str) -> List[Tracing_Tag]:
        return [
            Tracing_Tag.from_text("req", reference)
            for reference in _REFERENCE_SEPARATOR.split(value)
            if reference
        ]
