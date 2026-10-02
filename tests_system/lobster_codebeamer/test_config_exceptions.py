import unittest
from tests_system.lobster_codebeamer.lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from tests_system.asserter import Asserter
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
