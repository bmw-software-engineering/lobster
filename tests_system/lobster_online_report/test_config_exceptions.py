import unittest
from lobster.tools.core.online_report.online_report import (
    REPO_ROOT, BASE_URL, COMMIT_ID)
from tests_system.lobster_online_report.lobster_online_report_system_test_case_base \
    import (LobsterOnlineReportSystemTestCaseBase)
from tests_system.asserter import Asserter


class ConfigParserExceptionsOnlineReport(LobsterOnlineReportSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_missing_config_file(self):
        # lobster-trace: UseCases.Online_Report_Config_File_Missing
        not_existing_file = str(
            self._data_directory / "non-existing.yaml")

        self._test_runner.cmd_args.config = not_existing_file

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertStdErrText(
            f'lobster-online-report: {not_existing_file} '
            f'is not an existing file!\n'
        )
        asserter.assertExitCode(1)

    def test_config_file_errors(self):
        # lobster-trace: UseCases.Online_Report_Config_File_Key_Error
        test_cases = [
            (
                "with_no_repo_root.yaml",
                f"Missing attribute {REPO_ROOT}",
                "repo_root_key_error"
            ),
            (
                "with_no_base_url.yaml",
                f"Missing attribute {BASE_URL}",
                "base_url_key_error"
            ),
            (
                "with_no_commit_id.yaml",
                f"Missing attribute {COMMIT_ID}",
                "commit_id_key_error"
            ),
        ]

        for config_file, expected_error, case in test_cases:
            with self.subTest(i=case):
                self._test_runner.cmd_args.config = str(
                    self._data_directory / config_file)
                completed_process = self._test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, self._test_runner)
                asserter.assertInStdErr(expected_error)
                asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
