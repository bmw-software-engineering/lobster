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
from tests_system.lobster_junit.lobster_junit_system_test_case_base import (
    LobsterJunitSystemTestCaseBase,
)
from tests_system.lobster_junit.lobster_junit_asserter import (
    LobsterJunitAsserter as Asserter,
)


class JunitReportsTest(LobsterJunitSystemTestCaseBase):
    def test_junit_report_items(self):
        """Test the items of a JUnit report of a framework without own reader."""
        # lobster-trace: junit_req.One_Item_Per_Test_Case
        # lobster-trace: junit_req.Item_Tag
        # lobster-trace: junit_req.Item_Framework
        # lobster-trace: junit_req.Item_Status
        # lobster-trace: junit_req.Item_Location
        # lobster-trace: junit_req.Spec_Derived_From_Test_Name
        # GIVEN a JUnit report with nested test suites, a test case with an empty
        # classname, an errored and a skipped test case, and a test case whose
        # location is overridden by properties
        test_runner = self.create_test_runner()
        test_runner.declare_input_file(self._data_directory / "junit_report.xml")
        test_runner.cmd_args.files = ["junit_report.xml"]
        test_runner.cmd_args.out = "junit_report.lobster"
        test_runner.cmd_args.derive_gwt_from_test_name = True
        test_runner.declare_output_file(self._data_directory / "junit_report.lobster")

        # WHEN the tool is run
        completed_process = test_runner.run_tool_test()

        # THEN the test cases of the outer suite come before those of the nested
        # suite, the empty classname is replaced by the suite name, the framework
        # is JUnit, the line is not shifted, and the properties override the
        # location
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(4, "junit_report.lobster")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
