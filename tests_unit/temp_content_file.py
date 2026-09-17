# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import os
from tempfile import NamedTemporaryFile


class TempContentFile:
    """Context manager for creating a temporary file with a specific content.

       This class creates a temporary file with the given content, and deletes it
       when the context is exited.

       This is a wrapper around tempfile.NamedTemporaryFile which works for all
       Python versions.

       With Python 3.12+ we could simply set the parameters delete_on_close=False and
       delete=True, but we want to support Python 3.8+
    """

    def __init__(self, content: str):
        self._content = content
        self._file = None

    def __enter__(self):
        self._file = NamedTemporaryFile(
            mode="w",
            encoding="UTF-8",
            delete=False,
        )
        self._file.write(self._content)
        self._file.flush()
        self._file.close()
        return self._file.name

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            os.remove(self._file.name)
