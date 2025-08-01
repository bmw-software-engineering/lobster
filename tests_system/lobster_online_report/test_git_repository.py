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

    def test_invalid_git_repository(self):
        # lobster-trace: core_online_report_req.Invalid_Git_Repository
        self._test_runner.cmd_args.lobster_report = str(
            self._data_directory / "empty.lobster")
        invalid_git_dir = self._data_directory / "invalid_git_dir"
        self._test_runner.cmd_args.repo_root = str(invalid_git_dir)
        self._test_runner.cmd_args.out = "invalid_report.lobster"

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn("lobster-online-report: error: "
                      "cannot find .git directory in",
                      completed_process.stderr)
        asserter.assertExitCode(2)

    def test_valid_git_repository(self):
        # lobster-trace: core_online_report_req.Valid_Git_Repository
        self._test_runner.declare_input_file(self._data_directory / "basic.py")
        self._test_runner.declare_output_file(self._data_directory / self.OUT_FILE)
        self._test_runner.cmd_args.lobster_report = str(
            self._data_directory / "report.lobster")
        self._test_runner.cmd_args.out = self.OUT_FILE

        update_json(self._data_directory / self.OUT_FILE, str(
            f"{Path(self._test_runner.working_dir).name}/basic.py"))

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"LOBSTER report {self.OUT_FILE} "
                                  "created, using online references.\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
