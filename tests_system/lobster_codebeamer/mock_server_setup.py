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

import threading
import logging
from typing import Optional
from tests_system.lobster_codebeamer.mock_server import CodebeamerFlask, create_app

mock_server_thread: Optional[threading.Thread] = None
codebeamer_flask: Optional[CodebeamerFlask] = None


def _start_mock_server() -> CodebeamerFlask:
    global codebeamer_flask
    if codebeamer_flask:
        return codebeamer_flask

    codebeamer_flask = create_app(port=0)  # Use dynamic port allocation
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
