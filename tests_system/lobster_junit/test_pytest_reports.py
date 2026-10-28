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


def warning(location: str, uid: str) -> str:
    return (
        f"{location}: lobster warning: test {uid} records "
        "Given/When/Then properties, ignoring its name\n"
    )


class PytestReportsTest(LobsterJunitSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def _run(self, report: str, out_file: str):
        self._test_runner.declare_input_file(self._data_directory / report)
        self._test_runner.cmd_args.files = [report]
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)
        completed_process = self._test_runner.run_tool_test()
        return Asserter(self, completed_process, self._test_runner)

    def test_pytest_report_items(self):
        """Test the items of a pytest report with derived Given/When/Then."""
        # lobster-trace: junit_req.One_Item_Per_Test_Case
        # lobster-trace: junit_req.Item_Tag
        # lobster-trace: junit_req.Item_Framework
        # lobster-trace: junit_req.Item_Status
        # lobster-trace: junit_req.Item_References
        # lobster-trace: junit_req.Item_Location
        # lobster-trace: junit_req.Spec_Derived_From_Test_Name
        # lobster-trace: junit_req.Warning_If_Properties_And_Test_Name_Given
        # GIVEN a pytest report (junit_family=xunit1) with passed, failed,
        # errored, skipped and parametrized tests, tests in a class, tests
        # following the Given/When/Then naming convention, and one test which
        # records a Given property
        # AND the option to derive the specification from the name
        self._test_runner.cmd_args.derive_gwt_from_test_name = True

        # WHEN the tool is run
        asserter = self._run("pytest_report.xml", "pytest_report.lobster")

        # THEN there is one item per test case with the expected tag, framework,
        # status, references, 1-based location and text
        # AND a warning for the test which records a Given property
        asserter.assertStdErrText(
            warning("test_stack.py:28", "test_stack:test_GivenRecorded_ExpectWarning")
        )
        asserter.assertStdOutNumAndFile(8, "pytest_report.lobster")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_pytest_report_items_without_option(self):
        """Test that without the option only recorded properties form the text."""
        # lobster-trace: junit_req.Item_Text_From_Properties
        # GIVEN the same pytest report
        # AND no option to derive the specification from the name

        # WHEN the tool is run
        asserter = self._run(
            "pytest_report.xml", "pytest_report_without_option.lobster"
        )

        # THEN the item texts contain only the recorded properties
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(8, "pytest_report_without_option.lobster")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_pytest_report_without_file_and_line(self):
        """Test items of a pytest report which has no file and line attributes."""
        # lobster-trace: junit_req.Item_Location
        # lobster-trace: junit_req.Warning_If_Properties_And_Test_Name_Given
        # GIVEN a pytest report written with pytest's default junit_family
        # (xunit2), which has no file and line attributes
        # AND the option to derive the specification from the name
        self._test_runner.cmd_args.derive_gwt_from_test_name = True

        # WHEN the tool is run
        asserter = self._run(
            "pytest_report_without_location.xml",
            "pytest_report_without_location.lobster",
        )

        # THEN the items have an unknown location
        # AND the warning names the unknown location
        asserter.assertStdErrText(
            warning(
                "<unknown location>", "test_stack:test_GivenRecorded_ExpectWarning"
            )
        )
        asserter.assertStdOutNumAndFile(8, "pytest_report_without_location.lobster")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
