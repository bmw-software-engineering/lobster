from pathlib import Path
import shutil
from .lobsterjsonasserter import LobsterJsonAsserter
from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase


class InputsAndInputsFromFileParameterTest(LobsterJsonSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.tag_attribute = "RequirementIDs"
        self._test_runner.config_file_data.justification_attribute = "Justification"
        self._test_runner.config_file_data.test_list = "TestCases"
        self._test_runner.config_file_data.name_attribute = "Name"

    def test_inputs(self):
        self._test_runner.declare_input_file(
            self._data_directory / "inputs_safety.json")
        self._test_runner.declare_input_file(
            self._data_directory / "inputs_non_critical.json")
        self._test_runner.declare_input_file(
            self._data_directory / "inputs_cosmetic.json")

        out_file = "inputs.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(14, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_inputs_from_file(self):
        self._test_runner.declare_inputs_from_file(
            self._data_directory / "inputs_from_file.txt", self._data_directory)

        out_file = "inputs_from_file.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(14, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_consume_files_from_cwd(self):
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "inputs_non_critical.json")
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "inputs_safety.json")

        out_file = "files_from_cwd.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(10, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_consume_files_and_nested_directory_from_cwd(self):
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "inputs_non_critical.json")
        self._test_runner.copy_file_to_working_directory(
            self._data_directory / "inputs_safety.json")

        # Copy the "nested_directory_data" directory into the working directory
        source_dir = Path(self._data_directory / "nested_directory_data")
        dest_dir = Path(self._test_runner.working_dir / "nested_directory_data")
        shutil.copytree(source_dir, dest_dir)

        out_file = "file_and_nested_directories.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(15, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
