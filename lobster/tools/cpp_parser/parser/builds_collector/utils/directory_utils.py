import shutil
from pathlib import Path

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import ContextType


def ensure_directory(directory: Path) -> None:
    """Creates the directory and its parents if it not alread exists.

    Parameters
    ----------
    directory: pathlib.Path
        The directory to create.
    """
    if not directory.is_dir():
        directory.mkdir(parents=True)


class TestDirectory:
    def __init__(self) -> None:
        self.directory = Path(Path.cwd() / "builds_collector_test_directory")
        self.directory.mkdir(exist_ok=True)

    def __del__(self) -> None:
        self.clear_directory()

    def get_directory(self) -> Path:
        """Returns the actual testing directory
        Returns
        ----------
        The testing directory Path object
        """
        return self.directory

    def clear_directory(self) -> None:
        """Deletes everything under the actual test directory.
        Returns
        ----------
        None
        """
        if self.directory.exists():
            shutil.rmtree(self.directory)
