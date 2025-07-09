from .lobster_system_test_case_base import LobsterTrlcSystemTestCaseBase
from ..asserter import Asserter


class InputFromWorkingDirectory(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        config_string = self._test_runner.read_config_from_file(
            self._data_directory / "inputs-from-files-and-inputs.conf")
        self._test_runner.declare_trlc_config(config_string)

    def test_input_from_working_directory(self):
        # lobster-trace: trlc_req.No_Inputs_And_No_Inputs_From_File
        OUT_FILE = "input_from_working_directory.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
        file_paths = [
            self._data_directory / "fruits.trlc",
            self._data_directory / "fruits.rsl",
            self._data_directory / "default_file.trlc",
            self._data_directory / "default_file.rsl"
        ]
        self._test_runner.copy_files_in_working_directory(file_paths)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: successfully wrote 2 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
