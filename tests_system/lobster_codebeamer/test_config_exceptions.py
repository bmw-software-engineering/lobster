import unittest
from tests_system.lobster_codebeamer.lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from tests_system.asserter import Asserter
from tests_system.testrunner import TestRunner
from tests_system.lobster_codebeamer.mock_server_setup import get_mock_app


class LobsterCodebeamerConfigExceptionsTest(LobsterCodebeamerSystemTestCaseBase):
    """System tests for configuration errors that are detected before any
    request is sent to codebeamer."""

    @classmethod
    def setUpClass(cls):
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self.codebeamer_flask.reset()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.verify_ssl = False

    def test_missing_default_config_file_raises_error(self):
        # lobster-trace: codebeamer_req.Default_Config_File_Used
        # GIVEN no config path is specified and the default config file does not exist
        self._test_runner.cmd_args.config = None

        # WHEN the tool is run
        # (base class call, because the derived runner would create the file)
        completed_process = TestRunner.run_tool_test(self._test_runner)
        asserter = Asserter(self, completed_process, self._test_runner)

        # THEN the tool reports the default config file and exits with a non-zero code
        expected_file_name = str(
            self._test_runner.working_dir / 'codebeamer-config.yaml')
        asserter.assertStdErrText(
            f"lobster-codebeamer: File '{expected_file_name}' "
            "not found.\n"
        )
        asserter.assertExitCode(1)

    def test_missing_specified_config_file_raises_error(self):
        # lobster-trace: codebeamer_req.Config_File_Path_Error
        # GIVEN the specified config file does not exist
        self._test_runner.cmd_args.config = "does-not-exist.yaml"

        # WHEN the tool is run
        # (base class call, because the derived runner would create the file)
        completed_process = TestRunner.run_tool_test(self._test_runner)
        asserter = Asserter(self, completed_process, self._test_runner)

        # THEN the tool prints an error message and exits with a non-zero code
        asserter.assertStdErrText(
            f"lobster-codebeamer: File '{self._test_runner.cmd_args.config}' "
            "not found.\n"
        )
        asserter.assertExitCode(1)

    def test_config_file_is_directory_raises_error(self):
        # lobster-trace: codebeamer_req.Config_File_Path_Error
        # GIVEN the config file argument is a directory
        self._test_runner.cmd_args.config = str(self._test_runner.working_dir)

        # WHEN the tool is run
        # (base class call, because the derived runner would create the file)
        completed_process = TestRunner.run_tool_test(self._test_runner)
        asserter = Asserter(self, completed_process, self._test_runner)

        # THEN the tool prints an error message and exits with a non-zero code
        # Note: The error message depends on the operating system.
        message_posix = "lobster-codebeamer: Path " \
            f"'{self._test_runner.cmd_args.config}' is a directory, but a file was " \
            "expected.\n"
        message_windows = "lobster-codebeamer: Permission denied for " \
            f"'{self._test_runner.cmd_args.config}'.\n"
        if (completed_process.stderr != message_posix) \
                and (completed_process.stderr != message_windows):
            self.fail(f"Unexpected STDERR: {completed_process.stderr}")
        asserter.assertExitCode(1)

    def test_unsupported_config_key_raises_error(self):
        # lobster-trace: codebeamer_req.Unsupported_Config_Keys_Rejected
        # lobster-trace: codebeamer_req.Default_Config_File_Used
        # GIVEN the config file contains an unsupported key
        self._test_runner.cmd_args.config = None
        config_path = self._test_runner.working_dir / "codebeamer-config.yaml"
        config_path.write_text(
            "unsupported_key: value-of-unsupported-key\n",
            encoding="UTF-8",
        )

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        # THEN the tool identifies the unsupported key and exits with a non-zero code
        asserter.assertInStdErr("Unsupported config keys: unsupported_key.")
        asserter.assertExitCode(1)

    def test_empty_import_query_raises_error(self):
        # lobster-trace: codebeamer_req.No_Source_Parameter

        # GIVEN a configuration file where both import_query and import_tagged are not
        # provided
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)

        COMBINATIONS = (None, "")
        for import_tagged_value in COMBINATIONS:
            for import_query_value in COMBINATIONS:
                cfg.import_tagged = import_tagged_value
                cfg.import_query = import_query_value

                # WHEN the tool is run with this configuration
                completed_process = self._test_runner.run_tool_test()

                # THEN the tool shall display an error message and exit with a non-zero
                # return code
                asserter = Asserter(self, completed_process, self._test_runner)
                asserter.assertStdErrText(
                    "lobster-codebeamer: 'Either import_tagged or import_query "
                    "must be provided!'\n"
                )
                asserter.assertExitCode(1)

    def test_negative_numeric_import_query_string_raises_error(self):
        # lobster-trace: codebeamer_req.Invalid_Import_Query_String_Format
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = "-123"

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "usage: lobster-codebeamer [-h] [-v] [--config CONFIG] [--out OUT]\n"
            "lobster-codebeamer: error: import_query must be a positive integer\n"
        )
        asserter.assertExitCode(2)

    def test_negative_non_numeric_import_query_string_raises_error(self):
        # lobster-trace: codebeamer_req.Invalid_Import_Query_String_Format
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = "-abc"

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "usage: lobster-codebeamer [-h] [-v] [--config CONFIG] [--out OUT]\n"
            "lobster-codebeamer: error: import_query must be a valid cbQL query\n"
        )
        asserter.assertExitCode(2)


if __name__ == "__main__":
    unittest.main()
