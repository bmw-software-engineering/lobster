import shutil
from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from .lobsterjsonasserter import LobsterJsonAsserter


class JsonMultipleFilesTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_multiple_files(self):
        """
        Tests the processing of multiple input files by the tool,
        including handling of non-JSON files.
        """
        self._test_runner.config_file_data.name_attribute = "name"
        self._test_runner.config_file_data.tag_attribute = "tags"
        out_file = "multiple_files.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_input_file(self._data_directory / "basic.json")
        self._test_runner.declare_input_file(self._data_directory / "multi1.json")
        self._test_runner.declare_input_file(
            self._data_directory / "multi2_invalid.txt"
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"<config>: lobster warning: not a .json file\n"
            f"lobster-json: wrote 9 items to {out_file}\n"
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_multiple_files_specified_in_config(self):
        """
        Tests the processing of multiple input files specified in a configuration file
        """
        self._test_runner.config_file_data.name_attribute = "name"
        self._test_runner.config_file_data.tag_attribute = "tags"
        self._test_runner.config_file_data.inputs = [
            "basic.json",
            "multi1.json",
        ]
        out_file = "multi_config.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "basic.json"
        )
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "multi1.json"
        )
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "single2.json"
        )
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "input_with_attributes.json"
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(8, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_empty_dir_file(self):
        """ Tests the handling of an empty directory file."""
        self._test_runner.config_file_data.name_attribute = "name"
        self._test_runner.config_file_data.tag_attribute = "tags"

        self._test_runner.config_file_data.inputs.append("empty_file_dir")

        source_dir = self._data_directory / "empty_file_dir"
        dest_dir = self._test_runner.working_dir / "empty_file_dir"
        shutil.copytree(source_dir, dest_dir)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        self.assertIn("json.decoder.JSONDecodeError:", completed_process.stderr)
        asserter.assertExitCode(1)

    def test_valid_dir_file(self):
        """
        Tests the processing of a valid directory file with multiple input files.
        """
        self._test_runner.config_file_data.name_attribute = "name"
        self._test_runner.config_file_data.tag_attribute = "tags"
        out_file = "valid_dir.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_inputs_from_file(
            self._data_directory / "input_files.txt", self._data_directory)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(5, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_inputs_and_inputs_from_file(self):
        """
        Tests the combination of inputs declared directly and those from a file.
        """
        self._test_runner.config_file_data.name_attribute = "name"
        self._test_runner.config_file_data.tag_attribute = "tags"
        out_file = "inputs_and_inputs_from_file.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_input_file(self._data_directory / "basic.json")
        self._test_runner.declare_input_file(self._data_directory / "multi1.json")
        self._test_runner.declare_inputs_from_file(
            self._data_directory / "input_files.txt", self._data_directory)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(13, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
