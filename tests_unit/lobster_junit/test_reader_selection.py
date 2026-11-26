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

import unittest
import xml.etree.ElementTree as ET

from lobster.common.test_report.gtestreportreader import GtestReportReader
from lobster.common.test_report.junitreportreader import JunitReportReader
from lobster.common.test_report.pytestreportreader import PytestReportReader
from lobster.tools.junit.junit import JunitTool


class ReaderSelectionTest(unittest.TestCase):
    def test_lobster_junit_selects_first_accepting_reader(self):
        """Test which reader lobster-junit selects for which report."""
        # lobster-trace: junit_req.Reader_Selected_Per_Report
        # GIVEN lobster-junit
        tool = JunitTool()

        # WHEN a reader is selected for a GoogleTest, pytest, JUnit and other report
        # THEN the first reader in the order GoogleTest, pytest, JUnit which
        # accepts the report is selected, and none for the other report
        for xml, expected in (
            (
                '<testsuites name="pytest tests"><testsuite name="s">'
                '<testcase name="t" status="run"/></testsuite></testsuites>',
                GtestReportReader,
            ),
            ('<testsuites name="pytest tests"/>', PytestReportReader),
            ('<testsuites name="All tests"/>', JunitReportReader),
            ("<project/>", None),
        ):
            with self.subTest(xml):
                self.assertIs(tool._select_reader(ET.fromstring(xml)), expected)


if __name__ == "__main__":
    unittest.main()
