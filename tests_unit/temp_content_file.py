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
