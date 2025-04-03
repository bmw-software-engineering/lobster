import subprocess
import time
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from ..asserter import Asserter


class CodebeamerValidScenario(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer reports using a mock HTTPS server."""

    MOCK_SERVER_SCRIPT = "tests-system/lobster-codebeamer/mock_server.py"
    CONFIG_FILE = "codebeamer-config.yaml"

    @classmethod
    def setUpClass(cls):
        """Start the mock server before any tests run."""
        cls.mock_server = subprocess.Popen(["python", cls.MOCK_SERVER_SCRIPT])
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        """Terminate the mock server after all tests."""
        if cls.mock_server:
            cls.mock_server.terminate()
            cls.mock_server.wait()

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.cmd_args.config = str(self._data_directory / self.CONFIG_FILE)

    def test_valid_scenario(self):
        """Validate Codebeamer report generation with mock data."""
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        self.assertIn("InsecureRequestWarning", completed_process.stderr)
        self.assertIn("requirements to report.lobster", completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
