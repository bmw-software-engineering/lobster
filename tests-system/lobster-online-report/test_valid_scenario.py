from pathlib import Path
from .lobster_online_report_system_test_case_base import (
    LobsterOnlineReportSystemTestCaseBase)
from ..asserter import Asserter
from ..tests_utils.update_online_json_with_hashes import update_json


class GitRepositoryTest(LobsterOnlineReportSystemTestCaseBase):
    OUT_FILE = "expected-output.lobster"

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

        self._test_runner.declare_input_file(self._data_directory / "basic.py")
        self._test_runner.cmd_args.lobster_report = str(
            self._data_directory / "report.lobster")
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / self.OUT_FILE)

    def test_valid_git_repository(self):
        # lobster-trace: core_online_report_req.Valid_Git_Repository

        update_json(self._data_directory / "expected-output.lobster", str(
            Path(self._test_runner.working_dir).name))

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"LOBSTER report {self.OUT_FILE} "
                                  "created, using online references.\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
