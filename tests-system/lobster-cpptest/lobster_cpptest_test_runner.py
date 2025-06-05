from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import List, Optional
from ..test_runner import TestRunner


@dataclass
class CmdArgs:
    config: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []

        def append_if_string(parameter: str, value: Optional[str]):
            if value is not None:
                cmd_args.append(f"{parameter}={value}")

        append_if_string("--config", self.config)
        return cmd_args


class LobsterCpptestTestRunner(TestRunner):
    """System test runner for lobster-cpptest"""

    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments for 'lobster-cpptest'"""
        return self._cmd_args.as_list()

    def create_output_directory_and_copy_expected(self, output_dir: Path,
                                                  expected_file: Path):
        """
        Creates an output directory and copies the expected output file to it.
        The output directory is created in the working directory.
        Args:
            output_dir (Path): The directory where the expected output file will be
                               stored.
            expected_file (Path): The path of the expected file to be copied
                                  in output_dir.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        # Copy Expected output to temporary folder to compare with the output
        shutil.copy(expected_file, output_dir)
