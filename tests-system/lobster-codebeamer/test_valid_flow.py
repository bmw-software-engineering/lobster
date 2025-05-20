import json
from flask import Response
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from ..asserter import Asserter
from .mock_server_setup import start_mock_server, get_mock_app


class LobsterCodebeamerTest(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer with a mock HTTPS server
    returning predefined responses."""

    @classmethod
    def setUpClass(cls):
        start_mock_server()
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.codebeamer_flask.responses = []

    def test_valid_query_id(self):
        # lobster-trace: codebeamer_req.Query_Id_Parameter
        self.set_config_file_data()
        self._test_runner.declare_output_file(
            self._data_directory / self._test_runner.config_file_data.out)

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
            Response(json.dumps(response_data), status=200),
        ]

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn("requirements to codebeamer.lobster", completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
