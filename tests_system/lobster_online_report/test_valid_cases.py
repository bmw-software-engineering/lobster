from pathlib import Path
from unittest.mock import patch, Mock

from lobster.common.report import Report
from lobster.common.location import File_Reference
from tests_system.lobster_online_report.lobster_online_report_system_test_case_base \
    import (LobsterOnlineReportSystemTestCaseBase)
from tests_system.asserter import Asserter


class ConfigParserExceptionsOnlineReport(LobsterOnlineReportSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def _create_files_from_lobster_report(self, lobster_file_path):
        """
        Reads a .lobster report file, finds all "file" references,
        and creates those files.
        """
        report = Report()
        report.load_report(str(lobster_file_path))
        file_paths = set()

        for item in report.items.values():
            if isinstance(item.location, File_Reference):
                file_path = Path(item.location.filename)
                abs_path = self._test_runner.working_dir / file_path
                file_paths.add(abs_path)
        for file_path in file_paths:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

    @patch('lobster.tools.core.online_report.path_to_url_converter.Repo')
    def test_main_repo(self, mock_repo_class):
        OUT_FILE = "main_repo_online_report.lobster"

        mock_main_repo = Mock()
        mock_main_repo.working_tree_dir = str(self._test_runner.working_dir)
        mock_repo_class.return_value = mock_main_repo
        mock_main_repo.submodules = []

        input_file = self._data_directory / "main_repo_report.lobster"

        self._create_files_from_lobster_report(input_file)

        self._test_runner.declare_input_file(input_file)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_main_repo.yaml")
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    @patch('lobster.tools.core.online_report.path_to_url_converter.Repo')
    def test_submodules(self, mock_repo_class):
        OUT_FILE = "submodule_online_report.lobster"

        mock_repo = Mock()
        mock_repo.working_tree_dir = str(self._test_runner.working_dir)
        mock_repo.submodules = []
        submodule_detail = [
            {
                "name": "submodule2_folder",
                "path": "system-test-repo/submodule2/folder",
                "url": "../palm/beach",
                "hexsha": "abcdef333333333333"
            },
            {
                "name": "submodule2",
                "path": "system-test-repo/submodule2",
                "url": "../somewhere/else",
                "hexsha": "abcdef22222222222222"
            },
            {
                "name": "submodule1",
                "path": "system-test-repo/submodule1",
                "url": "../bali/trip",
                "hexsha": "abcdef1111111111111111"
            }
        ]

        for submodule_data in submodule_detail:
            mock_submodule = Mock()
            mock_submodule.name = submodule_data["name"]
            mock_submodule.path = submodule_data["path"]
            mock_submodule.url = submodule_data["url"]
            mock_submodule.hexsha = submodule_data["hexsha"]
            mock_repo.submodules.append(mock_submodule)
        mock_repo_class.return_value = mock_repo

        input_file = self._data_directory / "submodule_report.lobster"

        self._create_files_from_lobster_report(input_file)

        self._test_runner.declare_input_file(input_file)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_submodule.yaml")
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
