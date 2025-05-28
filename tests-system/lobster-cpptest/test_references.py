from pathlib import Path
from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from .lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from ..tests_utils.update_cpptest_expected_output import update_cpptest_output_file

class ReferencesCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_no_references_cpptest_file(self):
        # lobster-trace: cpptest_req.Input_File_Valid_Cpp_Test_File
        self.OUT_FILE = "no_references.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.declare_input_file(self._data_directory / "no_references.cpp")
        self._test_runner.declare_output_file(self._data_directory / self.OUT_FILE)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "no_references_config.yaml")
        
        self.out_file_path = self._data_directory / self.OUT_FILE
        with open(self.out_file_path, 'r') as file:
            self.original_contents = file.read()

        update_cpptest_output_file(
            self.out_file_path,
            expected_location=self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(6, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
    
    def test_one_reference_in_cpptest_file(self):
        # lobster-trace: cpptest_req.Input_File_Valid_Cpp_Test_File
        self.OUT_FILE = "1_reference.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.declare_input_file(self._data_directory / "1_reference.cpp")
        self._test_runner.declare_output_file(self._data_directory / self.OUT_FILE)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "1_reference_config.yaml")
        
        self.out_file_path = self._data_directory / self.OUT_FILE
        with open(self.out_file_path, 'r') as file:
            self.original_contents = file.read()

        update_cpptest_output_file(
            self.out_file_path,
            expected_location=self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
    
    def test_many_references_in_cpptest_file(self):
        # lobster-trace: cpptest_req.Input_File_Valid_Cpp_Test_File
        self.OUT_FILE = "many_references.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.declare_input_file(self._data_directory / "many_references.cpp")
        self._test_runner.declare_output_file(self._data_directory / self.OUT_FILE)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "many_references_config.yaml")
        
        self.out_file_path = self._data_directory / self.OUT_FILE
        with open(self.out_file_path, 'r') as file:
            self.original_contents = file.read()

        update_cpptest_output_file(
            self.out_file_path,
            expected_location=self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(13, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
    
    def tearDown(self):
        super().tearDown()
        with open(self.out_file_path, 'w') as file:
            file.write(self.original_contents)