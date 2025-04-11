from pathlib import Path
from .lobster_online_report_system_test_case_base import (
    LobsterOnlineReportSystemTestCaseBase)
from ..asserter import Asserter
import shutil


class ValidScenarioTest(LobsterOnlineReportSystemTestCaseBase):
    OUT_FILE = "expected-output.lobster"

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

        working_dir = Path(__file__).parents[2]
        basic_file = self._data_directory / "basic.py"

        shutil.copy2(basic_file, working_dir)
        self._test_runner.cmd_args.lobster_report = str(
            self._data_directory / "report.lobster")
        self._test_runner.cmd_args.out = self.OUT_FILE

    def test_valid_flow(self):
        self._test_runner._working_dir = Path(__file__).parents[2]

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        (Path(__file__).parents[2] / "basic.py").unlink(missing_ok=True)

        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"LOBSTER report {self.OUT_FILE} "
                                  "changed to use online references\n")
        asserter.assertExitCode(0)
