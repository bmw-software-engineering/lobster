import threading
from .mock_server import CodebeamerFlask, create_app

mock_server_thread = None
codebeamer_flask = None


def start_mock_server():
    global mock_server_thread, codebeamer_flask
    if mock_server_thread is not None:
        return

    codebeamer_flask = create_app()
    mock_server_thread = threading.Thread(
        target=codebeamer_flask.start_server,
        daemon=True
    )
    mock_server_thread.start()


def get_mock_app() -> CodebeamerFlask:
    if not codebeamer_flask:
        raise RuntimeError("Mock server not started! Call start_mock_server() first!")
    return codebeamer_flask
