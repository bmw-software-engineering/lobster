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

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List
import unittest

from tests_system.lobster_online_report.lobster_online_report_system_test_case_base \
    import LobsterOnlineReportSystemTestCaseBase

# Deliberately not a SHA, to show that the tool uses the configured value verbatim.
COMMIT_ID = "label-that-is-not-a-sha"

# Isolate the test repositories from the user's and the system's Git configuration.
_GIT_ENV = {
    **os.environ,
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}


def _git(cwd: Path, *args: str) -> str:
    """Runs the host's git in `cwd` and returns its stripped stdout.

    `args` are the Git subcommand and its arguments, e.g. "commit", "-q", "-m", "msg".
    Raises `CalledProcessError` if git exits with a non-zero code.
    """
    return subprocess.run(
        # -c protocol.file.allow=always: Git blocks local-path submodules by default
        #   (CVE-2022-39253), but "submodule add" from a local directory needs them.
        # -c commit.gpgsign=false: a user-level signing setting would otherwise make
        #   commits prompt for a key or fail in CI.
        ["git", "-c", "protocol.file.allow=always", "-c", "commit.gpgsign=false",
         *args],
        cwd=cwd,
        env=_GIT_ENV,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _init_repo(path: Path) -> None:
    path.mkdir(parents=True)
    _git(path, "init", "-q")


def _commit_file(repo: Path, name: str) -> str:
    (repo / name).write_text("content\n", encoding="utf-8")
    _git(repo, "add", name)
    _git(repo, "commit", "-q", "-m", f"add {name}")
    return _git(repo, "rev-parse", "HEAD")


def _report_with_files(files: List[str]) -> dict:
    items = [
        {
            "tag": f"python item_{index}",
            "location": {
                "kind": "file",
                "file": file,
                "line": 1,
                "column": None,
            },
            "name": f"item_{index}",
            "messages": [],
            "just_up": [],
            "just_down": [],
            "just_global": [],
            "tracing_status": "OK",
            "language": "Python",
            "kind": "Function",
        }
        for index, file in enumerate(files)
    ]
    return {
        "schema": "lobster-report",
        "version": 2,
        "generator": "lobster_report",
        "levels": [
            {
                "name": "code",
                "kind": "implementation",
                "items": items,
                "coverage": 100.0,
            }
        ],
        "policy": {
            "code": {
                "name": "code",
                "kind": "implementation",
                "traces": [],
                "source": [{"file": "basic.lobster"}],
                "needs_tracing_up": False,
                "needs_tracing_down": False,
                "breakdown_requirements": [],
            }
        },
        "matrix": [],
    }


class OnlineReportCommitValueTest(LobsterOnlineReportSystemTestCaseBase):
    """Tests using real Git repositories, which are created on the fly."""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._working_dir = self._test_runner.working_dir
        self._repo = self._working_dir / "repo"

    def _create_repo_with_submodule(self) -> str:
        """Creates repo/main.py and the submodule repo/sub containing lib.py.

        Returns the commit SHA of the submodule which is recorded by the repository.
        """
        submodule_origin = self._working_dir / "submodule_origin"
        _init_repo(submodule_origin)
        _commit_file(submodule_origin, "lib.py")

        _init_repo(self._repo)
        _commit_file(self._repo, "main.py")
        _git(self._repo, "submodule", "add", "-q", str(submodule_origin), "sub")
        _git(self._repo, "commit", "-q", "-m", "add submodule")
        return _git(self._repo, "rev-parse", "HEAD:sub")

    def _run_tool(self, files: List[str]) -> Dict[str, str]:
        """Runs the tool and returns the 'commit' of each item, keyed by its file."""
        (self._working_dir / "report.lobster").write_text(
            json.dumps(_report_with_files(files)), encoding="utf-8")
        (self._working_dir / "config.yaml").write_text(
            'base_url: "https://github.example.com/org/repo"\n'
            f'commit_id: "{COMMIT_ID}"\n'
            'repo_root: "repo"\n'
            'report: "report.lobster"\n',
            encoding="utf-8")
        self._test_runner.cmd_args.config = "config.yaml"
        self._test_runner.cmd_args.out = "out.lobster"

        result = self._test_runner.run_tool_test()

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(
            (self._working_dir / "out.lobster").read_text(encoding="utf-8"))
        return {
            item["location"]["file"]: item["location"]["commit"]
            for level in output["levels"]
            for item in level["items"]
        }

    def test_repository_without_submodules(self):
        # lobster-trace: core_online_report_req.Commit_Value_For_Item_Outside_Submodule
        _init_repo(self._repo)
        _commit_file(self._repo, "main.py")

        commits = self._run_tool(["repo/main.py"])

        self.assertEqual({"main.py": COMMIT_ID}, commits)

    def test_file_outside_submodule_of_repository_with_submodule(self):
        # lobster-trace: core_online_report_req.Commit_Value_For_Item_Outside_Submodule
        self._create_repo_with_submodule()

        commits = self._run_tool(["repo/main.py"])

        self.assertEqual({"main.py": COMMIT_ID}, commits)

    def test_file_inside_submodule(self):
        # lobster-trace: core_online_report_req.Commit_Value_For_Item_Inside_Submodule
        recorded_sha = self._create_repo_with_submodule()

        commits = self._run_tool(["repo/sub/lib.py"])

        self.assertEqual({"lib.py": recorded_sha}, commits)

    def test_file_inside_submodule_with_newer_checked_out_commit(self):
        # lobster-trace: core_online_report_req.Commit_Value_For_Item_Inside_Submodule
        recorded_sha = self._create_repo_with_submodule()
        checked_out_sha = _commit_file(self._repo / "sub", "newer.py")
        self.assertNotEqual(recorded_sha, checked_out_sha)

        commits = self._run_tool(["repo/sub/lib.py"])

        self.assertEqual({"lib.py": recorded_sha}, commits)


if __name__ == "__main__":
    unittest.main()
