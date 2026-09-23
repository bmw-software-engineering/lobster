import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_ci_report.lobster_ci_report_system_test_case_base import (
    LobsterCiReportSystemTestCaseBase)


class InvalidCiReportTest(LobsterCiReportSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_missing_report_file_explicit(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Missing_Report_File
        missing_file_name = "non-existent-file"
        self._test_runner.cmd_args.lobster_report = missing_file_name

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertInStdErr(f"{missing_file_name} is not a file")
        asserter.assertExitCode(2)

    def test_missing_default_report_file(self):
        # lobster-trace: core_ci_report_req.Ci_Report_Missing_Report_File
        # lobster-trace: core_ci_report_req.Ci_Report_Default_Report_File
        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdOutText()
        asserter.assertInStdErr("specify report file")
        asserter.assertExitCode(2)


if __name__ == "__main__":
    unittest.main()
