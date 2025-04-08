from pathlib import Path
from .lobster_online_report_system_test_case_base import (
    LobsterOnlineReportSystemTestCaseBase)
from ..asserter import Asserter


class ValidScenarioTest(LobsterOnlineReportSystemTestCaseBase):
    OUT_FILE = "expected-output.lobster"

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

        data_dir = self._data_directory
        self._test_runner.declare_input_file(data_dir / "basic.py")
        self._test_runner.cmd_args.lobster_report = str(data_dir / "report.lobster")
        self._test_runner.cmd_args.out = self.OUT_FILE

    def test_valid_flow(self):
        # lobster-trace: core_online_report_req.Valid_Git_Repository

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"LOBSTER report {self.OUT_FILE} "
                                  "changed to use online references\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
