import datetime
import json
import shutil
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, call, mock_open, patch

import pandas as pd

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.remove_artifacts import (
    remove_artifact,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_status import (
    DataCollectionPipelineStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.utils import (
    create_test_zuulbuild,
)


class TestRemoveArtifacts(TestCase):
    def setUp(self) -> None:
        self.build = create_test_zuulbuild("1234", "name", f"https://bmwgroup.net/zuul-api/api/tenant/ddad/builds")
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(output_directory=Path("/mocked_path")),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(),
        }

    def tearDown(self) -> None:
        pass

    @patch.object(Path, "is_file", return_value=True)
    @patch.object(Path, "unlink")
    def test_remove_artifact_file(
        self,
        mock_unlink: MagicMock,
        mock_path_is_file: MagicMock,
    ) -> None:
        remove_artifact(self.build, self.context, "bazel_logs.tar.gz")
        mock_unlink.assert_called_once()

    @patch.object(Path, "is_dir", return_value=True)
    @patch("shutil.rmtree")
    def test_remove_artifact_folder(self, mock_rmtree: MagicMock, mock_path_is_dir: MagicMock) -> None:
        remove_artifact(self.build, self.context, "testlogs")
        mock_rmtree.assert_called_once()

    @patch.object(Path, "unlink")
    @patch("shutil.rmtree")
    def test_remove_artifact_none(self, mock_rmtree: MagicMock, mock_unlink: MagicMock) -> None:
        remove_artifact(self.build, self.context, "whatever")
        self.assertEqual(mock_rmtree.call_count, 0)
        self.assertEqual(mock_unlink.call_count, 0)


if __name__ == "__main__":
    unittest.main()
