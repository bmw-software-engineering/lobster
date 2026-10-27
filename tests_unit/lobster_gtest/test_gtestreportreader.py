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


class GtestReportReaderTest(unittest.TestCase):
    def test_accepts_reports_with_test_case_status(self):
        """Test that only reports with a test case status are accepted."""
        # lobster-trace: gtest_req.Gtest_Accepts_Reports_With_Test_Case_Status
        # GIVEN a GoogleTest report, JUnit reports without status, and other XML
        # WHEN accepts is called
        # THEN only the testsuites root with a test case status is accepted
        for xml, expected in (
            (
                '<testsuites><testsuite name="s"><testcase name="t" status="run"/>'
                "</testsuite></testsuites>",
                True,
            ),
            (
                '<testsuites><testsuite name="s"><testcase name="t"/></testsuite>'
                "</testsuites>",
                False,
            ),
            ('<testsuite name="s"><testcase name="t" status="run"/></testsuite>', False),
            ("<testsuites/>", False),
            ("<project/>", False),
        ):
            with self.subTest(xml):
                self.assertEqual(GtestReportReader.accepts(ET.fromstring(xml)), expected)


if __name__ == "__main__":
    unittest.main()
