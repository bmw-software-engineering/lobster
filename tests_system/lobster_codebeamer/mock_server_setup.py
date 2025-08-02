import threading
import logging
from typing import Optional
from .mock_server import CodebeamerFlask, create_app

mock_server_thread: Optional[threading.Thread] = None
codebeamer_flask: Optional[CodebeamerFlask] = None


def _start_mock_server() -> CodebeamerFlask:
    global codebeamer_flask
    if codebeamer_flask:
        return codebeamer_flask

    codebeamer_flask = create_app()
    mock_server_thread = threading.Thread(
        target=codebeamer_flask.start_server,
        daemon=True
    )
    mock_server_thread.start()
    codebeamer_flask.await_startup_finished(logging.getLogger("Flask-Startup"))
    return codebeamer_flask


def get_mock_app() -> CodebeamerFlask:
    # lobster-trace: system_test.Use_Await_Startup_Finished
    global codebeamer_flask
    if not codebeamer_flask:
        codebeamer_flask = _start_mock_server()
    return codebeamer_flask
