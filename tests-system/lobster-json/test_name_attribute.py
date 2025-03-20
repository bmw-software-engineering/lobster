from os import makedirs
import shutil
from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from .lobsterjsonasserter import LobsterJsonAsserter
from ..asserter import Asserter


class JsonExtensionTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.tag_attribute = "tags"

    def test_attribute_given(self):
        # lobster-trace: json_req.Name_Attribute_Given
        self._test_runner.declare_input_file(self._data_directory / "basic.json")
        self._test_runner.config_file_data.name_attribute = "name"
        out_file = "basic-with-name.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(6, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_attribute_given_but_key_missing(self):
        # lobster-trace: json_req.Name_Attribute_Given_Key_Missing
        self._test_runner.declare_input_file(self._data_directory / "single2.json")
        self._test_runner.config_file_data.name_attribute = "name-not-in-item"
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "{'actual': {'expect': 42,\n"
            "            'inputs': [1, 2, 3],\n"
            "            'name': 'Single_Item',\n"
            "            'tags': 'link-to-requirement'}}\n"
            "single2.json: malformed input: object does not contain name-not-in-item\n"
            "lobster-json: aborting due to earlier errors\n"
        )
        asserter.assertExitCode(1)

    def test_name_attribute_missing_flat_input(self):
        # lobster-trace: json_req.Name_Attribute_Missing
        self._test_runner.declare_input_file(self._data_directory / "basic.json")
        out_file = "basic-without-name.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(6, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_name_attribute_missing_nested_input(self):
        # lobster-trace: json_req.Name_Attribute_Missing
        nested_directory = self._test_runner.working_dir / "one" / "two"
        makedirs(nested_directory, exist_ok=False)
        shutil.copy(
            src=self._data_directory / "basic.json",
            dst=nested_directory,
        )

        out_file = "basic-without-name-nested.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(6, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
