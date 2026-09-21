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

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from tests_system.testrunner import TestRunner
from lobster.tools.pkg.pkg import main


@dataclass
class CmdArgs:
    files: List[str] = field(default_factory=list)
    out: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []
        # Add all files as separate arguments
        cmd_args.extend(self.files)
        if self.out:
            cmd_args.extend(["--out", self.out])
        return cmd_args


class LobsterPKGTestRunner(TestRunner):
    """System test runner for lobster-pkg"""

    def __init__(self, working_dir: Path):
        super().__init__(main, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments for 'lobster-pkg'"""
        return self._cmd_args.as_list()
