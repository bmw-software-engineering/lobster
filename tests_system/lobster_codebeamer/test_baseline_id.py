import json
import unittest
from flask import Response
from tests_system.lobster_codebeamer.lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from tests_system.asserter import Asserter
from tests_system.lobster_codebeamer.lobster_codebeamer_asserter import (
    LobsterCodebeamerAsserter)
from tests_system.lobster_codebeamer.mock_server_setup import get_mock_app


class LobsterCodebeamerBaselineIdTest(LobsterCodebeamerSystemTestCaseBase):
    """System tests for baseline_id validation and usage."""

    @classmethod
    def setUpClass(cls):
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self.codebeamer_flask.reset()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.verify_ssl = False

    def test_baseline_id_with_import_tagged_raises_error(self):
        """Ensure baseline_id combined with import_tagged exits with error."""
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_tagged = "some_file.lobster"
        cfg.baseline_id = 12345

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(1)
        asserter.assertStdErrText(
            "lobster-codebeamer: 'The keys baseline_id and import_tagged "
            "are both present in the configuration, but they are mutually "
            "exclusive!'\n"
        )

    def test_baseline_id_with_numeric_import_query_raises_error(self):
        """Ensure baseline_id combined with a numeric import_query exits
        with error."""
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = 9999
        cfg.baseline_id = 12345

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(1)
        asserter.assertStdErrText(
            "lobster-codebeamer: 'The key baseline_id is only allowed if "
            "import_query is a cbQL query string, not a numeric report ID!'\n"
        )

    def test_baseline_id_negative_raises_error(self):
        """Ensure a negative baseline_id exits with error."""
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = "tracker.id IN (123)"
        cfg.baseline_id = -1

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(1)
        asserter.assertStdErrText(
            "lobster-codebeamer: baseline_id must be a positive integer.\n"
        )

    def test_baseline_id_zero_raises_error(self):
        """Ensure baseline_id of 0 exits with error."""
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = "tracker.id IN (123)"
        cfg.baseline_id = 0

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(1)
        asserter.assertStdErrText(
            "lobster-codebeamer: baseline_id must be a positive integer.\n"
        )

    def test_baseline_id_with_cbql_query_succeeds(self):
        """Ensure baseline_id with a cbQL string query works and appends
        baselineId to the URL."""
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = "tracker.id IN (123)"
        cfg.baseline_id = 407126303

        response_data = {
            'page': 1,
            'pageSize': 1,
            'total': 1,
            'items': [
                {
                    'id': 5,
                    'name': 'Requirement 5: Dynamic name',
                    'description': 'Dynamic description',
                    'status': {
                        'id': 5,
                        'name': 'Status 5',
                        'type': 'ChoiceOptionReference'
                    },
                    'tracker': {
                        'id': 5,
                        'name': 'Tracker_Name_5',
                        'type': 'TrackerReference',
                    },
                    'version': 1,
                }
            ]
        }
        self.codebeamer_flask.responses = [
            Response(json.dumps(response_data), status=200),
        ]
        self._test_runner.declare_output_file(
            self._data_directory / cfg.out)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)

        # Verify the baselineId parameter was included in the request URL
        self.assertEqual(len(self.codebeamer_flask.received_requests), 1)
        request_url = self.codebeamer_flask.received_requests[0]["url"]
        self.assertIn("baselineId=407126303", request_url)


if __name__ == "__main__":
    unittest.main()
