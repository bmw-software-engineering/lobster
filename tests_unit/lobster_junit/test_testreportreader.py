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

import contextlib
import io
import unittest
import xml.etree.ElementTree as ET

from lobster.common.test_report.junitreportreader import JunitReportReader


class TestReportReaderTest(unittest.TestCase):
    def test_read_uses_all_references_and_last_other_properties(self):
        """Test how the properties of a test case are read."""
        # lobster-trace: junit_req.Read_Properties_Of_Test_Case
        # GIVEN a test case with two lobster-tracing properties, two location
        # properties of each kind and a repeated other property
        root = ET.fromstring(
            '<testsuite name="suite">'
            '<testcase classname="pkg" name="test" file="a.py" line="1">'
            "<properties>"
            '<property name="lobster-tracing" value="Pkg.First"/>'
            '<property name="lobster-tracing-file" value="b.py"/>'
            '<property name="lobster-tracing-line" value="2"/>'
            '<property name="owner" value="first owner"/>'
            '<property name="lobster-tracing" value="Pkg.Second"/>'
            '<property name="lobster-tracing-file" value="c.py"/>'
            '<property name="lobster-tracing-line" value="3"/>'
            '<property name="owner" value="second owner"/>'
            "</properties>"
            "</testcase>"
            "</testsuite>"
        )

        # WHEN the report is read
        [item] = JunitReportReader().read(root)

        # THEN the item refers to both requirements, is located by the last
        # location properties, and its text has the last value of the property
        self.assertEqual(
            [str(reference) for reference in item.unresolved_references],
            ["req Pkg.First", "req Pkg.Second"],
        )
        self.assertEqual((item.location.filename, item.location.line), ("c.py", 3))
        self.assertEqual(item.text, ":Owner: second owner")


    def test_read_keeps_properties_and_warns_if_name_conflicts(self):
        """Test that recorded Given/When/Then properties win over the test name."""
        # lobster-trace: junit_req.Read_Keeps_Properties_And_Warns_On_Conflict
        # GIVEN a test case named by the Given/When/Then convention which records
        # a Given property
        # AND a reader which derives Given, When and Then from test names
        root = ET.fromstring(
            '<testsuite name="suite">'
            '<testcase classname="pkg" name="GivenA_ExpectB" file="a.py" line="7">'
            '<properties><property name="given" value="recorded"/></properties>'
            "</testcase>"
            "</testsuite>"
        )
        stderr = io.StringIO()

        # WHEN the report is read
        with contextlib.redirect_stderr(stderr):
            [item] = JunitReportReader(derive_gwt_from_test_name=True).read(root)

        # THEN the text is the recorded property only
        # AND a warning names the location and the uid of the test case
        self.assertEqual(item.text, ":Given: recorded")
        self.assertEqual(
            stderr.getvalue(),
            "a.py:7: lobster warning: test pkg:GivenA_ExpectB records "
            "Given/When/Then properties, ignoring its name\n",
        )


if __name__ == "__main__":
    unittest.main()
