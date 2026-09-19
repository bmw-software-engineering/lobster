import json
import unittest
from flask import Response
from tests_system.lobster_codebeamer.lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from tests_system.lobster_codebeamer.lobster_codebeamer_asserter import (
    LobsterCodebeamerAsserter)
from tests_system.lobster_codebeamer.mock_server_setup import get_mock_app


class LobsterCodebeamerTest(LobsterCodebeamerSystemTestCaseBase):
    """System test for Codebeamer with a mock HTTPS server
    returning predefined responses."""

    @classmethod
    def setUpClass(cls):
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self.codebeamer_flask.reset()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.verify_ssl = False

    def test_valid_query_id(self):
        # lobster-trace: codebeamer_req.Query_Id_Parameter
        # lobster-trace: codebeamer_req.Codebeamer_Reference_In_Output
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = 10203
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
        asserter = LobsterCodebeamerAsserter(
            self,
            completed_process,
            self._test_runner,
            port=self.codebeamer_flask.port,
        )
        asserter.assertStdOutNumAndFile(
            num_items=len(response_data['items']),
            page_size=1,
            port=self.codebeamer_flask.port,
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_references_tracing_tag_added(self):
        # lobster-trace: codebeamer_req.References_Field_Support
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = 424242
        cfg.out = "refs_tracing_tag.lobster"
        self._test_runner.declare_output_file(
            self._data_directory / self._test_runner.config_file_data.out)
        self._test_runner.config_file_data.refs = ["Wife", "Husband"]

        response_data = {
            'page': 1,
            'pageSize': 1,
            'total': 1,
            'items': [
                {
                    'item': {
                        'id': 42,
                        'name': 'Alpha',
                        'status': {
                            'id': 1,
                            'name': 'Married',
                            'type': 'ChoiceOptionReference'
                        },
                        'tracker': {
                            'id': 5,
                            'name': 'Beta',
                            'type': 'TrackerReference'
                        },
                        'version': 1,
                        'Wife': [
                            {"id": 1001, "name": "Delta"}
                        ],
                        'Husband': [
                            {"id": 1002, "name": "Charly"}
                        ],
                    }
                }
            ]
        }

        self.codebeamer_flask.responses = [
            Response(json.dumps(response_data), status=200),
        ]

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterCodebeamerAsserter(
            self,
            completed_process,
            self._test_runner,
            port=self.codebeamer_flask.port,
        )
        asserter.assertStdOutNumAndFile(
            num_items=len(response_data['items']),
            page_size=1,
            out_file=cfg.out,
            port=self.codebeamer_flask.port,
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_references_tracing_tag_from_custom_fields(self):
        # lobster-trace: codebeamer_req.References_Field_Support
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = 434343
        cfg.out = "refs_custom_fields.lobster"
        self._test_runner.declare_output_file(
            self._data_directory / self._test_runner.config_file_data.out)
        self._test_runner.config_file_data.refs = ["Wife", "Husband"]

        response_data = {
            'page': 1,
            'pageSize': 1,
            'total': 1,
            'items': [
                {
                    'item': {
                        'id': 55,
                        'name': 'Gamma',
                        'status': {
                            'id': 1,
                            'name': 'Ready',
                            'type': 'ChoiceOptionReference'
                        },
                        'tracker': {
                            'id': 9,
                            'name': 'Delta',
                            'type': 'TrackerReference'
                        },
                        'version': 3,
                        'customFields': [
                            {
                                'name': 'Wife',
                                'values': [{"id": 3001, "name": "Foo"}],
                            },
                            {
                                'name': 'Husband',
                                'values': [{"id": 3002, "name": "Bar"}],
                            },
                        ],
                    }
                }
            ]
        }

        self.codebeamer_flask.responses = [
            Response(json.dumps(response_data), status=200),
        ]

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterCodebeamerAsserter(
            self,
            completed_process,
            self._test_runner,
            port=self.codebeamer_flask.port,
        )
        asserter.assertStdOutNumAndFile(
            num_items=len(response_data['items']),
            page_size=1,
            out_file=cfg.out,
            port=self.codebeamer_flask.port,
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_numeric_import_query_string_treated_as_query_id(self):
        # lobster-trace: codebeamer_req.Numeric_Import_Query_String_Treated_As_Id
        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out(self.codebeamer_flask.port)
        cfg.import_query = "10203"
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

        self.assertEqual(len(self.codebeamer_flask.received_requests), 1)
        request_url = self.codebeamer_flask.received_requests[0]["url"]
        self.assertIn("/api/v3/reports/10203/items", request_url)

        asserter = LobsterCodebeamerAsserter(
            self,
            completed_process,
            self._test_runner,
            port=self.codebeamer_flask.port,
        )
        asserter.assertStdOutNumAndFile(
            num_items=len(response_data['items']),
            page_size=1,
            port=self.codebeamer_flask.port,
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
