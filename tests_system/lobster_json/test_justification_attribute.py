from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from .lobsterjsonasserter import LobsterJsonAsserter


class JsonJustificationAttributeTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.tag_attribute = "RequirementIDs"
        self._test_runner.config_file_data.name_attribute = "Name"

    def test_justification_attribute_given(self):
        self._test_runner.declare_input_file(
            self._data_directory / "justification_attribute_given.json")

        self._test_runner.config_file_data.justification_attribute = "Justification"
        out_file = "justification_attribute_given.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_justification_attribute_given_but_key_missing(self):
        self._test_runner.declare_input_file(
            self._data_directory / "justification_attribute_given.json")

        self._test_runner.config_file_data.justification_attribute = "missingkey"

        out_file = "justification_attribute_irrelavent.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_justification_attribute_not_given(self):
        self._test_runner.declare_input_file(
            self._data_directory / "justification_attribute_given.json")

        out_file = "justification_attribute_not_given.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
