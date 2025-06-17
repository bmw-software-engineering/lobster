import shutil

from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from .lobsterjsonasserter import LobsterJsonAsserter


class InputDirectoryJsonTest(LobsterJsonSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_missing_directory(self):
        dir_does_not_exist = "directory_does_not_exist"
        self._test_runner.config_file_data.inputs.append(dir_does_not_exist)
        self._test_runner.config_file_data.tag_attribute = "directory_test"

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"<config>: lobster error: {dir_does_not_exist} is not a file or "
            f"directory\n"
        )
        asserter.assertExitCode(1)

    def test_empty_directory(self):
        OUT_FILE = "empty_directory.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)

        empty_dir_name = "empty_directory"
        empty_dir_path = self._data_directory / empty_dir_name
        self._test_runner.config_file_data.inputs.append(str(empty_dir_path))
        self._test_runner.config_file_data.tag_attribute = "directory_test"

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(0, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_consumes_files_in_specified_directory(self):
        OUT_FILE = "valid_directory.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.config_file_data.tag_attribute = "tags"
        self._test_runner.config_file_data.name_attribute = "name"
        self._test_runner.config_file_data.inputs.append("valid_directory")

        source_dir = self._data_directory / "valid_directory"
        dest_dir = self._test_runner.working_dir / "valid_directory"
        shutil.copytree(source_dir, dest_dir)

        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(6, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
