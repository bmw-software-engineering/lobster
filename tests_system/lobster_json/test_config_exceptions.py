from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from .lobsterjsonasserter import LobsterJsonAsserter


class ConfigParserExceptionsLobsterJsonTest(LobsterJsonSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner_without_config_file_data()

    def test_missing_config_file(self):

        out_file = "missing_config_file.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            'usage: lobster-json [-h] [-v] [--out OUT] --config CONFIG\n'
            'lobster-json: error: the following arguments are required: --config\n'
        )
        asserter.assertExitCode(2)

    def test_config_file_errors(self):
        test_cases = [
            {
                "config_file": "with_syntax_error.yaml",
                "expected_error": "mapping values are not allowed here",
                "case": "syntax_error",
                "expected_exit_code": 1
            },
            {
                "config_file": "with_no_tag_attribute.yaml",
                "expected_error": "missing - tag_attribute",
                "case": "no_tag_error",
                "expected_exit_code": 1
            },
        ]

        for test_case in test_cases:
            with self.subTest(i=test_case["case"]):

                out_file = f"{test_case['case']}.lobster"
                self._test_runner.cmd_args.out = out_file
                self._test_runner.declare_output_file(self._data_directory / out_file)

                self._test_runner.cmd_args.config = str(
                    self._data_directory / test_case["config_file"])

                completed_process = self._test_runner.run_tool_test()
                asserter = LobsterJsonAsserter(self, completed_process,
                                               self._test_runner)

                asserter.assertInStdErr(test_case["expected_error"])
                asserter.assertExitCode(test_case["expected_exit_code"])
