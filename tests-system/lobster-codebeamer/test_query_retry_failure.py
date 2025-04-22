import threading
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from ..asserter import Asserter
from .mock_server import start_mock_server


class CodebeamerErrorScenario(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer with mock HTTPS server returning error."""

    @classmethod
    def setUpClass(cls):
        """Start the mock server thread before any tests run."""
        cls.mock_server_thread = threading.Thread(
            target=start_mock_server,
            daemon=True
        )
        cls.mock_server_thread.start()

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_retry_if_configured(self):
        # lobster-trace: codebeamer_req.Retry_On_Specific_HTTPS_Status_Codes
        """Ensure the tool retries and exits on HTTPS error from mock server."""
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

    def test_retry_success(self):
        """Ensure the tool retries and exits on HTTPS error from mock server."""
        CONFIG_FILE = "codebeamer-config-retry-configured.yaml"
        self._test_runner.cmd_args.config = str(self._data_directory / CONFIG_FILE)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn(
            "[Attempt 1/3] Retryable error: 429\n"
            "[Attempt 2/3] Retryable error: 429\n",
            completed_process.stdout
        )
        asserter.assertExitCode(0)

    def test_no_retry_if_not_configured(self):
        # lobster-trace: codebeamer_req.Missing_Error_Code
        """Ensure the tool does NOT retry if RETRY_ERROR_CODES is not defined."""
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
