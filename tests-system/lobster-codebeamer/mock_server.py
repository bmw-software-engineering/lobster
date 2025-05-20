import json
from typing import List
from flask import Flask, Response
from threading import Lock
import logging

# Suppress Flask development server warning
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Config
CERT_PATH = 'tests-system/lobster-codebeamer/data/ssl/cert.pem'
KEY_PATH = 'tests-system/lobster-codebeamer/data/ssl/key.pem'
PORT = 8999
MOCK_ROUTE = '/api/v3/reports/<int:report_id>/items'


class CodebeamerFlask(Flask):
    def __init__(self):
        super().__init__(__name__)
        self._responses = []
        self._lock = Lock()
        self._counter = 0

    @property
    def counter(self):
        with self._lock:
            return self._counter

    @counter.setter
    def counter(self, value):
        with self._lock:
            self._counter = value

    @property
    def responses(self):
        with self._lock:
            return self._responses

    @responses.setter
    def responses(self, value: List):
        with self._lock:
            self._responses = value

    def start_server(self):
        self.run(
            host='0.0.0.0',
            port=PORT,
            ssl_context=(CERT_PATH, KEY_PATH),
            use_reloader=False
        )


def create_app():
    app = CodebeamerFlask()

    @app.route(MOCK_ROUTE, methods=['GET'])
    def mock_response(report_id):
        """Return mocked item response or error."""
        app.counter += 1
        return app.responses.pop(0)
    return app


if __name__ == '__main__':
    # NOTE: This is needed for manual testing, if a developer wants to run the server
    # locally
    app = create_app()
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
    app.responses = [
        Response(json.dumps(response_data), status=200),
    ]
    app.start_server()
