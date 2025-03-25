from .lobster_system_test_case_base import LobsterTrlcSystemTestCaseBase
from ..asserter import Asserter


class InputFromFilesAndInputsTest(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(self._data_directory / "default_file.rsl")
        self._test_runner.declare_input_file(self._data_directory / "default_file.trlc")
        self._test_runner.declare_trlc_config_file(
            self._data_directory / "inputs-from-files-and-inputs.conf")

    def test_input_from_files_and_inputs_list(self):
        # lobster-trace: trlc_req.Input_list_Of_File_And_Inputs_From_File
        OUT_FILE = "input_from_files_and_inputs.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
        self._test_runner.declare_inputs_from_file(self._data_directory /
                                                   "input_from_files_and_inputs.txt",
                                                   self._data_directory)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: successfully wrote 2 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_duplicate_contents_input_from_files_and_inputs_list(self):
        # lobster-trace: trlc_req.Duplicate_Input_list_Of_File_And_Inputs_From_File
        self._test_runner.declare_inputs_from_file(
            self._data_directory / "input_from_files_and_inputs_duplicate_contents.txt",
            self._data_directory)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText('package test_default\n        ^^^^^^^^^^^^'
                                  ' default_file_copy.rsl:1: error:'
                                  ' duplicate definition, previous definition at'
                                  ' default_file.rsl:1\nnamaste goodname {\n'
                                  '        ^^^^^^^^ default_file_copy.trlc:3: error:'
                                  ' duplicate definition, previous definition at'
                                  ' default_file.trlc:3\nlobster-trlc: aborting due'
                                  ' to earlier error\n')
        asserter.assertExitCode(1)
