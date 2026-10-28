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

from lobster.common.test_report.pytestreportreader import PytestReportReader


class PytestReportReaderTest(unittest.TestCase):
    def test_accepts_roots_named_pytest(self):
        """Test that only JUnit roots whose name starts with pytest are accepted."""
        # lobster-trace: junit_req.Pytest_Accepts_Pytest_Root
        # GIVEN roots of pytest reports, of other JUnit reports and of other XML
        # WHEN accepts is called
        # THEN only JUnit roots named pytest... are accepted
        for xml, expected in (
            ('<testsuites name="pytest tests"/>', True),
            ('<testsuite name="pytest"/>', True),
            ('<testsuites name="All tests"/>', False),
            ("<testsuites/>", False),
            ('<project name="pytest"/>', False),
        ):
            with self.subTest(xml):
                self.assertEqual(
                    PytestReportReader.accepts(ET.fromstring(xml)), expected
                )

    def test_source_line_is_one_based(self):
        """Test that the 0-based line of pytest is converted to a 1-based line."""
        # lobster-trace: junit_req.Pytest_Source_Line_Is_One_Based
        # GIVEN test cases with and without a line attribute
        reader = PytestReportReader()

        # WHEN the source line is requested
        # THEN it is one more than the attribute, or None without the attribute
        self.assertEqual(reader.source_line(ET.fromstring('<testcase line="41"/>')), 42)
        self.assertIsNone(reader.source_line(ET.fromstring("<testcase/>")))

    def test_spec_name_without_parameters(self):
        """Test that parameters of parametrized tests are removed from the name."""
        # lobster-trace: junit_req.Pytest_Spec_Name_Without_Parameters
        # GIVEN test cases with and without parameters in their name
        reader = PytestReportReader()

        # WHEN the name for the Given/When/Then derivation is requested
        # THEN the parameters are removed
        for name, expected in (
            ("test_GivenA_ExpectB[1-arbitrary_value]", "test_GivenA_ExpectB"),
            ("test_GivenA_ExpectB", "test_GivenA_ExpectB"),
        ):
            with self.subTest(name):
                testcase = ET.fromstring(f'<testcase name="{name}"/>')
                self.assertEqual(reader.test_name_for_spec(testcase), expected)


if __name__ == "__main__":
    unittest.main()
