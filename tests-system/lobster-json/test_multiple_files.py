import shutil
from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from .lobsterjsonasserter import LobsterJsonAsserter


class JsonMultipleFilesTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.tag_attribute = "tags"
        self._test_runner.config_file_data.name_attribute = "name"

    def test_multiple_input_files_specified_in_config(self):
        """
        Tests the processing of input files specified in a configuration file
        using the 'inputs' parameter.
        """
        self._test_runner.config_file_data.inputs = [
            "basic.json",
            "multi1.json",
        ]
        out_file = "multi_config.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.declare_output_file(self._data_directory / out_file)
        for filename in [
            "basic.json",
            "multi1.json",
            "single2.json",
            "input_with_attributes.json",
        ]:
            self._test_runner.copy_file_to_working_directory(
                self._data_directory / filename
            )

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(8, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_directory_with_empty_invalid_file(self):
        """
        Tests the processing of a directory containing an empty invalid file.
        """
        out_file = "empty.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.config_file_data.inputs.append("one")

        source_dir = self._data_directory / "one"
        dest_dir = self._test_runner.working_dir / "one"
        shutil.copytree(source_dir, dest_dir)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(0, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_inputs_from_file_specified_in_config(self):
        """
        Tests the processing of input files specified in a configuration file
        using the 'inputs_from_file' parameter.
        """
        out_file = "valid_dir.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_inputs_from_file(
            self._data_directory / "input_files.txt", self._data_directory)
        for filename in [
            "basic.json",
            "multi1.json",
            "single2.json",
            "input_with_attributes.json",
        ]:
            self._test_runner.copy_file_to_working_directory(
                self._data_directory / filename
            )

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(5, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_inputs_and_inputs_from_file_With_extra_valid_files(self):
        """
        Tests the processing of both 'inputs' and 'inputs_from_file' parameters
        in the configuration file, including additional valid files.
        """
        out_file = "both_inputs_with_extra_files.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_input_file(self._data_directory / "basic.json")
        self._test_runner.declare_input_file(self._data_directory / "multi1.json")
        self._test_runner.declare_inputs_from_file(
            self._data_directory / "input_files.txt", self._data_directory)
        for filename in [
            "basic.json",
            "multi1.json",
            "single2.json",
            "input_with_attributes.json",
        ]:
            self._test_runner.copy_file_to_working_directory(
                self._data_directory / filename
            )

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(13, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
