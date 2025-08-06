import json
from time import sleep
from typing import List
from flask import Flask, Response, request
from threading import Lock
import logging

import requests

# Suppress Flask development server warning
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Config
CERT_PATH = 'tests_system/lobster_codebeamer/data/ssl/cert.pem'
KEY_PATH = 'tests_system/lobster_codebeamer/data/ssl/key.pem'
PORT = 8999
MOCK_ROUTE = '/api/v3/reports/<int:report_id>/items'
ARE_YOU_RUNNING_ROUTE = '/are-you-running'


class CodebeamerFlask(Flask):
    STARTUP_ANSWER = "Yes, I am running!"

    _HOST = "127.0.0.1"
    _STARTUP_TEST_URL = f"https://{_HOST}:{PORT}{ARE_YOU_RUNNING_ROUTE}"

    def __init__(self):
        super().__init__(__name__)
        self._lock = Lock()
        self._responses = []
        self._received_requests = []

    def reset(self):
        """Reset the server state."""
        # lobster-trace: system_test.Codebeamer_Flask_Responses_Reset
        with self._lock:
            self._responses = []
            self._received_requests = []

    @property
    def received_requests(self):
        with self._lock:
            return self._received_requests

    @received_requests.setter
    def received_requests(self, value: List):
        with self._lock:
            self._received_requests = value

    @property
    def responses(self):
        with self._lock:
            return self._responses

    @responses.setter
    def responses(self, value: List):
        # lobster-trace: system_test.Codebeamer_Flask_Responses_Setter
        with self._lock:
            self._responses = value

    def start_server(self):
        self.run(
            host=self._HOST,
            port=PORT,
            ssl_context=(CERT_PATH, KEY_PATH),
            use_reloader=False
        )

    def await_startup_finished(self, logger: logging.Logger):
        """Wait for the Flask server to start by sending a request."""
        # lobster-trace: system_test.Codebeamer_Mock_Server_Await_Startup
        self._await_startup_finished(
            url=self._STARTUP_TEST_URL,
            num_attempts=10,
            retry_sleep=0.5,
            http_timeout=4.0,
            expected_response=self.STARTUP_ANSWER,
            logger=logger,
        )

    @staticmethod
    def _await_startup_finished(
        url: str,
        num_attempts: int,
        retry_sleep: float,
        http_timeout: float,
        expected_response: str,
        logger: logging.Logger,
    ):
        """Wait for the Flask server to start by retrying requests until success, or
           until timeout.

           This function is blocking and threadsafe.
        """
        attempts = 0
        while attempts < num_attempts:
            attempts += 1
            logger.debug(f"Sending test request {attempts}/{num_attempts} to the mock "
                         f"server to verify it is running.")
            try:
                response = requests.get(
                    url=url,
                    timeout=http_timeout,
                    verify=False,
                )
                if (response.status_code == 200) and \
                        (response.text == expected_response):
                    logger.debug(f"Mock server is ready. "
                                 f"Response was '{response.text}'")
                    return
                raise NotImplementedError(
                    f"Unexpected response from mock server: "
                    f"{response.status_code} - {response.text}"
                )
            except requests.exceptions.Timeout as e:
                raise TimeoutError(
                    f"Codebeamer mock server did start after {attempts} attempt(s), "
                    f"but did not respond after {http_timeout} seconds!",
                ) from e
            except requests.exceptions.RequestException as e:
                logger.debug("Mock server not ready yet, retrying...")
                sleep(retry_sleep)

        raise requests.exceptions.RequestException(
            f"Codebeamer mock server did not start after {num_attempts} attempts, "
            f"giving up!"
        )


def create_app():
    app = CodebeamerFlask()

    @app.route(MOCK_ROUTE, methods=['GET'])
    def mock_response(report_id):
        """Return mocked item response or error."""
        app.received_requests.append({
            "url": request.url,
            "method": request.method,
            "args": request.args.to_dict(flat=False),
            "headers": dict(request.headers),
            "data": request.get_data(as_text=True),
            "json": request.get_json(silent=True),
        })
        return app.responses.pop(0)

    @app.route(ARE_YOU_RUNNING_ROUTE, methods=['GET'])
    def i_am_running():
        """Reply that the mock server is running."""
        return app.STARTUP_ANSWER

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
