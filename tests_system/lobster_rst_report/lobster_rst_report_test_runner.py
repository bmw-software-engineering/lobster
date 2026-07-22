from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from tests_system.testrunner import TestRunner
from lobster.tools.core.rst_report.rst_report import main


@dataclass
class CmdArgs:
    lobster_report: Optional[str] = None
    out: Optional[str] = None
    out_dir: Optional[str] = None
    source_root: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list."""
        cmd_args = []
        if self.lobster_report is not None:
            cmd_args.append(self.lobster_report)
        if self.out is not None:
            cmd_args.extend(["--out", self.out])
        if self.out_dir is not None:
            cmd_args.extend(["--out-dir", self.out_dir])
        if self.source_root is not None:
            cmd_args.extend(["--source-root", self.source_root])
        return cmd_args


class LobsterRstReportTestRunner(TestRunner):
    """System test runner for lobster-rst-report"""

    def __init__(self, working_dir: Path):
        super().__init__(main, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to start
        'lobster-rst-report' under test."""
        return self._cmd_args.as_list()
