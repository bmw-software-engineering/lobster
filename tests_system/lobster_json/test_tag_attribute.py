from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from .lobsterjsonasserter import LobsterJsonAsserter
from ..asserter import Asserter


class JsonTagAttributeTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_tag_attribute_given(self):
        self._test_runner.declare_input_file(
            self._data_directory / "tag_attribute_given.json")
        self._test_runner.config_file_data.tag_attribute = "Requirements"
        out_file = "tag_attribute_requirements.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(8, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tag_attribute_given_but_key_missing(self):
        self._test_runner.declare_input_file(
            self._data_directory / "tag_attribute_given_key_missing.json")
        self._test_runner.config_file_data.tag_attribute = "missingkey"
        out_file = "tag_attribute_irrelavent.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(4, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tag_attribute_missing(self):
        self._test_runner.declare_input_file(self._data_directory / "basic.json")
        # Intentionally not setting tag_attribute (it's mandatory)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "Required mandatory parameters missing - tag_attribute\n")
        asserter.assertNoStdOutText()
        asserter.assertExitCode(1)
