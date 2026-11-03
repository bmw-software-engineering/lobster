# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from lobster.tools.core.online_report.path_to_url_converter import (
    NotInsideRepositoryException,
    PathToUrlConverter,
    UrlParts,
)


class PathToUrlConverterTest(unittest.TestCase):
    """Checks main-repository fallback and its repository boundary."""

    def setUp(self):
        self.repo_root = Path("repo").resolve()
        self.repo = Mock(working_tree_dir=str(self.repo_root), submodules=[])
        repo_patch = patch(
            "lobster.tools.core.online_report.path_to_url_converter.Repo",
            return_value=self.repo,
        )
        repo_patch.start()
        self.addCleanup(repo_patch.stop)
        self.converter = PathToUrlConverter(
            str(self.repo_root), "https://github.example.com/org/repo/"
        )
        self.addCleanup(self.converter.close)

    def test_main_repository_paths_without_errors(self):
        """Valid main-repository paths need no submodule error diagnostic."""
        # lobster-trace: core_online_report_req.Main_Repo_Path_Without_Error
        # GIVEN root and nested files, with and without an unrelated submodule.
        for has_submodule in (False, True):
            self.repo.submodules = (
                [Mock(path="sub", url="../library", hexsha="submodule-sha")]
                if has_submodule else []
            )
            for filename, encoded_path in (
                ("main.py", "main.py"),
                ("nested/file name.py", "nested/file%20name.py"),
            ):
                with self.subTest(submodule=has_submodule, filename=filename):
                    # WHEN converting a path outside every submodule.
                    with self.assertNoLogs("PathToUrlConverter", level="ERROR"):
                        result = self.converter.path_to_url(
                            self.repo_root / filename, "configured-commit"
                        )

                    # THEN the main-repository URL and commit are preserved.
                    self.assertEqual(
                        UrlParts(
                            "https://github.example.com/org/repo",
                            "configured-commit",
                            encoded_path,
                        ),
                        result,
                    )

    def test_path_outside_repository_is_rejected(self):
        """Removing a false diagnostic must not accept out-of-repository paths."""
        # lobster-exclude: Compatibility control for the existing repository boundary.
        # GIVEN a path in a similarly named sibling directory.
        outside_path = self.repo_root.with_name("repo-other") / "main.py"

        # WHEN converting the path, THEN the repository boundary still rejects it.
        with self.assertRaisesRegex(
            NotInsideRepositoryException, "is not inside the repository"
        ):
            self.converter.path_to_url(outside_path, "configured-commit")


if __name__ == "__main__":
    unittest.main()
