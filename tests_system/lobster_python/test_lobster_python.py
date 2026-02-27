from pathlib import Path
import shutil
import unittest

from tests_system.lobster_python.\
    lobster_python_system_test_case_base import LobsterPythonSystemTestCaseBase
from tests_system.lobster_python.\
    lobster_python_asserter import LobsterPythonAsserter as Asserter


class LobsterPythonSystemTest(LobsterPythonSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_file_from_current_directory(self):
        """
        Tests hello_world.py in the current directory.
        Output written with schema imp and version 3.
        """

        OUT_FILE = "hello_world.lobster"
        IN_FILE = "hello_world.py"

        in_file = self._data_directory / IN_FILE
        self._test_runner.copy_file_to_working_directory(in_file)

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        self._test_runner.cmd_args.files.append(IN_FILE)
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.cmd_args.single = True

        self._test_runner.cmd_args.kind = "imp"

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFileDeprecated(1, OUT_FILE, "lobster-imp-trace", 3)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_file_from_current_directory_no_schema(self):
        """
        Tests hello_world.py in the current directory.
        Output written without schema and version 5.
        """

        OUT_FILE = "hello_world_no_schema.lobster"
        IN_FILE = "hello_world.py"

        in_file = self._data_directory / IN_FILE
        self._test_runner.copy_file_to_working_directory(in_file)

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        self._test_runner.cmd_args.files.append(IN_FILE)
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.cmd_args.single = True

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
