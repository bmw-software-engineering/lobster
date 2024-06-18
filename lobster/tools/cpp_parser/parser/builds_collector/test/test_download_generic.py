import json
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests
import responses

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads import (
    _make_zuul_session,
    download_generic_zuul_content,
    get_url,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_status import (
    DataCollectionPipelineStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildPaths,
    CachePrefixType,
    ContentType,
    DownloadSpec,
)
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
    REST_GATEWAY_TIMEOUT,
    REST_GET_ERROR,
    REST_GET_NOT_FOUND,
    REST_GET_SUCCESS,
)


class TestDownloadGeneric(TestCase):
    def setUp(self) -> None:
        self.server_address = f"https://bmwgroup.net/zuul-api/api/tenant/ddad/builds"
        self.build = create_test_zuulbuild("1234", "name", self.server_address)

        self.test_dir = Path("/mocked_path")
        self.output_dir = Path(self.test_dir.name)
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                zuul_auth_pair=("", ""), enable_caching=False, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(builds={"1234": BuildPaths()}),
        }

        self.spec = DownloadSpec(
            file_name="log.json",
            content_type=ContentType.JSON,
            cache_prefix=CachePrefixType.TESTLOG,
        )
        self.server_url = self.server_address + "/" + self.spec.file_name

    def tearDown(self) -> None:
        pass

    # Test _make_zuul_session
    def test_make_zuul_session(self) -> None:
        session = _make_zuul_session()
        self.assertTrue(isinstance(session, requests.Session))

    def test_get_url(self) -> None:
        """
        Verify that get_url correctly builds up the url
        """
        extension = "logs.txt"
        base_urls = [
            "https://cc-ci.bmwgroup.net/logs/t/ddad/1234",
            "https://cc-ci.bmwgroup.net/logs/y/ddad/5678/",
        ]
        target = [
            "https://cc-ci.bmwgroup.net/logs/a/ddad/1234/logs.txt",
            "https://cc-ci.bmwgroup.net/logs/y/ddad/5678/logs.txt",
        ]
        self.assertEqual([get_url(url, extension) for url in base_urls], target)

    # Test download_generic_zuul_content
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_missing_url(self, mock_logging: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content keeps the context untouched for a ZuulBuild
        if the log_url is not set for this ZuulBuild and a debug message is logged
        """
        # Given a ZuulBuild with no log_url
        self.build.log_url = None
        context_prior_download = deepcopy(self.context)
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.debug.call_count, 1)
        self.assertEqual(self.context, context_prior_download)

    @patch.object(Path, "exists", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_cached_download_path_exists(self, mock_logging: MagicMock, mock_path_exists: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content does not download again if the data is
        already cached and a cached marker is stored
        """
        # Given a ZuulBuild with already cached data
        self.context["data_collection_pipeline_config"].enable_caching = True
        mocked_session = MagicMock()
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec, mocked_session)
        # Then the path to the file is set for the corresponding attribute of the ZuulBuild
        self.assertIsNone(return_value)
        self.assertEqual(mocked_session.get.call_count, 0)  # No new download of the data
        self.assertEqual(mock_logging.debug.call_count, 1)
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].log_path,
            self.output_dir / "1234/log.json",
        )

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_invalid_url(self, mock_logging: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content keeps the context untouched for a ZuulBuild
        if the log_url is not a valid url for this ZuulBuild and a warning message is logged
        """
        # Given a ZuulBuild with invalid log url
        self.build.log_url = "invalid/url"
        context_prior_download = deepcopy(self.context)
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.warning.call_count, 1)
        self.assertEqual(self.context, context_prior_download)

    @responses.activate
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_timeout(self, mock_logging: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content keeps the context untouched for a ZuulBuild
        if the download fails with time out
        """
        # Given
        context_prior_download = deepcopy(self.context)
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_url, REST_GATEWAY_TIMEOUT)
        http_server.start()
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.warning.call_count, 1)
        self.assertEqual(self.context, context_prior_download)

    @responses.activate
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_header(self, mock_logging: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content keeps the context untouched for a ZuulBuild
        if the download fails
        """
        # Given
        context_prior_download = deepcopy(self.context)
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_url, REST_GET_ERROR)
        http_server.start()
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.warning.call_count, 1)
        self.assertEqual(self.context, context_prior_download)

    @responses.activate
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_data_not_found(self, mock_logging: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content keeps the context untouched for a ZuulBuild
        if the data to download can not be found under the specified log_url for this ZuulBuild and a warning message is logged
        """
        # Given
        context_prior_download = deepcopy(self.context)
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_url, REST_GET_NOT_FOUND)
        http_server.start()
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.warning.call_count, 1)
        self.assertEqual(self.context, context_prior_download)

    @responses.activate
    @patch.object(Path, "touch", return_value=None)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_download_generic_log_path(self, mock_logging: MagicMock, mock_path_touch: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content set the correct attribute of
        the ZuulBuild in the context after DownloadSpec of a log_path JSON file
        """
        # Given
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_url, REST_GET_SUCCESS, headers, body)
        http_server.start()
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then the corresponding attribute of the ZuulBuild is set in the context
        self.assertIsNone(return_value)
        self.assertIsNotNone(self.context["data_collection_pipeline_status"].builds["1234"].log_path)
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].log_path,
            self.output_dir / "1234/log.json",
        )
        # And leaving marker is created
        mock_logging.debug.assert_called_with(f"Leaving marker 'mocked_path/1234/TESTLOG_DOWNLOADED'")
        self.assertEqual(mock_path_touch.call_count, 1)

    @responses.activate
    @patch.object(Path, "touch", return_value=None)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_download_generic_archive(self, mock_logging: MagicMock, mock_path_touch: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content set the correct attribute of
        the ZuulBuild in the context after DownloadSpec of a archive file
        """
        # Given
        self.spec = DownloadSpec(
            file_name="test_archive.tar.gz",
            content_type=ContentType.TAR,
            cache_prefix=CachePrefixType.ARCHIVE,
        )
        self.server_url = self.server_address + "/" + self.spec.file_name
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_url, REST_GET_SUCCESS, headers, body)
        http_server.start()
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then the corresponding attribute of the ZuulBuild is set in the context
        self.assertIsNone(return_value)
        self.assertIsNotNone(self.context["data_collection_pipeline_status"].builds["1234"].archive_path)
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].archive_path,
            self.output_dir / "1234/test_archive.tar.gz",
        )
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["1234"].log_url,
            self.server_address + "/test_archive.tar.gz",
        )
        # And leaving marker is created
        mock_logging.debug.assert_called_with(f"Leaving marker 'mocked_path/1234/ARCHIVE_DOWNLOADED'")
        self.assertEqual(mock_path_touch.call_count, 1)

    @responses.activate
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.downloads.logging"
    )
    def test_download_generic_no_log_path(self, mock_logging: MagicMock) -> None:
        """
        Verify that download_generic_zuul_content does not set the correct attribute of
        the ZuulBuild in the context after DownloadSpec of a JSON file not from cache prefix type
        log_path or archive_path
        """
        # Given
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_url, REST_GET_SUCCESS, headers, body)
        http_server.start()
        self.spec = DownloadSpec(
            file_name="manifest.json",
            content_type=ContentType.JSON,
            cache_prefix=CachePrefixType.MANIFEST,
        )
        # When download_generic_zuul_content
        return_value = download_generic_zuul_content(self.build, self.context, self.spec)
        # Then the corresponding attribute of the ZuulBuild is set in the context
        self.assertIsNone(return_value)
        self.assertIsNone(self.context["data_collection_pipeline_status"].builds["1234"].log_url)


if __name__ == "__main__":
    with responses.RequestsMock():
        unittest.main()
