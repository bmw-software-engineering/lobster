from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from ..asserter import Asserter


class JsonExtensionTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.name_attribute = "fruit"
        self._test_runner.config_file_data.tag_attribute = "vegtable"

    def test_single_non_json_extensions(self):
        # lobster-trace: json_req.Input_File_JSON_Extension
        self._test_runner.declare_input_file(self._data_directory / "valid-json.txt")
        OUT_FILE = "banana.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"<config>: lobster warning: not a .json file\n"
            f"lobster-json: wrote 1 items to {OUT_FILE}\n"
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_mixed_extensions(self):
        # lobster-trace: json_req.Input_File_JSON_Extension
        self._test_runner.declare_input_file(self._data_directory / "valid-mini.json")
        self._test_runner.declare_input_file(self._data_directory / "valid-json.txt")
        OUT_FILE = "apple-banana.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"<config>: lobster warning: not a .json file\n"
            f"lobster-json: wrote 2 items to {OUT_FILE}\n"
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_invalid_json_content(self):
        self._test_runner.declare_input_file(
            self._data_directory / "valid_extension_invalid_json.json"
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn("json.decoder.JSONDecodeError:", completed_process.stderr)
        asserter.assertExitCode(1)
