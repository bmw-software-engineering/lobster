from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from ..asserter import Asserter


class InputFileCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(self._data_directory / "test_case.cpp")

    def test_valid_input_cpptest_file(self):
        # lobster-trace: cpptest_req.Input_File_Valid_Cpp_Test_File
        self._test_runner.cmd_args.config = str(
            self._data_directory / "cpptest-config.yaml")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        self.assertIn('lobster items to', completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_invalid_input_cpptest_file(self):
        # lobster-trace: cpptest_req.Invalid_Config_File
        self._test_runner.cmd_args.config = str(
            self._data_directory / "cpptest-config-invalid-syntax.yaml")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn('raise LOBSTER_Exception(message="Invalid config file")',
                      completed_process.stderr)
        asserter.assertExitCode(1)
        asserter.assertOutputFiles()

    def test_invalid_parameters_input_cpptest_file(self):
        # lobster-trace: cpptest_req.Invalid_Config_File_Parameters
        self._test_runner.cmd_args.config = str(
            self._data_directory / "cpptest-config-invalid.yaml")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertStdErrText('usage: lobster-cpptest [-h] [-v, --version]'
                                  ' [--config CONFIG]\nlobster-cpptest: error: Please'
                                  ' follow the right config file structure! Missing'
                                  ' attribute "markers" for output file'
                                  ' "component_tests.lobster"\n')
        asserter.assertExitCode(2)
