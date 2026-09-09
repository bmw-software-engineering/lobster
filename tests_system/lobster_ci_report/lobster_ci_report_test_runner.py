from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from tests_system.testrunner import TestRunner
from lobster.tools.core.ci_report.ci_report import main


@dataclass
class CmdArgs:
    lobster_report: Optional[str] = None
    show_coverage: bool = False

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []
        if self.lobster_report is not None:
            cmd_args.append(self.lobster_report)
        if self.show_coverage:
            cmd_args.append("--show-coverage")
        return cmd_args


class LobsterCiReportTestRunner(TestRunner):
    """System test runner for lobster-ci-report"""

    def __init__(self, working_dir: Path):
        super().__init__(main, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to start
        'lobster-ci-report' under test"""
        return self._cmd_args.as_list()
