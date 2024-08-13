import shutil
import tarfile
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.constants import (
    BAZEL_LOGS_NAME,
    TAR_LOGS_NAME,
    TEST_LOGS_NAME,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts import (
    _extract_archive,
    extract_build_archive,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_status import (
    DataCollectionPipelineStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import BuildPaths
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.utils import (
    create_test_zuulbuild,
)


class TestExtractBuildArchive(TestCase):
    def setUp(self) -> None:
        self.build = create_test_zuulbuild("1234", "name")
        self.output_dir = Path("/mocked_path")
        self.build_dir = self.output_dir / "1234"
        self.tar_file = self.build_dir / BAZEL_LOGS_NAME

        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                enable_caching=False, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={"1234": BuildPaths(archive_path=self.build_dir / BAZEL_LOGS_NAME)}
            ),
        }

    def tearDown(self) -> None:
        pass

    @patch.object(Path, "exists", return_value=True)
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts._extract_archive"
    )
    def test_extract_build_archived_cached(
        self, mock_extract_archive: MagicMock, mock_logging: MagicMock, mock_path_exists: MagicMock
    ) -> None:
        """
        Verify that extract_build_archive does not extract again if the data is
        already cached and a cached marker is stored
        """
        # Given a ZuulBuild with already cached data
        self.context["data_collection_pipeline_config"].enable_caching = True
        # When extract_build_archive
        return_value = extract_build_archive(self.build, self.context)
        # Then the archive is not extracted again and a debug message is logged
        self.assertEqual(mock_extract_archive.call_count, 0)
        self.assertIsNone(return_value)
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].log_path,
            self.output_dir / "1234" / TEST_LOGS_NAME,
        )
        self.assertEqual(mock_logging.debug.call_count, 1)

    @patch.object(Path, "exists", return_value=False)
    @patch.object(Path, "is_file", return_value=False)
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts._extract_archive"
    )
    def test_extract_build_archived_no_file(
        self,
        mock_extract_archive: MagicMock,
        mock_logging: MagicMock,
        mock_path_is_file: MagicMock,
        mock_path_exists: MagicMock,
    ) -> None:
        """
        Verify that extract_build_archive does not extract archive if the archive file is not
        located at the expected path
        """
        # Given a ZuulBuild with an non-existing path
        self.context["data_collection_pipeline_config"].enable_caching = True
        self.context["data_collection_pipeline_status"].builds["1234"].archive_path = (
            self.build_dir / "no_bazel_logs.tar.gz"
        )  # Not really required since is_file is mocked, but added for readability
        # When extract_build_archive
        return_value = extract_build_archive(self.build, self.context)
        # Then the archive is not extracted and a warning message is logged
        self.assertIsNone(return_value)
        self.assertEqual(mock_extract_archive.call_count, 0)
        self.assertEqual(mock_logging.warning.call_count, 1)

    @patch.object(Path, "exists", return_value=False)
    @patch.object(Path, "is_file", side_effect=[True, False])
    @patch.object(Path, "touch", return_value=None)
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts._extract_archive"
    )
    def test_extract_build_archive_missing_archive(
        self,
        mock_extract_archive: MagicMock,
        mock_logging: MagicMock,
        mock_path_touch: MagicMock,
        mock_path_is_file: MagicMock,
        mock_path_exists: MagicMock,
    ) -> None:
        """
        Verify that no marker is added if the extraction of the archive failed, i.e. no file is located at the specified extraction path
        """
        # Given
        # When extract_build_archive
        return_value = extract_build_archive(self.build, self.context)
        # Then _extract_archive is called but no marker is added
        self.assertIsNone(return_value)
        self.assertEqual(mock_extract_archive.call_count, 1)
        mock_extract_archive.assert_called_with(
            self.context["data_collection_pipeline_status"].builds["1234"].archive_path,
            self.context["data_collection_pipeline_config"].output_directory / "1234",
        )
        self.assertEqual(mock_path_touch.call_count, 0)

    @patch.object(shutil, "copyfile", return_value=None)
    @patch.object(tarfile, "open")
    @patch.object(Path, "exists", return_value=False)
    @patch.object(Path, "is_file", return_value=True)
    @patch.object(Path, "touch", return_value=None)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts._extract_archive"
    )
    def test_extract_build_archive(
        self,
        mock_extract_archive: MagicMock,
        mock_path_touch: MagicMock,
        mock_path_is_file: MagicMock,
        mock_path_exists: MagicMock,
        mock_tar_open: MagicMock,
        mock_shutil_copyfile: MagicMock,
    ) -> None:
        """
        Verify that a marker is added if the extraction of the archive is a success
        """
        # Given
        # When extract_build_archive
        return_value = extract_build_archive(self.build, self.context)
        # Then _extract_archive is called and a marker is added
        self.assertIsNone(return_value)
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].log_path,
            self.output_dir / "1234" / TEST_LOGS_NAME,
        )
        self.assertEqual(mock_extract_archive.call_count, 1)
        mock_extract_archive.assert_called_with(
            self.context["data_collection_pipeline_status"].builds["1234"].archive_path,
            self.context["data_collection_pipeline_config"].output_directory / "1234",
        )
        mock_shutil_copyfile.assert_called_once_with(self.build_dir / TAR_LOGS_NAME, self.build_dir / TEST_LOGS_NAME)
        self.assertEqual(mock_path_touch.call_count, 1)

    # TEST_EXTRACT_ARCHIVE ALONE
    @patch.object(tarfile, "open")
    def test_extract_archive(self, mock_tar_open: MagicMock) -> None:
        """
        Verify that _extract_archive extract the archive specified to the specified destination
        """
        # Given
        archive_path = Path("/archive_for_test")
        destination_path = Path("/destination_for_test")
        empty_tarfile = MagicMock()
        mock_tar_open.return_value = empty_tarfile

        # When _extract_archive
        return_value = _extract_archive(archive_path, destination_path)

        # Then the archive in archive_path is opened and extracted to destination_path
        self.assertEqual(mock_tar_open.call_count, 1)
        mock_tar_open.assert_called_with(archive_path)
        self.assertEqual(empty_tarfile.__enter__().extractall.call_count, 1)
        empty_tarfile.__enter__().extractall.assert_called_with(path=destination_path)


if __name__ == "__main__":
    unittest.main()
