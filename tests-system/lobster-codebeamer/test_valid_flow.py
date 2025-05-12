import json
from flask import Response
from .lobster_codebeamer_system_test_case_base import LobsterCodebeamerSystemTestCaseBase
from ..asserter import Asserter
from .mock_server_setup import start_mock_server, get_mock_app


class LobsterCodebeamerTest(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer with a mock HTTPS server returning predefined responses."""

    MOCK_URL = "https://localhost:5000"
    TOKEN = "abcdef1234567890"
    IMPORT_QUERY = 1234458
    OUTPUT_FILE = "report.lobster"

    @classmethod
    def setUpClass(cls):
        start_mock_server()
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.codebeamer_flask.responses = []

    def _configure_runner(self, retry_codes=None, num_retries=None):
        cfg = self._test_runner.config_file_data
        cfg.import_query = self.IMPORT_QUERY
        cfg.root = self.MOCK_URL
        cfg.token = self.TOKEN
        cfg.out = self.OUTPUT_FILE
        if retry_codes is not None:
            cfg.retry_error_codes = retry_codes
        if num_retries is not None:
            cfg.num_request_retry = num_retries

    def test_valid_query_id(self):
        # lobster-trace: codebeamer_req.Query_Id_Parameter
        self._configure_runner()

        response_data = {
            "item": 1,
            "page": 1,
            "total": 1,
            "items": [{"item": {"id": 8, "version": 9, "tracker": {"id": 10}}}],
        }

        self.codebeamer_flask.responses = [
            Response(json.dumps(response_data), status=200),
        ]

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn("requirements to report.lobster", completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
