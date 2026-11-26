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
from tests_system.lobster_gtest.lobster_gtest_system_test_case_base import (
    LobsterGtestSystemTestCaseBase,
)
from tests_system.lobster_gtest.lobster_gtest_asserter import (
    LobsterGtestAsserter as Asserter,
)


class ReportsWithoutTestCaseStatusTest(LobsterGtestSystemTestCaseBase):
    def test_reports_of_other_frameworks_are_ignored(self):
        """Test that JUnit XML reports of other test frameworks are ignored."""
        # lobster-trace: gtest_req.Reports_Without_Test_Case_Status_Ignored
        # GIVEN a pytest report and a JUnit report, in which no test case has a
        # status attribute
        test_runner = self.create_test_runner()
        for report in ("pytest_report.xml", "junit_report.xml"):
            test_runner.declare_input_file(self._data_directory / report)
        test_runner.cmd_args.files = ["pytest_report.xml", "junit_report.xml"]
        out_file = "reports_without_test_case_status.lobster"
        test_runner.cmd_args.out = out_file
        test_runner.declare_output_file(self._data_directory / out_file)

        # WHEN the tool is run
        completed_process = test_runner.run_tool_test()

        # THEN no item is written, nothing is printed to stderr, and the tool
        # succeeds
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(0, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
