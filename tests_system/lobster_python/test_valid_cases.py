import unittest

from tests_system.asserter import Asserter
from tests_system.lobster_python.lobster_python_system_test_case_base import (
    LobsterPythonSystemTestCaseBase,
)
from tests_system.lobster_python.\
    lobster_python_asserter import LobsterPythonTestAsserter as Asserter


class ValidCasesPython(LobsterPythonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_valid_python(self):
        """Simple Python file and verifies the generated lobster output."""
        OUT_FILE = "basic.lobster"

        self._test_runner.declare_input_file(self._data_directory / "basic.py")

        self._test_runner.cmd_args.files = ["basic.py"]
        self._test_runner.cmd_args.single = True
        self._test_runner.cmd_args.out = OUT_FILE

        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(3, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
