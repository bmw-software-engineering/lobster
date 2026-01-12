from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from tests_system.testrunner import TestRunner
from lobster.tools.python.python import main



@dataclass
class CmdArgs:
    files: List[str] = field(default_factory=list)
    out: Optional[str] = None
    kind: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []

        # Add all files as separate arguments
        cmd_args.extend(self.files)
        if self.out:
            cmd_args.extend(["--out", self.out])
        if self.kind:
            cmd_args.extend(["--kind", self.kind])
        return cmd_args


class LobsterPythonTestRunner(TestRunner):
    """System test runner for lobster-python"""

    def __init__(self, working_dir: Path):
        super().__init__(main, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments for 'lobster-python'"""
        return self._cmd_args.as_list()
