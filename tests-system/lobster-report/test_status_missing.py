from .lobster_report_system_test_case_base import LobsterReportSystemTestCaseBase
from ..asserter import Asserter


class ReportJustifiedTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_status_missing(self):
        # lobster-trace: core_report_req.Status_Missing
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_missing.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_missing.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_missing.lobster")

        conf_file = "lobster_missing.conf"
        out_file = "report_missing.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_status_missing_mixed(self):
        # lobster-trace: core_report_req.Status_Missing
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_mixed.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_mixed.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_mixed.lobster")

        conf_file = "lobster_mixed.conf"
        out_file = "report_mixed.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
