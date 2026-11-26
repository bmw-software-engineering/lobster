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

from lobster.common.test_report.junitreportreader import JunitReportReader


class JunitReportReaderTest(unittest.TestCase):
    def test_accepts_testsuites_and_testsuite_roots(self):
        """Test which root elements are accepted."""
        # lobster-trace: junit_req.Junit_Accepts_Testsuites_And_Testsuite
        # GIVEN root elements of JUnit reports and of other XML files
        # WHEN accepts is called
        # THEN only testsuites and testsuite roots are accepted
        for xml, expected in (
            ("<testsuites/>", True),
            ("<testsuite/>", True),
            ("<project/>", False),
        ):
            with self.subTest(xml):
                self.assertEqual(
                    JunitReportReader.accepts(ET.fromstring(xml)), expected
                )

    def test_suites_are_all_testsuites_with_test_cases_in_document_order(self):
        """Test that nested test suites are found in document order."""
        # lobster-trace: junit_req.Junit_Suites_With_Test_Cases
        # GIVEN a report whose outer suite contains a nested suite before its own
        # test case, and a suite without test cases
        root = ET.fromstring(
            "<testsuites>"
            '<testsuite name="outer">'
            '<testsuite name="inner"><testcase name="a"/></testsuite>'
            '<testcase name="b"/>'
            "</testsuite>"
            '<testsuite name="empty"/>'
            "</testsuites>"
        )

        # WHEN the suites are requested
        suites = JunitReportReader().suites(root)

        # THEN all suites with test cases are returned in document order
        self.assertEqual([suite.attrib["name"] for suite in suites], ["outer", "inner"])

    def test_suites_include_a_testsuite_root(self):
        """Test that a testsuite root element is a suite itself."""
        # lobster-trace: junit_req.Junit_Suites_With_Test_Cases
        # GIVEN a report whose root element is a testsuite with a test case
        root = ET.fromstring('<testsuite name="root"><testcase name="a"/></testsuite>')

        # WHEN the suites are requested
        # THEN the root element is returned
        self.assertEqual(JunitReportReader().suites(root), [root])

    def test_uid_from_classname_or_suite_name(self):
        """Test that the uid uses the classname, or else the suite name."""
        # lobster-trace: junit_req.Junit_Uid_From_Classname_Or_Suite
        # GIVEN test cases with a classname, an empty classname and no classname
        suite = ET.fromstring('<testsuite name="suite"/>')
        reader = JunitReportReader()

        # WHEN the uid is requested
        # THEN it is scoped by the classname, or by the suite name
        for xml, expected in (
            ('<testcase classname="pkg.Class" name="test"/>', "pkg.Class:test"),
            ('<testcase classname="" name="test"/>', "suite:test"),
            ('<testcase name="test"/>', "suite:test"),
        ):
            with self.subTest(xml):
                self.assertEqual(reader.uid(suite, ET.fromstring(xml)), expected)

    def test_status_from_child_elements(self):
        """Test that skipped, failure and error elements determine the status."""
        # lobster-trace: junit_req.Junit_Status_From_Child_Elements
        # GIVEN test cases with no, a skipped, a failure and an error element
        reader = JunitReportReader()

        # WHEN is_executed and has_failed are called
        # THEN skipped test cases are not executed, and failures and errors fail
        for xml, executed, failed in (
            ('<testcase name="t"/>', True, False),
            ('<testcase name="t"><skipped/></testcase>', False, False),
            ('<testcase name="t"><failure/></testcase>', True, True),
            ('<testcase name="t"><error/></testcase>', True, True),
        ):
            with self.subTest(xml):
                testcase = ET.fromstring(xml)
                self.assertEqual(reader.is_executed(testcase), executed)
                self.assertEqual(reader.has_failed(testcase), failed)

    def test_references_split_at_commas_and_whitespace(self):
        """Test that references are split at commas and whitespace."""
        # lobster-trace: junit_req.Junit_References_Split_At_Commas_And_Whitespace
        # GIVEN a lobster-tracing value with commas, whitespace and a version
        value = " Pkg.First,Pkg.Second  Pkg.Third@2,, "

        # WHEN the references are requested
        references = JunitReportReader().references(value)

        # THEN there is one versioned tag per non-empty part
        self.assertEqual(
            [str(reference) for reference in references],
            ["req Pkg.First", "req Pkg.Second", "req Pkg.Third@2"],
        )


if __name__ == "__main__":
    unittest.main()
