import os.path
from pathlib import Path
from re import Pattern
from typing import Iterable, List

from lobster.common.errors import PathError


class FileCollector:
    def __init__(
            self,
            extensions: Iterable[str],
            directory_exclude_patterns: Iterable[Pattern],
    ) -> None:
        if extensions is None:
            raise ValueError("'extensions' must not be None")
        if directory_exclude_patterns is None:
            directory_exclude_patterns = []
        self._extensions = extensions
        self._files = []
        self._directory_exclude_patterns = directory_exclude_patterns
        for ext in self._extensions:
            if not ext.startswith("."):
                raise ValueError(f"Extension '{ext}' must start with a dot (.)")

    @property
    def files(self) -> List[str]:
        return self._files

    def add_file(self, file: str, throw_on_mismatch: bool) -> None:
        if self._is_file_of_interest(file):
            self._files.append(file)
        elif throw_on_mismatch:
            raise PathError(
                f"File {file} does not have a valid extension. "
                f"Expected one of {', '.join(self._extensions)}."
            )

    def _is_file_of_interest(self, file: str) -> bool:
        return (not self._extensions) or \
            (os.path.splitext(file)[1].lower() in self._extensions)

    def _is_dir_of_interest(self, dir_name: str) -> bool:
        return not any(pattern.match(dir_name)
                       for pattern in self._directory_exclude_patterns)

    def add_dir_recursively(self, dir_path: str) -> None:
        """Recursively adds files from a directory, filtering by extensions."""
        def walk_directory(path: Path):
            for item in Path(path).iterdir():
                if item.is_file():
                    self.add_file(str(item.as_posix()), throw_on_mismatch=False)
                elif item.is_dir():
                    if self._is_dir_of_interest(item.name):
                        walk_directory(item)

        walk_directory(Path(dir_path))
