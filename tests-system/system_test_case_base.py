from pathlib import Path
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
        return Path(temp_dir.name)

    def tearDown(self):
        # lobster-trace: system_test.Delete_Temporary_Directory
        for temp_dir in self._temp_dirs:
            temp_dir.cleanup()
        super().tearDown()
