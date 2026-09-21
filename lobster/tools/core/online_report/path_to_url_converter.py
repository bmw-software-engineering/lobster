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

from dataclasses import dataclass
import logging
import os
from pathlib import Path
from typing import Tuple
from urllib.parse import quote
from git import Repo, Submodule


@dataclass
class UrlParts:
    url_start: str
    commit_hash: str
    path_html: str


class NotInsideRepositoryException(Exception):
    """Exception raised when a path is not inside a Git repository."""


class PathToUrlConverter:

    def __init__(self, repo_path, url_base: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._repo = Repo(repo_path)
        self._url_base = url_base
        for submodule in self._repo.submodules:
            self._logger.info("Name: %s, Path: %s, URL: %s",
                              submodule.name, submodule.path, submodule.url)

    @staticmethod
    def _path_to_html_format(path: Path) -> str:
        """Convert a file path to a URL format suitable for HTML links."""
        return quote(path.as_posix())

    def _get_submodule_full_url(self, submodule_url: str) -> str:
        """Get the full URL for a submodule."""
        return f"{self._url_base.rstrip('/')}/{submodule_url.lstrip('/')}"

    def path_to_url(self, path: Path, commit_id: str) -> UrlParts:
        """Convert a path to a URL based on the submodule configuration.

           The path must be nested inside a submodule of the repository.
        """
        path = path.resolve()
        try:
            submodule, relative_path = self._get_submodule_and_relative_path(path)
            url_start = self._get_submodule_full_url(submodule.url)
            commit_hash = submodule.hexsha
        except KeyError as e:
            self._logger.error("Path '%s' is not inside a submodule: %s", path, e)
            # Path is not inside a submodule — use main repo
            commit_hash = commit_id
            try:
                relative_path = path.resolve().relative_to(self._repo.working_tree_dir)
            except ValueError as value_error:
                raise NotInsideRepositoryException(
                    f"Path '{path}' is not inside the repository '"
                    f"{self._repo.working_tree_dir}'!",
                ) from value_error

            url_start = self._url_base.rstrip("/")

        path_html = self._path_to_html_format(relative_path)
        return UrlParts(url_start=url_start, commit_hash=commit_hash,
                        path_html=path_html)

    def _get_submodule_and_relative_path(self, path: Path) -> Tuple[Submodule, Path]:
        """Get the submodule and the relative path (relative to the submodule folder,
         not to repo root) for a given path.

        Example:
           path = "/home/<user>/git/swh/repo/domains/driving/folder1/folder2/file.cpp"
           submodule.path = "domains/driving"

           return Submodule instance of "domains/driving", Path of "folder1/folder2/
           file.cpp"
        """
        path = path.resolve()
        for submodule in self._repo.submodules:
            submodule_path = (Path(str(self._repo.working_tree_dir)) /
                              str(submodule.path).replace("/", os.sep))
            try:
                rel_path = path.relative_to(submodule_path)
                return submodule, rel_path
            except ValueError:
                continue

        raise KeyError(f"No submodule found for path: {path}")
