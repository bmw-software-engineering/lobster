# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

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


if __name__ == "__main__":
    unittest.main()
