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

import json
import unittest
from pathlib import Path
from lobster.tools.gtest.gtest import main as lobster_gtest_main
from tests_system.lobster_junit.lobster_junit_system_test_case_base import (
    LobsterJunitSystemTestCaseBase,
)
from tests_system.lobster_junit.lobster_junit_asserter import (
    LobsterJunitAsserter as Asserter,
)
from tests_system.testrunner import TestRunner


class LobsterGtestRunner(TestRunner):
    """Runs lobster-gtest, to compare its output with the one of lobster-junit."""

    def __init__(self, working_dir: Path, args: list):
        super().__init__(lobster_gtest_main, working_dir)
        self._args = args

    def get_tool_args(self) -> list:
        return self._args


def items(path: Path) -> list:
    with open(path, encoding="UTF-8") as lobster_file:
        return json.load(lobster_file)["data"]


class GoogleTestReportsTest(LobsterJunitSystemTestCaseBase):
    def _compare_with_lobster_gtest_tool(self, report: str):
        # GIVEN a GoogleTest report
        # AND the option to derive the specification from the name
        test_runner = self.create_test_runner()
        test_runner.declare_input_file(self._data_directory / report)
        test_runner.cmd_args.files = [report]
        test_runner.cmd_args.out = "junit.lobster"
        test_runner.cmd_args.derive_gwt_from_test_name = True
        gtest_runner = LobsterGtestRunner(
            self.create_temp_dir(prefix="test-lobster_gtest-"),
            [report, "--out", "gtest.lobster", "--derive-gwt-from-test-name"],
        )
        gtest_runner.declare_input_file(self._data_directory / report)

        # WHEN lobster-junit and lobster-gtest are run
        completed_process = test_runner.run_tool_test()
        gtest_process = gtest_runner.run_tool_test()

        # THEN lobster-junit writes the same items and messages as lobster-gtest
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertExitCode(gtest_process.returncode)
        asserter.assertStdErrText(gtest_process.stderr)
        self.assertEqual(
            items(test_runner.working_dir / "junit.lobster"),
            items(gtest_runner.working_dir / "gtest.lobster"),
        )

    def test_googletest_report_items_equal_lobster_gtest(self):
        """Test that GoogleTest reports give the same items as lobster-gtest."""
        # lobster-trace: junit_req.GoogleTest_Report_Items
        self._compare_with_lobster_gtest_tool("conventional_names.xml")

    def test_googletest_report_warnings_equal_lobster_gtest(self):
        """Test that GoogleTest reports give the same warnings as lobster-gtest."""
        # lobster-trace: junit_req.GoogleTest_Report_Items
        self._compare_with_lobster_gtest_tool("record_properties.xml")


if __name__ == "__main__":
    unittest.main()
