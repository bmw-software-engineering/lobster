from .lobster_system_test_case_base import LobsterTrlcSystemTestCaseBase
from ..asserter import Asserter


class TrlcInvalidExtensionsTest(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_trlc_config_file(self._data_directory /
                                                   "lobster-trlc.conf")

    def test_invalid_extensions_inputs_files_list(self):
        # lobster-trace: trlc_req.Invalid_Inputs_List_Of_Files_Extensions
        self._test_runner.declare_input_file(self._data_directory /
                                             "rsl_invalid_extension.slr")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_invalid_extension.clrt")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("<config>: lobster warning: not a .rsl or .trlc"
                                  " file\n<config>: lobster warning: not a .rsl or"
                                  " .trlc file\nrsl_invalid_extension.slr: error:"
                                  " is not a rsl or trlc"
                                  " file\ntrlc_invalid_extension.clrt: error: is not"
                                  " a rsl or trlc file\ntest_default.namaste"
                                  " {\n^^^^^^^^^^^^ lobster-trlc.conf:1: error:"
                                  " unknown symbol test_default\nlobster-trlc:"
                                  " aborting due to error in configuration file"
                                  " 'lobster-trlc.conf'\n")
        asserter.assertExitCode(1)

    def test_invalid_extensions_input_from_file(self):
        # lobster-trace: trlc_req.Invalid_Inputs_From_File_Extensions
        self._test_runner.declare_inputs_from_file(self._data_directory /
                                                   "invalid_ext_inputs_from_file.txt",
                                                   self._data_directory)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("invalid_ext_inputs_from_file.txt:1: "
                                  "lobster warning: not a .rsl or .trlc"
                                  " file\ninvalid_ext_inputs_from_file.txt:2:"
                                  " lobster warning: not a .rsl or"
                                  " .trlc file\nrsl_invalid_extension.slr: error:"
                                  " is not a rsl or trlc "
                                  "file\ntrlc_invalid_extension.clrt: error: "
                                  "is not a rsl or trlc file\ntest_default.namaste "
                                  "{\n^^^^^^^^^^^^ lobster-trlc.conf:1: error: "
                                  "unknown symbol test_default\nlobster-trlc:"
                                  " aborting due to error in configuration file"
                                  " 'lobster-trlc.conf'\n")
        asserter.assertExitCode(1)
