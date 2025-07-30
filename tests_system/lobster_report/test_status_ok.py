from .lobster_report_system_test_case_base import LobsterReportSystemTestCaseBase
from ..asserter import Asserter


class ReportOkTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_status_ok(self):
        # lobster-trace: core_report_req.Status_Ok
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_ok.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_ok.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_ok.lobster")

        conf_file = "lobster_ok.conf"
        out_file = "report_ok.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
