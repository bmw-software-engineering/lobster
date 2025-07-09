from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import List, Optional, Union
from unittest import TestCase


class SystemTestCaseBase(TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.maxDiff = None  # pylint: disable=invalid-name
        self._temp_dirs: List[TemporaryDirectory] = []

    def create_temp_dir(
            self,
            prefix: str, dir_path: Optional[Union[str, Path]] = None,
    ) -> Path:
        # lobster-trace: system_test.Create_Temporary_Directory
        # pylint: disable=consider-using-with
        temp_dir = TemporaryDirectory(prefix=prefix, dir=dir_path)
        self._temp_dirs.append(temp_dir)
        return Path(temp_dir.name).resolve()

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
        # pylint: disable=consider-using-with
        output_dir = TemporaryDirectory(dir=output_dir)
        self._temp_dirs.append(output_dir)
        # Copy Expected output to temporary folder to compare with the output
        output_dir_path = Path(output_dir.name)
        shutil.copy(expected_file, output_dir_path)
        return output_dir_path

    def tearDown(self):
        # lobster-trace: system_test.Delete_Temporary_Directory
        for temp_dir in self._temp_dirs:
            temp_dir.cleanup()
        super().tearDown()
