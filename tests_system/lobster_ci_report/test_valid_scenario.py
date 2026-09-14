import os
import unittest
from unittest.mock import patch
from tests_system.asserter import Asserter
from tests_system.lobster_ci_report.lobster_ci_report_system_test_case_base import (
    LobsterCiReportSystemTestCaseBase)


class ValidCiReportTest(LobsterCiReportSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_all_items_fully_traced(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Exits_Zero_When_Fully_Traced
        self._test_runner.declare_input_file(
            self._data_directory / "report_all_ok.lobster")
        self._test_runner.cmd_args.lobster_report = "report_all_ok.lobster"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)

    def test_zero_items(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Exits_Zero_When_Fully_Traced
        self._test_runner.declare_input_file(
            self._data_directory / "report_zero_items.lobster")
        self._test_runner.cmd_args.lobster_report = "report_zero_items.lobster"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)

    def test_default_report_file(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Default_Report_File
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "report_all_ok.lobster")
        os.rename(
            self._test_runner.working_dir / "report_all_ok.lobster",
            self._test_runner.working_dir / "report.lobster",
        )

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)

    def test_show_coverage_flag(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Show_Coverage_Flag
        # lobster-trace: core_ci_report_req.Ci_Report_Prints_Compiler_Style_Errors
        self._test_runner.declare_input_file(
            self._data_directory / "report_with_issues.lobster")
        self._test_runner.cmd_args.lobster_report = "report_with_issues.lobster"
        self._test_runner.cmd_args.show_coverage = True

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "demo.trlc:8:5: lobster error: missing up reference\n"
            "coverage: Requirements: 50.0% (1 of 2 items)\n"
        )
        asserter.assertExitCode(1)

    def test_relative_path_resolved_against_build_working_directory(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Relative_Path_Resolution
        other_dir = self.create_temp_dir(prefix="test-ci_report-bwd-")
        (other_dir / "elsewhere.lobster").write_text(
            (self._data_directory / "report_all_ok.lobster").read_text(
                encoding="UTF-8"),
            encoding="UTF-8",
        )
        self._test_runner.cmd_args.lobster_report = "elsewhere.lobster"

        with patch.dict(os.environ, {"BUILD_WORKING_DIRECTORY": str(other_dir)}):
            result = self._test_runner.run_tool_test()

        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertNoStdErrText()
        asserter.assertExitCode(0)


if __name__ == "__main__":
    unittest.main()
