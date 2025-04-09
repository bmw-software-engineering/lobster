import threading
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from ..asserter import Asserter
from .mock_server import start_mock_server


class CodebeamerValidScenario(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer reports using a mock HTTPS server."""

    CONFIG_FILE = "codebeamer-config.yaml"

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
        self._test_runner.cmd_args.config = str(self._data_directory / self.CONFIG_FILE)

    def test_valid_query_id(self):
        # lobster-trace: codebeamer_req.Query_Id_Parameter
        """Validate Codebeamer report generation with mock data."""
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn("InsecureRequestWarning", completed_process.stderr)
        self.assertIn("requirements to report.lobster", completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
