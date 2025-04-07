from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from ..asserter import Asserter


class InputFileCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(self._data_directory / "test_case.cpp")
        self._test_runner.cmd_args.config = str(
            self._data_directory / "cpptest-config.yaml")

    def test_valid_input_cpptest_file(self):
        # lobster-trace: cpptest_req.Input_File_Valid_Cpp_Test_File

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        self.assertIn('lobster items to', completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
