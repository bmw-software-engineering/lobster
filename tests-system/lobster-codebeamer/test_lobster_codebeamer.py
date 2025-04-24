import json
import threading
from flask import jsonify, Response
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from ..asserter import Asserter
from .mock_server import create_app


# Note: Currently the Flask mock server is not teared down.
# It is created once, and that instance is reused for all tests.
# For that reason all tests must be written in this file, or the mock server has to be
# teared down, or the other server must use a different port.


class LobsterCodebeamerTest(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer with mock HTTPS server returning predefined
       responses."""

    @classmethod
    def setUpClass(cls):
        """Start the mock server thread before any tests run."""
        cls.codebeamer_flask = create_app()
        cls.mock_server_thread = threading.Thread(
            target=cls.codebeamer_flask.start_server,
            daemon=True
        )
        cls.mock_server_thread.start()

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_retry_if_configured(self):
        # lobster-trace: codebeamer_req.Retry_On_Specific_HTTPS_Status_Codes
        """Ensure the tool retries and exits on HTTPS error from mock server."""

        self.codebeamer_flask.responses = [
            Response(status=429),
            Response(status=429),
            Response(status=429),
        ]

        CONFIG_FILE = "codebeamer-config-retry-configured.yaml"
        self._test_runner.cmd_args.config = str(self._data_directory / CONFIG_FILE)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn(
            "[Attempt 1/3] Retryable error: 429\n"
            "[Attempt 2/3] Retryable error: 429\n"
            "[Attempt 3/3] Retryable error: 429\n"
            "Could not fetch https://localhost:5000/api/"
            "v3/reports/1234458/items?page=1&pageSize=100.\n",
            completed_process.stdout
        )
        asserter.assertExitCode(1)

    def test_retry_then_success(self):
        # lobster-trace: codebeamer_req.Retry_On_Specific_HTTPS_Status_Codes
        """Ensure the tool retries and uses the result if the server replied to one of
        the retry attempts."""

        data = {
            "item": 1,
            "page": 1,
            "total": 1,
            "items": [{"item": {"id": 8, "version": 9, "tracker": {"id": 10}}}]
        }

        self.codebeamer_flask.responses = [
            Response(status=429),
            Response(status=429),
            Response(json.dumps(data), status=200),
        ]

        CONFIG_FILE = "codebeamer-config-retry-configured.yaml"
        self._test_runner.cmd_args.config = str(self._data_directory / CONFIG_FILE)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn(
            "[Attempt 1/3] Retryable error: 429\n"
            "[Attempt 2/3] Retryable error: 429\n"
            "Written 1 requirements to report.lobster\n",
            completed_process.stdout
        )
        asserter.assertExitCode(0)

    def test_no_retry_if_not_configured(self):
        # lobster-trace: codebeamer_req.Missing_Error_Code
        """Ensure the tool does NOT retry if RETRY_ERROR_CODES is not defined."""

        self.codebeamer_flask.responses = [
            Response(status=429),
        ]

        CONFIG_FILE = "codebeamer-config-retry-not_configured.yaml"
        self._test_runner.cmd_args.config = str(self._data_directory / CONFIG_FILE)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn(
            "[Attempt 1/5] Failed with status 429\n"
            "Could not fetch https://localhost:5000/"
            "api/v3/reports/1234458/items?page=1&pageSize=100.\n",
            completed_process.stdout
        )
        self.assertNotIn("Retrying request", completed_process.stdout)
        asserter.assertExitCode(1)

    def test_valid_query_id(self):
        # lobster-trace: codebeamer_req.Query_Id_Parameter
        """Validate Codebeamer report generation with mock data."""
        self._test_runner.cmd_args.config = str(self._data_directory /
                                                "codebeamer-config.yaml")
        data = {
            "item": 1,
            "page": 1,
            "total": 1,
            "items": [{"item": {"id": 8, "version": 9, "tracker": {"id": 10}}}]
        }

        self.codebeamer_flask.responses = [
            Response(json.dumps(data), status=200),
        ]

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn("requirements to report.lobster", completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
