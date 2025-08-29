from pathlib import Path
from unittest.mock import patch, MagicMock
import shutil

from tests_system.lobster_online_report.lobster_online_report_system_test_case_base \
    import (LobsterOnlineReportSystemTestCaseBase)
from tests_system.asserter import Asserter


class ConfigParserExceptionsOnlineReport(LobsterOnlineReportSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        src = self._data_directory / "system-test-repo"
        dst = Path(self._test_runner.working_dir) / "system-test-repo"
        shutil.copytree(src, dst, dirs_exist_ok=True)

    @patch('lobster.tools.core.online_report.path_to_url_converter.Repo')
    def test_main_repo(self, mock_repo_class):
        OUT_FILE = "main_repo_online_report.lobster"

        mock_repo = MagicMock()
        mock_repo.working_tree_dir = str(self._test_runner.working_dir)
        mock_repo_class.return_value = mock_repo

        input_file = self._data_directory / "main_repo_report.lobster"
        config_file = str(
            self._data_directory / "valid_main_repo.yaml")
        output_file = self._data_directory / OUT_FILE

        self._test_runner.declare_input_file(input_file)
        self._test_runner.cmd_args.config = config_file
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(output_file)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    @patch('lobster.tools.core.online_report.path_to_url_converter.Repo')
    def test_submodules(self, mock_repo_class):
        OUT_FILE = "submodule_online_report.lobster"

        mock_repo = MagicMock()
        mock_repo.working_tree_dir = str(self._test_runner.working_dir)
        mock_repo.submodules = []
        submodule_detail = [
            {
                "name": "submodule2_folder",
                "path": "system-test-repo/submodule2/folder",
                "url": "https://somewhere/submodule2_folder.git",
                "hexsha": "abcdef333333333333"
            },
            {
                "name": "submodule2",
                "path": "system-test-repo/submodule2",
                "url": "https://somewhere/submodule2.git",
                "hexsha": "abcdef22222222222222"
            },
            {
                "name": "submodule1",
                "path": "system-test-repo/submodule1",
                "url": "https://somewhere/submodule1.git",
                "hexsha": "abcdef1111111111111111"
            }
        ]

        for submodule_data in submodule_detail:
            mock_submodule = MagicMock()
            mock_submodule.name = submodule_data["name"]
            mock_submodule.path = submodule_data["path"]
            mock_submodule.url = submodule_data["url"]
            mock_submodule.hexsha = submodule_data["hexsha"]
            mock_repo.submodules.append(mock_submodule)
        mock_repo_class.return_value = mock_repo

        input_file = self._data_directory / "submodule_report.lobster"
        config_file = str(
            self._data_directory / "valid_submodule.yaml")
        output_file = self._data_directory / OUT_FILE

        self._test_runner.declare_input_file(input_file)
        self._test_runner.cmd_args.config = config_file
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(output_file)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
