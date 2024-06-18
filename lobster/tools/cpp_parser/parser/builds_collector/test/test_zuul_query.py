import json
import unittest
from os.path import basename
from threading import Thread
from typing import Dict
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests
import responses

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query import (
    _parse_response,
    zuul_query,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_status import (
    DataCollectionPipelineStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildPaths,
    PipelineType,
    ZuulJobConfiguration,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.http_server_mock import (
    MockHttpServerWithoutCallback,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.zuul_response_mock import (
    RESPONSE,
    return_zuul_build,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.constants_utils import (
    REST_GATEWAY_TIMEOUT,
    REST_GET_ERROR,
    REST_GET_SUCCESS,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild


class TestQuery(TestCase):
    def setUp(self) -> None:
        self.json_content = RESPONSE
        self.first_build = ZuulBuild.parse_obj(self.json_content[0])
        self.second_build = ZuulBuild.parse_obj(self.json_content[1])
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                branch="master",
                number_of_last_builds=5,
                zuul_url=f"https://bmwgroup.net/zuul-api/api/tenant/ddad/builds",
                zuul_job=ZuulJobConfiguration("bazel-build-and-test-with-cache-upload", PipelineType.POST_INDEPENDENT),
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(),
        }
        self.server_address = f"https://bmwgroup.net/zuul-api/api/tenant/ddad/builds"

        self.mocked_response = MagicMock()
        self.mocked_response.json = MagicMock(return_value=self.json_content)
        self.mocked_response.status_code = REST_GET_SUCCESS
        self.mocked_response.headers = {"Content-Type": "application/json"}

    # Test parsed_response
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_parse_response(self, mock_logging: MagicMock) -> None:
        """
        Verify that zuul_query correctly parsed the answer for the Zuul server
        """
        self.mocked_response.json = MagicMock(return_value=self.json_content)
        parsed_response = _parse_response(self.mocked_response)
        self.assertEqual(parsed_response, [self.first_build, self.second_build])
        mock_logging.warning.assert_not_called()

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_parse_empty_response(self, mock_logging: MagicMock) -> None:
        """
        Verify that when a Zuul Server response is empty, _parse_response return an empty list of builds
        """
        self.mocked_response.json = MagicMock(return_value="")
        parsed_response = _parse_response(self.mocked_response)
        self.assertEqual(parsed_response, [])
        mock_logging.warning.assert_called_with(f"No valid Builds detected!")

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_parse_response(self, mock_logging: MagicMock) -> None:
        """
        Verify that when a Zuul Server response contains 2 well formed ZuulBuild,
        _parse_response return the list of 2 builds
        """
        self.mocked_response.json = MagicMock(return_value=self.json_content)
        parsed_response = _parse_response(self.mocked_response)
        self.assertEqual(parsed_response, [self.first_build, self.second_build])
        mock_logging.warning.assert_not_called()

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_parse_one_wrongly_formed_zuul_build(self, mock_logging: MagicMock) -> None:
        """
        Verify that when a ZuulBuild can not be parsed, a debug is logged
        """
        modified_content = RESPONSE[1].copy()
        modified_content.pop("end_time", None)  # remove end_time
        self.mocked_response.json = MagicMock(return_value=[RESPONSE[0], modified_content])
        parsed_response = _parse_response(self.mocked_response)
        # Verify that only the first Zuul Build is correctly parsed
        self.assertEqual(parsed_response, [self.first_build])
        # And that a debug is written in the logs for the second one
        self.assertEqual(mock_logging.debug.call_count, 3)

    # response_json contains 2 builds that can not completely be parsed and one that can be parsed, warning is logged
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_parse_majority_of_wrongly_formed_zuul_build(self, mock_logging: MagicMock) -> None:
        """
        Verify that when most of the ZuulBuild can not be parsed, a warning is logged
        """
        modified_content = RESPONSE[1].copy()
        modified_content.pop("end_time", None)  # remove end_time
        self.mocked_response.json = MagicMock(return_value=[RESPONSE[0], modified_content, modified_content])
        parsed_response = _parse_response(self.mocked_response)
        # Verify that only the first Zuul Build is correctly parsed
        self.assertEqual(parsed_response, [self.first_build])
        # And that a Warning is written in the logs for the second one which was "Impossible to parse"
        mock_logging.warning.assert_called_with(f"Most of the builds are invalid. You might want to investigate.")

    # Test zuul_query
    @responses.activate
    def test_status_code(self) -> None:
        """
        Verify that zuul_query raises a RetryError in case of a HTTP Timeout
        """
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GATEWAY_TIMEOUT)
        http_server.start()
        with self.assertRaises(requests.exceptions.RetryError):
            zuul_query(self.context)

    @responses.activate
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_error_code(self, mock_logging: MagicMock) -> None:
        """
        Verify that in case of error code a warning is logged
        """
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_ERROR)
        http_server.start()
        parsed_response = zuul_query(self.context)
        self.assertEqual(parsed_response, [])
        self.assertEqual(mock_logging.warning.call_count, 1)

    @responses.activate
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_header(self, mock_logging: MagicMock) -> None:
        """
        Verify that in case of wrong header type a warning is logged
        """
        headers = {"Content-Type": "text/html"}
        body = bytes("<html><head><title>Test</title></head><body>Test Body</body></html>", encoding="utf8")
        http_server = MockHttpServerWithoutCallback(
            responses.GET,
            self.server_address,
            REST_GET_SUCCESS,
            headers,
            body,
        )
        http_server.start()
        parsed_response = zuul_query(self.context)
        self.assertEqual(parsed_response, [])
        self.assertEqual(mock_logging.warning.call_count, 1)

    @responses.activate
    def test_query(self) -> None:
        """
        Verify that zuul_query correctly parsed the answer for the Zuul server
        """
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(RESPONSE), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_SUCCESS, headers, body)
        http_server.start()
        parsed_response = zuul_query(self.context)
        self.assertEqual(parsed_response, [self.first_build, self.second_build])

    @responses.activate
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.zuul_query.logging"
    )
    def test_parse_partial_response(self, mock_logging: MagicMock) -> None:
        """
        Verify that when a ZuulBuild can not be parsed, a warning is logged
        """
        updated_content = [RESPONSE[0]]
        modified_content = RESPONSE[1].copy()
        modified_content.pop("end_time", None)  # remove end_time
        updated_content = [RESPONSE[0], modified_content]
        headers = {"Content-Type": "application/json"}
        body = bytes(json.dumps(updated_content), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_SUCCESS, headers, body)
        http_server.start()
        parsed_response = zuul_query(self.context)
        # Verify that only the first Zuul Build is correctly parsed
        self.assertEqual(parsed_response, [self.first_build])
        # And that a Warning is written in the logs for the second one which was "Impossible to parse"
        self.assertEqual(mock_logging.warning.call_count, 1)

    @responses.activate
    def test_zuul_parsing_buildresult(self) -> None:
        """
        Verify that all BuildStatus of a Zuulbuild are correctly parsed
        """
        possible_builds_results = [
            "FAILURE",
            "POST_FAILURE",
            "RETRY",
            "RETRY_LIMIT",
            "SUCCESS",
            "TIMED_OUT",
            "ABORTED",
            "CANCELED",
            "RERUN",
            "SKIPPED",
        ]
        headers = {"Content-Type": "application/json"}
        body_all_builds_results = []
        for build_results in possible_builds_results:
            body_all_builds_results.append(
                return_zuul_build("31f1da8735dc41989bb34e56ab9caa62", build_results, "swh/ddad")
            )
        body = bytes(json.dumps(body_all_builds_results), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_SUCCESS, headers, body)
        http_server.start()
        parsed_response = zuul_query(self.context)
        self.assertEqual(len(parsed_response), len(possible_builds_results))

    @responses.activate
    def test_zuul_parsing_invalid_buildresult(self) -> None:
        """
        Verify that a Zuulbuild with an invalid BuildResult is filtered out
        """
        builds_results = ["FAILURE", "UNKNOWN_BUILD_RESULT", "POST_FAILURE"]  # Contains one invalid build_result
        headers = {"Content-Type": "application/json"}
        body_invalid_builds_results = []
        for build_results in builds_results:
            body_invalid_builds_results.append(
                return_zuul_build("31f1da8735dc41989bb34e56ab9caa62", build_results, "swh/ddad")
            )
        body = bytes(json.dumps(body_invalid_builds_results), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_SUCCESS, headers, body)
        http_server.start()
        parsed_response = zuul_query(self.context)
        self.assertEqual(len(parsed_response), len(builds_results) - 1)

    @responses.activate
    def test_zuul_parsing_projectname(self) -> None:
        """
        Verify that all ProjectName of a Zuulbuild are correctly parsed
        """
        possible_project_names = [
            "swh/adp",
            "swh/astas",
            "swh/boardnet",
            "swh/cvc",
            "swh/ddad",
            "swh/ddad_ci_config",
            "swh/ddad_platform",
            "swh/deployment",
            "swh/fkr",
            "swh/foresight",
            "swh/gnss_common",
            "swh/ib-vip",
            "swh/ltf_dlt",
            "swh/orion_aeb_temp",
            "swh/qdm",
            "swh/system_description",
            "swh/ufm",
            "swh/vdm",
            "swh/xpad-ara",
            "swh/xpad-shared",
            "swh/xpad-xpc",
            "swh/zuul-trusted-ddad",
        ]
        headers = {"Content-Type": "application/json"}
        body_all_project_names = []
        for project_name in possible_project_names:
            body_all_project_names.append(
                return_zuul_build("31f1da8735dc41989bb34e56ab9caa62", "FAILURE", project_name)
            )
        body = bytes(json.dumps(body_all_project_names), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_SUCCESS, headers, body)
        http_server.start()
        parsed_response = zuul_query(self.context)
        self.assertEqual(len(parsed_response), len(possible_project_names))

    @responses.activate
    def test_zuul_parsing_invalid_projectname(self) -> None:
        """
        Verify that a Zuulbuild with an invalid ProjectName is filtered out
        """
        project_names = [
            "swh/adp",
            "this_is_not_a_project",
        ]
        headers = {"Content-Type": "application/json"}
        body_invalid_project_name = []
        for project_name in project_names:
            body_invalid_project_name.append(
                return_zuul_build("31f1da8735dc41989bb34e56ab9caa62", "FAILURE", project_name)
            )
        body = bytes(json.dumps(body_invalid_project_name), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_SUCCESS, headers, body)
        http_server.start()
        parsed_response = zuul_query(self.context)
        self.assertEqual(len(parsed_response), len(project_names) - 1)

    @responses.activate
    def test_zuul_query_adding_build_path_to_pipeline_status_context(self) -> None:
        """
        Verify that a new BuildPaths is added to the data_collection_pipeline_status context if this ZuulBuild is not already part of the context
        """
        headers = {"Content-Type": "application/json"}

        body = [return_zuul_build("31f1da8735dc41989bb34e56ab9caa62", "FAILURE", "swh/ddad")]
        body = bytes(json.dumps(body), encoding="utf8")
        http_server = MockHttpServerWithoutCallback(responses.GET, self.server_address, REST_GET_SUCCESS, headers, body)
        http_server.start()
        parsed_response = zuul_query(self.context)
        # Verify that the correct amount of builds are returned
        self.assertEqual(len(parsed_response), 1)
        # Verify that a new BuildPath with default values is added to the data_collection_pipeline_status builds dictionnary
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["31f1da8735dc41989bb34e56ab9caa62"].json_path, None
        )
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds["31f1da8735dc41989bb34e56ab9caa62"].has_archive,
            False,
        )


if __name__ == "__main__":
    with responses.RequestsMock():
        unittest.main()
