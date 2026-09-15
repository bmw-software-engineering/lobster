import unittest
from yaml.scanner import ScannerError
from tests_system.lobster_json.lobsterjsonasserter import LobsterJsonAsserter
from tests_system.lobster_json.lobsterjsonsystemtestcasebase import (
    LobsterJsonSystemTestCaseBase
)


class ConfigParserExceptionsLobsterJsonTest(LobsterJsonSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner_without_config_file_data()

    def test_missing_config_file_parameter(self):
        # lobster-trace: json_req.Config_Option_Mandatory
        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            'usage: lobster-json [-h] [-v] [--out OUT] --config CONFIG\n'
            'lobster-json: error: the following arguments are required: --config\n'
        )
        asserter.assertExitCode(2)

    def test_missing_config_file(self):
        # lobster-trace: json_req.Config_File_Not_Found
        self._test_runner.cmd_args.config = str(
            self._data_directory / "missing_config_file.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(
            f'Error: Config file '
            f"'{self._data_directory / 'missing_config_file.yaml'}'"
            f' not found.'
        )

    def test_config_file_errors(self):
        # lobster-trace: json_req.Config_File_Invalid_YAML
        out_file = "syntax_error.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "with_syntax_error.yaml")
        with self.assertRaises(ScannerError) as ctx:
            self._test_runner.run_tool_test()
        self.assertIn("mapping values are not allowed here", str(ctx.exception))

    def test_config_file_empty(self):
        # lobster-trace: json_req.Config_File_Mandatory_Parameter_Missing
        out_file = "no_tag_error.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "whitespace.yaml")
        test_run_result = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, test_run_result, self._test_runner)
        asserter.assertExitCode("Required mandatory parameters missing - tag_attribute")

    def test_config_file_unsupported_key(self):
        # lobster-trace: json_req.Config_File_Unsupported_Key
        self._test_runner.cmd_args.config = str(
            self._data_directory / "with_unsupported_key.yaml")
        with self.assertRaises(KeyError) as ctx:
            self._test_runner.run_tool_test()
        self.assertIn("invalid_key", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
