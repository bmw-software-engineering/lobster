from pathlib import Path
from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from .lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from ..tests_utils.update_cpptest_expected_output import update_cpptest_output_file


class InputFileCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_valid_input_cpptest_file(self):
        # lobster-trace: cpptest_req.Input_File_Valid_Cpp_Test_File
        OUT_FILE = "report.lobster"
        self._test_runner.declare_input_file(self._data_directory / "1_reference.cpp")
        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_cpptest_flow.yaml")

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
