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
