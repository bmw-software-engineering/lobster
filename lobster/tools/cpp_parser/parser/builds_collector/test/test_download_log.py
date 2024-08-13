import json
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

import responses
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.constants import (
    BAZEL_LOGS_NAME,
    TEST_LOGS_NAME,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads import (
    download_log,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_status import (
    DataCollectionPipelineStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import BuildPaths
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.http_server_mock import (
    MockHttpServerWithoutCallback,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.utils import (
    create_test_zuulbuild,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.zuul_response_mock import (
    RESPONSE,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.constants_utils import (
    REST_GET_SUCCESS,
)


class TestDownloadLog(TestCase):
    def setUp(self) -> None:
        self.server_address = f"https://bmwgroup.net/zuul-api/api/tenant/ddad/builds"
        self.build = create_test_zuulbuild("1234", "name", self.server_address)
        self.test_dir = Path("/mocked_path")
        self.output_dir = Path(self.test_dir.name)

    def tearDown(self) -> None:
        pass

    @responses.activate
    @patch.object(Path, "touch", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_download_bazel_logs(self, mock_logging: MagicMock, mock_path_touch: MagicMock) -> None:
        # Given a Build with has_archive set
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                zuul_auth_pair=("", ""), enable_caching=False, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "1234": BuildPaths(has_archive=True),
                }
            ),
        }
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(
            responses.GET, self.server_address + "/" + BAZEL_LOGS_NAME, REST_GET_SUCCESS, headers, body
        )
        http_server.start()
        # When download_log
        return_value = download_log(self.build, self.context)
        # Then the corresponding attribute of the ZuulBuild is set in the context
        self.assertIsNone(return_value)
        self.assertIsNotNone(self.context["data_collection_pipeline_status"].builds["1234"].archive_path)
        self.assertEqual(
            str(self.context["data_collection_pipeline_status"].builds["1234"].archive_path),
            str(self.output_dir.name + "/1234/" + BAZEL_LOGS_NAME),
        )
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].log_url,
            self.server_address + "/" + BAZEL_LOGS_NAME,
        )
        # And leaving marker is created
        mock_logging.debug.assert_called_with(f"Leaving marker 'mocked_path/1234/ARCHIVE_DOWNLOADED'")
        self.assertEqual(mock_path_touch.call_count, 1)

    @responses.activate
    @patch.object(Path, "touch", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_download_test_logs(self, mock_logging: MagicMock, mock_path_touch: MagicMock) -> None:
        # Given a Build with has_testlog set
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                zuul_auth_pair=("", ""), enable_caching=False, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "1234": BuildPaths(has_testlog=True),
                }
            ),
        }
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(
            responses.GET, self.server_address + "/" + TEST_LOGS_NAME, REST_GET_SUCCESS, headers, body
        )
        http_server.start()
        # When download_log
        return_value = download_log(self.build, self.context)
        # Then the corresponding attribute of the ZuulBuild is set in the context
        self.assertIsNone(return_value)
        self.assertIsNotNone(self.context["data_collection_pipeline_status"].builds["1234"].log_path)
        self.assertEqual(
            str(self.context["data_collection_pipeline_status"].builds["1234"].log_path),
            str(self.output_dir.name + "/1234/" + TEST_LOGS_NAME),
        )
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].log_url,
            self.server_address + "/" + TEST_LOGS_NAME,
        )
        # And leaving marker is created
        mock_logging.debug.assert_called_with(f"Leaving marker 'mocked_path/1234/TESTLOG_DOWNLOADED'")
        self.assertEqual(mock_path_touch.call_count, 1)

    @responses.activate
    @patch.object(Path, "touch", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.download_generic_zuul_content"
    )
    def test_download_invalid_logs(
        self, mock_download: MagicMock, mock_logging: MagicMock, mock_path_touch: MagicMock
    ) -> None:
        # Given a Build with has_archive None and has_testlog None
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                zuul_auth_pair=("", ""), enable_caching=False, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "1234": BuildPaths(),
                }
            ),
        }
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(
            responses.GET, self.server_address + "/" + TEST_LOGS_NAME, REST_GET_SUCCESS, headers, body
        )
        http_server.start()
        # When download_log
        return_value = download_log(self.build, self.context)
        # Then no download takes place and a warning is displayed
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.warning.call_count, 1)
        self.assertEqual(mock_download.call_count, 0)


if __name__ == "__main__":
    unittest.main()
