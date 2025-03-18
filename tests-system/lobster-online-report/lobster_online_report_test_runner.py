from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from ..test_runner import TestRunner


@dataclass
class CmdArgs:
    lobster_report: Optional[str] = None
    repo_root: Optional[str] = None
    out: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []

        def append_if_string(parameter: str, value: Optional[str]):
            if value is not None:
                cmd_args.append(f"{parameter}={value}")

        if self.lobster_report:
            cmd_args.append(self.lobster_report)

        append_if_string("--repo-root", self.repo_root)
        append_if_string("--out", self.out)
        return cmd_args


class LobsterOnlineReportTestRunner(TestRunner):
    """System test runner for lobster-online-report"""

    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments for 'lobster-online-report'"""
        return self._cmd_args.as_list()
