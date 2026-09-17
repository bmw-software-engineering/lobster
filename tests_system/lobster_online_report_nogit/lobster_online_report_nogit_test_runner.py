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
from pathlib import Path
from typing import List, Optional
from tests_system.testrunner import TestRunner
from tests_system.args_to_list import arguments_to_list
from lobster.tools.core.online_report_nogit.online_report_nogit import main


@dataclass
class CmdArgs:
    lobster_report: Optional[str] = None
    repo_root: Optional[str] = None
    remote_url: Optional[str] = None
    commit: Optional[str] = None
    out: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = arguments_to_list(
            key_value_args=(
                ("--repo-root", self.repo_root),
                ("--remote-url", self.remote_url),
                ("--commit", self.commit),
                ("--out", self.out),
            )
        )
        if self.lobster_report:
            cmd_args.append(self.lobster_report)
        return cmd_args


class LobsterOnlineReportNogitTestRunner(TestRunner):
    """System test runner for lobster-online-report-nogit"""

    def __init__(self, working_dir: Path):
        super().__init__(main, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        return self._cmd_args.as_list()
