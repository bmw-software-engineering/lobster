from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from ..asserter import Asserter


class ValidInputTest(LobsterJsonSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_input_with_specific_schema(self):

        out_file = "specific_schema.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.config_file_data.tag_attribute = "requirements"
        self._test_runner.config_file_data.name_attribute = "description"

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_input_file(self._data_directory /
                                             "specific_schema.json")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "lobster-json: wrote 2 items to specific_schema.lobster\n"
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
