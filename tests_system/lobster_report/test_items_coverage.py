import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase)


class ReportItemsCoverageTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_zero_items_coverage(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Coverage_calculation_in_Output
        # lobster-trace: core_report_req.Zero_Items_Coverage
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_zero_items.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_zero_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_zero_items.lobster")

        conf_file = "lobster_zero_items.conf"
        out_file = "report_zero_items.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()

        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_items_message_trace_coverage(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Coverage_calculation_in_Output
        # lobster-trace: core_report_req.Message_Trace_Coverage
        self._test_runner.declare_input_file(self._data_directory /
                                             "message_trace_coverage.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_message_trace_coverage.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_message_trace_coverage.lobster")

        out_file = "report_message_trace_coverage.lobster"
        self._test_runner.cmd_args.lobster_config = "message_trace_coverage.conf"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()

        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
