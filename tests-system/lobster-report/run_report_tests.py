from .lobster_report_system_test_case_base import LobsterReportSystemTestCaseBase
from ..asserter import Asserter


class ReportTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def _run_test(self, config_file, trlc_file, python_file, out_file):
        self._test_runner.declare_input_file(self._data_directory / config_file)
        self._test_runner.declare_input_file(self._data_directory / trlc_file)
        self._test_runner.declare_input_file(self._data_directory / python_file)

        self._test_runner.cmd_args.out = out_file
        self._test_runner.cmd_args.lobster_config = config_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
