import json
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, call, mock_open, patch

import responses

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.constants import (
    BAZEL_LOGS_NAME,
    JOB_OUTPUT_NAME,
    TEST_LOGS_NAME,
    ZUUL_MANIFEST_NAME,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads import (
    download_manifest,
    parse_manifest,
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

manifest_with_all_data = {
    "tree": [
        {"name": BAZEL_LOGS_NAME},
        {"name": JOB_OUTPUT_NAME},
        {"name": "adpbuild_123.yaml"},
        {"name": TEST_LOGS_NAME},
    ]
}
MANIFEST_WITH_ALL_DATA = json.dumps(manifest_with_all_data)

manifest_with_useless_data = {
    "tree": [
        {"name": "something_not_parsable"},
    ]
}
MANIFEST_WITH_USELESS_DATA = json.dumps(manifest_with_useless_data)

MANIFEST_EXCEPTION = """
{
    "exception"
}
"""


class TestDownloadManifest(TestCase):
    def setUp(self) -> None:
        self.server_address = f"https://bmwgroup.net/zuul-api/api/tenant/ddad/builds"
        self.build = create_test_zuulbuild("1234", "name", self.server_address)
        self.output_dir = Path("mocked_path")
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                zuul_auth_pair=("", ""), enable_caching=False, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={"1234": BuildPaths(manifest_path=Path("mocked_path/manifest.json"))}
            ),
        }
        self.server_address = f"https://bmwgroup.net/zuul-api/api/tenant/ddad/builds"
        self.server_url = self.server_address + "/" + ZUUL_MANIFEST_NAME

    def tearDown(self) -> None:
        pass

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    @patch("builtins.open")
    def test_parse_manifest_no_manifest_path(self, mock_open: MagicMock, mock_logging: MagicMock) -> None:
        """
        Verify that parse_manifest does not try to open a manifest if no manifest_path is specified,
        a warning message is logged, and the context stays unchanged
        """
        # Given manifest_path is None
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].manifest_path = None
        context_prior_parse_manifest = deepcopy(self.context)
        # When parse_manifest
        return_value = parse_manifest(self.build, self.context)
        # Then open is not called, and a warning is logged
        self.assertIsNone(return_value)
        self.assertEqual(mock_open.call_count, 0)
        mock_logging.warning.assert_called_with(f"Manifest json file 'None' not found")
        # And context stays unchanged
        self.assertEqual(self.context, context_prior_parse_manifest)

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    @patch.object(Path, "is_file", return_value=False)
    @patch("builtins.open")
    def test_parse_manifest_missing_manifest(
        self, mock_open: MagicMock, mock_path_is_file: MagicMock, mock_logging: MagicMock
    ) -> None:
        """
        Verify that parse_manifest does not try to open a manifest if no file is located at the specified manifest path,
        and the context stays unchanged
        """
        context_prior_parse_manifest = deepcopy(self.context)
        # When parse_manifest
        return_value = parse_manifest(self.build, self.context)
        # Then open is not called, and a warning is logged
        self.assertIsNone(return_value)
        self.assertEqual(mock_open.call_count, 0)
        mock_logging.warning.assert_called_with(f"Manifest json file 'mocked_path/manifest.json' not found")
        # And context stays unchanged
        self.assertEqual(self.context, context_prior_parse_manifest)

    @patch("builtins.open", mock_open(read_data=MANIFEST_EXCEPTION))
    @patch.object(Path, "is_file", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_parse_manifest_json_exception(self, mock_logging: MagicMock, mock_path_is_file: MagicMock) -> None:
        """
        Verify that when the manifest.json does not contain a valid JSON, a warning is logged in and the context stays unchanged
        """
        context_prior_parse_manifest = deepcopy(self.context)
        parse_manifest(self.build, self.context)
        # Warning is logged and the context stays unchanged
        mock_logging.warning.assert_called_once()
        self.assertEqual(self.context, context_prior_parse_manifest)

    @patch("builtins.open", mock_open(read_data=MANIFEST_WITH_USELESS_DATA))
    @patch.object(Path, "is_file", return_value=True)
    def test_parse_manifest_json_no_data(self, mock_path_is_file: MagicMock) -> None:
        """
        Verify that the ZuulBuild attributes are not set in the context if the data found
        by parse_manifest in the manifest.json is irrelevant
        """
        parse_manifest(self.build, self.context)
        self.assertFalse(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_archive)
        self.assertFalse(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_testlog)
        self.assertFalse(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_yaml)
        self.assertFalse(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_job_output)
        self.assertIsNone(
            self.context["data_collection_pipeline_status"].builds[self.build.uuid].yaml_name,
        )

    @patch("builtins.open", mock_open(read_data=MANIFEST_WITH_ALL_DATA))
    @patch.object(Path, "is_file", return_value=True)
    def test_parse_manifest_json_all_data(self, mock_path_is_file: MagicMock) -> None:
        """
        Verify that the corresponding attribute of the ZuulBuild is set in the context if found
        by parse_manifest in the manifest.json
        """
        parse_manifest(self.build, self.context)
        self.assertTrue(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_archive)
        self.assertTrue(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_testlog)
        self.assertTrue(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_yaml)
        self.assertTrue(self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_job_output)
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds[self.build.uuid].yaml_name,
            "adpbuild_123.yaml",
        )

    @responses.activate
    @patch.object(Path, "touch", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_download_manifest(self, mock_logging: MagicMock, mock_path_touch: MagicMock) -> None:
        # Given
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_url, REST_GET_SUCCESS, headers, body)
        http_server.start()
        # When download_manifest
        return_value = download_manifest(self.build, self.context)
        # Then the corresponding attribute of the ZuulBuild is set in the context
        self.assertIsNone(return_value)
        self.assertIsNotNone(self.context["data_collection_pipeline_status"].builds["1234"].manifest_path)
        self.assertEqual(
            str(self.context["data_collection_pipeline_status"].builds["1234"].manifest_path),
            str(self.output_dir.name + "/1234/" + ZUUL_MANIFEST_NAME),
        )
        self.assertIsNone(self.context["data_collection_pipeline_status"].builds["1234"].log_url)
        # And leaving marker is created
        mock_logging.debug.assert_called_with(f"Leaving marker 'mocked_path/1234/MANIFEST_DOWNLOADED'")
        self.assertEqual(mock_path_touch.call_count, 1)
        self.assertIsNone(download_manifest(self.build, self.context))


if __name__ == "__main__":
    unittest.main()
