from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class TrlcInvalidExtensionsTest(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.conversion_rules = [
            self.NAMASTE_CONVERSION_RULE,
        ]

    def test_invalid_extensions_inputs_files_list(self):
        # lobster-trace: trlc_req.Invalid_Inputs_List_Of_Files_Extensions
        # lobster-trace: UseCases.TRLC_Config_File_Syntax_Error
        self._test_runner.declare_input_file(self._data_directory /
                                             "rsl_invalid_extension.slr")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_invalid_extension.clrt")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "lobster-trlc: File rsl_invalid_extension.slr does not have a valid "
            "extension. Expected one of .rsl, .trlc.\n"
        )
        asserter.assertExitCode(1)

    def test_invalid_extensions_input_from_file(self):
        # lobster-trace: trlc_req.Invalid_Inputs_From_File_Extensions
        # lobster-trace: UseCases.TRLC_Config_File_Syntax_Error
        self._test_runner.declare_inputs_from_file(self._data_directory /
                                                   "invalid_ext_inputs_from_file.txt",
                                                   self._data_directory)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "lobster-trlc: File rsl_invalid_extension.slr does not have a valid "
            "extension. Expected one of .rsl, .trlc.\n"
        )
        asserter.assertExitCode(1)
