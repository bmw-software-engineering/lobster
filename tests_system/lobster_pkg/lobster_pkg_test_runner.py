from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from ..test_runner import TestRunner


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

    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments for 'lobster-pkg'"""
        return self._cmd_args.as_list()
