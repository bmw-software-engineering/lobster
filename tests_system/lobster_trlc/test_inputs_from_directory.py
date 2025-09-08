import os
import shutil
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class InputFromDirectory(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.conversion_rules = [
            self.BERRY_CONVERSION_RULE,
            self.NAMASTE_CONVERSION_RULE,
        ]

    def test_input_from_directory(self):
        """Test that a directory is processed"""
        # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC

        # TODO: the test folder structure is not recursive, but it should be
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
        os.makedirs(self._test_runner.working_dir / "nested", exist_ok=True)
        shutil.copy(
            self._data_directory / "fruits_nested.trlc",
            self._test_runner.working_dir / "nested" / "fruits_nested.trlc"
        )
        self._test_runner.config_file_data.inputs = ["."]
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: successfully wrote 3 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
