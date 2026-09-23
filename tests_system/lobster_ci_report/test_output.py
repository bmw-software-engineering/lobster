import os
import shutil
import unittest
from unittest.mock import patch
from tests_system.asserter import Asserter
from tests_system.lobster_ci_report.lobster_ci_report_system_test_case_base import (
    LobsterCiReportSystemTestCaseBase)


class ValidCiReportTest(LobsterCiReportSystemTestCaseBase):
    REPORT_ALL_OK_JUSTIFIED = "report_all_ok_justified.lobster"
    REPORT_ZERO_ITEMS = "report_zero_items.lobster"
    REPORT_WITH_ISSUES = "report_with_issues.lobster"
    DEFAULT_REPORT = "report.lobster"

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_all_items_fully_traced(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Exits_Zero_When_Fully_Traced

        # GIVEN a report file with one item with tracing status "OK"
        # and one with "JUSTIFIED"
        filename = self.REPORT_ALL_OK_JUSTIFIED
        self._test_runner.declare_input_file(
            self._data_directory / filename)
        self._test_runner.cmd_args.lobster_report = filename

        # WHEN the tool is run with the specified report file
        result = self._test_runner.run_tool_test()

        # THEN the tool shall exit with code 0 and produce no output
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)

    def test_zero_items(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Exits_Zero_When_Fully_Traced
        # GIVEN a report file with zero items
        filename = self.REPORT_ZERO_ITEMS
        self._test_runner.declare_input_file(
            self._data_directory / filename)
        self._test_runner.cmd_args.lobster_report = filename

        # WHEN the tool is run with the specified report file
        result = self._test_runner.run_tool_test()

        # THEN the tool shall exit with code 0 and produce no output
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)

    def test_default_report_file(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Default_Report_File
        # GIVEN a report file called "report.lobster" in the current working directory
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / self.REPORT_ALL_OK_JUSTIFIED)
        os.rename(
            self._test_runner.working_dir / self.REPORT_ALL_OK_JUSTIFIED,
            self._test_runner.working_dir / self.DEFAULT_REPORT,
        )

        # WHEN the tool is run without specifying a report file explicitly
        result = self._test_runner.run_tool_test()

        # THEN the tool shall use the existing report file "report.lobster"
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)

    def test_show_coverage_flag_not_fully_traced(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Show_Coverage_Flag
        # lobster-trace: core_ci_report_req.Ci_Report_Prints_Compiler_Style_Errors

        # GIVEN a report file where items have got "messages"
        self._test_runner.declare_input_file(
            self._data_directory / self.REPORT_WITH_ISSUES)
        self._test_runner.cmd_args.lobster_report = self.REPORT_WITH_ISSUES
        self._test_runner.cmd_args.show_coverage = True

        # WHEN the tool is run
        result = self._test_runner.run_tool_test()

        # THEN the tool shall print the messages and coverage information
        # AND exit with non-zero return code
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "hydrogen.element:8:5: lobster error: missing electron\n"
            "coverage: Atoms: 50.0% (1 of 2 items)\n"
        )
        asserter.assertExitCode(1)

    def test_relative_path_resolved_against_build_working_directory(self):
        # lobster-trace: core_ci_report_req.Relative_Bazel_Path_Resolution
        ELSEWHERE_REPORT = "elsewhere.lobster"
        other_dir = self.create_temp_dir(prefix="test-ci-report-bwd-")
        shutil.copy(
            self._data_directory / self.REPORT_ALL_OK_JUSTIFIED,
            other_dir / ELSEWHERE_REPORT,
        )

        # GIVEN a relative path to the report file
        # AND "BUILD_WORKING_DIRECTORY" environment variable set
        self._test_runner.cmd_args.lobster_report = ELSEWHERE_REPORT

        with patch.dict(os.environ, {"BUILD_WORKING_DIRECTORY": str(other_dir)}):
            # WHEN the tool is run
            result = self._test_runner.run_tool_test()

        # THEN the tool shall find the report file relative to the path in
        # "BUILD_WORKING_DIRECTORY"
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)


if __name__ == "__main__":
    unittest.main()
