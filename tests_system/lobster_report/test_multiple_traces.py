from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportMultipleTracesTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_multiple_traces_justification(self):
        """
        This test checks that the lobster report tool can handle multiple lobster traces
         with justifications in code as well as tests
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_just.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_test.lobster")

        conf_file = "multiple_traces_just.conf"
        out_file = "report_multiple_traces_just.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
