from .lobster_online_report_system_test_case_base import (
    LobsterOnlineReportSystemTestCaseBase)
from ..asserter import Asserter


class GitRepositoryTest(LobsterOnlineReportSystemTestCaseBase):
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
