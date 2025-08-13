from .lobster_pkg_system_test_case_base import LobsterPKGSystemTestCaseBase
from ..asserter import Asserter


class InvalidInputFilePkgTest(LobsterPKGSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_not_existing_pkg_file(self):
        OUT_FILE = "not_existing.lobster"
        non_existing_file = str(
            self._data_directory / "not_existing.pkg")
        self._test_runner.cmd_args.files = [non_existing_file]

        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(
            self._data_directory / OUT_FILE)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn(f'{non_existing_file} is not a file or directory', completed_process.stderr)
        asserter.assertExitCode(1)
