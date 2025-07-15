import json
from flask import Response
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from ..asserter import Asserter
from .mock_server_setup import start_mock_server, get_mock_app


class LobsterCodebeamerTest(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer with a mock HTTPS server returning
    predefined responses."""

    @classmethod
    def setUpClass(cls):
        """Start the mock server once before any tests run."""
        start_mock_server()
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self.codebeamer_flask.reset()
        self._test_runner = self.create_test_runner()

    def test_retry_if_configured(self):
        """Ensure the tool retries and exits after exhausting
        retries on specified error codes."""
        # lobster-trace: codebeamer_req.Retry_On_Specific_HTTPS_Status_Codes

        self.codebeamer_flask.responses = [Response(status=429)] * 3
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out()
        cfg.retry_error_codes = [429]
        cfg.num_request_retry = 3
        cfg.import_query = 999

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn(
            "[Attempt 1/3] Retryable error: 429\n"
            "[Attempt 2/3] Retryable error: 429\n"
            "[Attempt 3/3] Retryable error: 429\n"
            f"Could not fetch {cfg.root}/api/"
            f"v3/reports/{cfg.import_query}/items?page=1&pageSize=100.\n",
            completed_process.stdout,
        )
        asserter.assertExitCode(1)

    def test_retry_then_success(self):
        """Ensure the tool retries and uses successful response
        if received within retry limit."""
        # lobster-trace: codebeamer_req.Retry_On_Specific_HTTPS_Status_Codes
        response_data = {
            'page': 1,
            'pageSize': 1,
            'total': 1,
            'items': [
                {
                    'item': {
                        'id': 5,
                        'name': 'Requirement 5: Dynamic name',
                        'description': 'Dynamic description for requirement 5.',
                        'status': {
                            'id': 5,
                            'name': 'Status 5',
                            'type': 'ChoiceOptionReference'
                        },
                        'tracker': {
                            'id': 5,
                            'name': 'Tracker_Name_5',
                            'type': 'TrackerReference'
                        },
                        'version': 1
                    }
                }
            ]
        }
        self.codebeamer_flask.responses = [
            Response(status=429),
            Response(status=429),
            Response(json.dumps(response_data), status=200),
        ]
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out()
        cfg.retry_error_codes = [429]
        cfg.num_request_retry = 3
        cfg.import_query = 123123123123123123
        self._test_runner.declare_output_file(
            self._data_directory / self._test_runner.config_file_data.out)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn(
            "[Attempt 1/3] Retryable error: 429\n"
            "[Attempt 2/3] Retryable error: 429\n"
            "Written 1 requirements to codebeamer.lobster\n",
            completed_process.stdout,
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_no_retry_if_not_configured(self):
        """Ensure the tool does NOT retry if RETRY_ERROR_CODES is not defined."""
        # lobster-trace: codebeamer_req.Missing_Error_Code
        self.codebeamer_flask.responses = [Response(status=429)]
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out()
        cfg.import_query = 1111

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn(
            "[Attempt 1/5] Failed with status 429\n"
            f"Could not fetch {self._test_runner.config_file_data.root}/"
            f"api/v3/reports/{cfg.import_query}/items?page=1&pageSize=100.\n",
            completed_process.stdout,
        )
        self.assertNotIn("Retrying request", completed_process.stdout)
        asserter.assertExitCode(1)
