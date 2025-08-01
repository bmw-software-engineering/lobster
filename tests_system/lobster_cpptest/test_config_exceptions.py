from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from ..asserter import Asserter


class ConfigParserExceptionsCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(self._data_directory / "test_case.cpp")

    def test_missing_config_file(self):
        # lobster-trace: UseCases.Config_File_Missing

        self._test_runner.cmd_args.config = str(
            self._data_directory / "non-existing.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertStdErrText(
            f'usage: lobster-cpptest [-h] [-v] [--config CONFIG]\n'
            f'lobster-cpptest: error: {self._test_runner.cmd_args.config} '
            'is not an existing file!\n'
        )
        asserter.assertExitCode(2)

    def test_config_file_errors(self):
        test_cases = [
            {
                "config_file": "with_syntax_error.yaml",
                "expected_error": "Invalid config file",
                "case": "syntax_error",
                "expected_exit_code": 1
            },
            {
                "config_file": "with_key_error.yaml",
                "expected_error": (
                    'usage: lobster-cpptest [-h] [-v] [--config CONFIG]\n'
                    'lobster-cpptest: error: Please follow the right config '
                    'file structure! Missing attribute "output" and "codebeamer_url"\n'
                ),
                "case": "key_error",
                "expected_exit_code": 2
            },
            {
                "config_file": "with_no_markers.yaml",
                "expected_error": (
                    'usage: lobster-cpptest [-h] [-v] [--config CONFIG]\n'
                    'lobster-cpptest: error: Please follow the right config '
                    'file structure! Missing attribute "markers" for output file '
                    '"component_tests.lobster"\n'
                ),
                "case": "no_markers",
                "expected_exit_code": 2
            },
            {
                "config_file": "with_no_kind.yaml",
                "expected_error": (
                    'usage: lobster-cpptest [-h] [-v] [--config CONFIG]\n'
                    'lobster-cpptest: error: Please follow the right config '
                    'file structure! Missing attribute "kind" for output file '
                    '"component_tests.lobster"\n'
                ),
                "case": "no_kind",
                "expected_exit_code": 2
            },
            {
                "config_file": "with_not_supported_markers.yaml",
                "expected_error": (
                    'usage: lobster-cpptest [-h] [-v] [--config CONFIG]\n'
                    'lobster-cpptest: error: "@marker1" is not a supported '
                    '"markers" value for output file "component_tests.lobster". '
                    'Supported values are: "@requirement, @requiredby, @defect"\n'
                ),
                "case": "not_supported_markers",
                "expected_exit_code": 2
            }
        ]

        # lobster-trace: cpptest_req.Input_File_Invalid_Cpp_Test_File
        # lobster-trace: UseCases.Config_File_Syntax_Error
        # lobster-trace: UseCases.Config_File_Key_Error
        for test_case in test_cases:
            with self.subTest(i=test_case["case"]):
                self._test_runner.cmd_args.config = str(
                    self._data_directory / test_case["config_file"]
                )

                completed_process = self._test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, self._test_runner)

                asserter.assertInStdErr(test_case["expected_error"])
                asserter.assertExitCode(test_case["expected_exit_code"])
