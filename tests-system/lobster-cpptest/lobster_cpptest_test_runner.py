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
    """System test runner for lobster-cpptest-report"""

    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments for 'lobster-cpptest'"""
        return self._cmd_args.as_list()

    def copy_directory(self, source_dir, destination_dir):
        """
        Copies the contents of the source directory to the destination directory.
        If the destination directory does not exist, it will be created.
        """
        source_path = Path(source_dir)
        if not source_path.exists():
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

        destination_path = Path(destination_dir)
        destination_path.mkdir(parents=True, exist_ok=True)

        # Copy the directory contents
        for item in source_path.iterdir():
            source_item = item
            destination_item = destination_path / item.name

            if source_item.is_dir():
                shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)

    def create_output_directory_and_copy_expected(self, output_dir: Path,
                                                  expected_file: Path):
        """
        Creates an output directory and copies the expected output file to it.
        The output directory is created in the working directory.
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Copy Expected output to temperory folder to compare with the output
        shutil.copy(expected_file, output_dir)
