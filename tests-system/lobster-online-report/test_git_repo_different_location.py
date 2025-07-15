from pathlib import Path

from .lobster_online_report_system_test_case_base import (
    LobsterOnlineReportSystemTestCaseBase)
from ..asserter import Asserter
from ..tests_utils.update_online_json_with_hashes import update_json


class NonGitRepositoryTest(LobsterOnlineReportSystemTestCaseBase):
    OUT_FILE = "expected-output.lobster"

    def setUp(self):
        super().setUp()
        current_dir = Path.cwd()
        # Go one folder back from the current working directory. This would be a
        # non-git directory
        parent_dir = current_dir.parent

        self._test_runner = self.create_test_runner(working_dir=parent_dir)
        self._test_runner.declare_input_file(self._data_directory / "report.lobster")
        self._test_runner.declare_input_file(self._data_directory / "basic.py")
        self._test_runner.declare_output_file(self._data_directory / self.OUT_FILE)
        self._test_runner.cmd_args.out = self.OUT_FILE

    def test_non_git_repository_with_repo_root(self):
        self._test_runner.cmd_args.lobster_report = str(
            self._test_runner.working_dir / "report.lobster")
        self._test_runner.cmd_args.repo_root = Path.cwd()

        update_json(self._data_directory / self.OUT_FILE, str(
            f"../{Path(self._test_runner.working_dir).name}/basic.py"))
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"LOBSTER report {self.OUT_FILE} "
                                  "created, using online references.\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_non_git_repository_without_repo_root(self):
        self._test_runner.cmd_args.lobster_report = str(
            self._test_runner.working_dir / "report.lobster")
        self._test_runner.cmd_args.out = self.OUT_FILE
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("error: could not find .git directory\n")
        asserter.assertExitCode(1)
