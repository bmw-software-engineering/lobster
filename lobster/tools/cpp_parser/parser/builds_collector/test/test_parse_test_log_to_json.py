import unittest
from copy import deepcopy
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json import (
    _parse_log,
    _tail_log,
    parse_test_log_to_json,
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

TEST_LOG_ONLY_TEST_RESULTS = """
//tests/test2 PASSED in 2.4s 
//tests/test3 FAILED in 3.2s 
Duration min= 0.0s avg = 0.8s max= 1.6s
Lorem ipsum dolor sit amet
"""

TEST_LOG_CACHED_TEST_RESULTS = """
//tests/test1 (cached) PASSED in 0.0s 
Duration min= 0.0s avg = 0.8s max= 1.6s
Lorem ipsum dolor sit amet
"""

TEST_LOG_NO_TIME = """
//tests/test5 NO STATUS  
Duration min= 0.0s avg = 0.8s max= 1.6s
Lorem ipsum dolor sit amet
"""

TEST_LOG_FLAKY_TEST_RESULTS = """
//tests/test6 FLAKY, failed in 1 out of 4 in 5.6s 
Duration min= 0.0s avg = 0.8s max= 1.6s
Lorem ipsum dolor sit amet
"""

TEST_LOG_WITH_TEST_OUTPUT = """
//tests/test3 FAILED in 3.2s
Duration min= 0.0s avg = 0.8s max= 1.6s
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
==================== Test output for //tests/test3:
[Debug] Irrelevant debug output.
[Info] Irrelevant information.
Line 1
Line 2
Line 3
================================================================================
"""

TEST_LOG_WITH_TEST_OUTPUT_AND_EMPTY_LINE = """
//tests/test3 FAILED in 3.2s
Duration min= 0.0s avg = 0.8s max= 1.6s
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
==================== Test output for //tests/test3:
[Debug] Irrelevant debug output.
[Info] Irrelevant information.
"""


TEST_LOG2 = """
==================== Test output for //tests/test3:
===============================================================================
"""


class TestParseTestLogToJson(TestCase):
    def setUp(self) -> None:
        self.build = create_test_zuulbuild("1234", "name")
        self.output_dir = Path("/mocked_path")
        self.build_dir = self.output_dir / "1234"
        self.log_file = self.build_dir / "test_log.txt"
        self.log_file2 = self.build_dir / "test_log2.txt"
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                max_log_length=2, enable_caching=False, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={self.build.uuid: BuildPaths(log_path=self.log_file, log_url="url1")}
            ),
        }

    def tearDown(self) -> None:
        pass

    # Test parse_to_json
    @patch.object(Path, "exists", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json.logging"
    )
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json._parse_log"
    )
    def test_cached_parsed_json_exists(
        self, mock_parse_log: MagicMock, mock_logging: MagicMock, mock_path_exists: MagicMock
    ) -> None:
        """
        Verify that parse_test_log_to_json does not parse the json file again if the json is
        already cached and a cached marker is stored
        """
        # Given a ZuulBuild with already cached parsed json
        self.context["data_collection_pipeline_config"].enable_caching = True
        # When parse_test_log_to_json
        return_value = parse_test_log_to_json(self.build, self.context)
        # Then the json file is not parsed again and the path to the json path is set for the corresponding attribue of the ZuulBuild
        self.assertIsNone(return_value)
        self.assertEqual(mock_parse_log.get.call_count, 0)  # No new parsing of the json
        self.assertEqual(mock_logging.debug.call_count, 1)
        self.assertEqual(
            str(self.context["data_collection_pipeline_status"].builds[self.build.uuid].json_path),
            str(self.output_dir) + "/1234/parsed_status_by_test.json",
        )

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json.logging"
    )
    def test_parse_to_json_no_log_path(self, mock_logging: MagicMock) -> None:
        """
        Verify that parse_test_log_to_json keeps the context untouched for a ZuulBuild
        if the log_path is not defined for this ZuulBuild and a warning message is logged
        """
        # Given log_path is not set for the ZuulBuild
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].log_path = None
        context_prior_parse_test_log = deepcopy(self.context)
        # When parse_test_log_to_json
        return_value = parse_test_log_to_json(self.build, self.context)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.warning.call_count, 1)
        self.assertEqual(self.context, context_prior_parse_test_log)

    @patch.object(Path, "exists", return_value=False)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json.logging"
    )
    def test_parse_to_json_no_file_in_path(self, mock_logging: MagicMock, mock_path_exists: MagicMock) -> None:
        """
        Verify that parse_test_log_to_json keeps the context untouched for a ZuulBuild
        if the json to be parsed can not be found under the specified log_path for this ZuulBuild
        and a warning message is logged
        """
        # Given there is no file locate to the log_path
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].log_path = (
            self.build_dir / "no_test_log.txt"
        )  # Not needed since Path.exists is mocked, but added for clarity
        context_prior_parse_test_log = deepcopy(self.context)
        # When parse_test_log_to_json
        return_value = parse_test_log_to_json(self.build, self.context)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_logging.warning.call_count, 1)
        self.assertEqual(self.context, context_prior_parse_test_log)

    @patch.object(Path, "is_file", return_value=True)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json.logging"
    )
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json._parse_log"
    )
    def test_parse_to_json_no_log_url(
        self, mock_parse_log: MagicMock, mock_logging: MagicMock, mock_path_is_file: MagicMock
    ) -> None:
        """
        Verify that parse_test_log_to_json does not parse the json file if the log_url is not set
        for this ZuulBuild and a debug message is logged
        """
        # Given log_url is not set for the ZuulBuild
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].log_url = False
        # When parse_test_log_to_json
        return_value = parse_test_log_to_json(self.build, self.context)
        # Then context is unchanged
        self.assertIsNone(return_value)
        self.assertEqual(mock_parse_log.get.call_count, 0)  # No new parsing of the json
        self.assertEqual(mock_logging.debug.call_count, 1)

    @patch("builtins.open", mock_open())
    @patch.object(Path, "is_file", return_value=True)
    @patch.object(Path, "touch", return_value=None)
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.parse_test_log_to_json.logging"
    )
    def test_parse_to_json(
        self, mock_logging: MagicMock, mock_path_touch: MagicMock, mock_path_is_file: MagicMock
    ) -> None:
        """
        Verify that parse_test_log_to_json set the correct attribute of
        the ZuulBuild in the context after DownloadSpec of a archive file
        """
        # When parse_test_log_to_json
        return_value = parse_test_log_to_json(self.build, self.context)
        # Then the corresponding attribute of the ZuulBuild is set in the context
        self.assertIsNone(return_value)
        self.assertEqual(
            self.context["data_collection_pipeline_status"].builds[self.build.uuid].json_path,
            self.output_dir / "1234/parsed_status_by_test.json",
        )
        # And leaving marker is created
        mock_logging.debug.assert_called_with(f"Leaving marker '/mocked_path/1234/CACHED_PARSED_TO_JSON'")
        self.assertEqual(mock_path_touch.call_count, 1)

    # Test _parse_log
    @patch("builtins.open", mock_open(read_data=""))
    def test_parse_log_empty_file(self) -> None:
        """
        Verify that _parse_log returns an empty directory if the log file is empty
        """
        status_by_test = _parse_log(self.log_file, "url2", 3)
        self.assertEqual(status_by_test, {})

    @patch("builtins.open", mock_open(read_data=TEST_LOG_ONLY_TEST_RESULTS))
    def test_parse_log_run_test_cases(self) -> None:
        """
        Verify that _parse_log returns the correct parsed logs
        for a log file containing only run testcases with duration
        """
        expected_parsed_logs = {
            "//tests/test2": {"status": "PASSED", "duration": 2.4},
            "//tests/test3": {
                "status": "FAILED",
                "duration": 3.2,
            },
        }
        status_by_test = _parse_log(self.log_file, "url2", 3)
        self.assertEqual(status_by_test, expected_parsed_logs)

    @patch("builtins.open", mock_open(read_data=TEST_LOG_CACHED_TEST_RESULTS))
    def test_parse_log_cached_test_cases(self) -> None:
        """
        Verify that _parse_log returns the correct parsed logs
        for a log file containing only cached testcases
        """
        expected_parsed_logs = {
            "//tests/test1": {"status": "(cached) PASSED", "duration": 0},
        }
        status_by_test = _parse_log(self.log_file, "url2", 3)
        self.assertEqual(status_by_test, expected_parsed_logs)

    @patch("builtins.open", mock_open(read_data=TEST_LOG_NO_TIME))
    def test_parse_log_no_time(self) -> None:
        """
        Verify that _parse_log returns the correct parsed logs
        for a log file containing only run testcases without duration
        """
        expected_parsed_logs = {
            "//tests/test5": {"status": "NO STATUS", "duration": -1},
        }
        status_by_test = _parse_log(self.log_file, "url2", 3)
        self.assertEqual(status_by_test, expected_parsed_logs)

    @patch("builtins.open", mock_open(read_data=TEST_LOG_FLAKY_TEST_RESULTS))
    def test_parse_log_flaky(self) -> None:
        """
        Verify that _parse_log returns the correct parsed logs
        for a log file containing only run flaky testcases
        """
        expected_parsed_logs = {
            "//tests/test6": {"status": "FLAKY", "duration": 0.8},
        }
        status_by_test = _parse_log(self.log_file, "url2", 3)
        self.assertEqual(status_by_test, expected_parsed_logs)

    @patch("builtins.open", mock_open(read_data=TEST_LOG_WITH_TEST_OUTPUT))
    def test_parse_log_with_test_output(self) -> None:
        """
        Verify that _parse_log returns the correct parsed logs
        for a log file containing test output messages
        Verify that the log, the url and the starting line of the log
        is correctly added
        """
        expected_parsed_logs = {
            "//tests/test3": {
                "status": "FAILED",
                "duration": 3.2,
                "error_log": {"log": "Line 1\nLine 2\nLine 3\n", "url": "test_url", "line": 8},
            },
        }
        status_by_test = _parse_log(self.log_file, "test_url", 3)
        self.assertEqual(status_by_test, expected_parsed_logs)

    @patch("builtins.open", mock_open(read_data=TEST_LOG_WITH_TEST_OUTPUT))
    def test_parse_log_with_test_output_last_2_lines(self) -> None:
        """
        Verify that _parse_log returns the correct parsed logs
        for a log file containing test output messages
        Verify that the log length is set accordingly to the tail parameter
        defined in _parse_log
        """
        expected_parsed_logs = {
            "//tests/test3": {
                "status": "FAILED",
                "duration": 3.2,
                "error_log": {"log": "Line 2\nLine 3\n", "url": "test_url", "line": 8},
            },
        }
        # This test verifies _tail_log in the mean time
        status_by_test = _parse_log(self.log_file, "test_url", 2)
        self.assertEqual(status_by_test, expected_parsed_logs)

    @patch("builtins.open", mock_open(read_data=TEST_LOG_WITH_TEST_OUTPUT_AND_EMPTY_LINE))
    def test_parse_log_with_empty_line(self) -> None:
        """
        Verify that if the testlog ends with a logging message
        """
        expected_parsed_logs = {
            "//tests/test3": {
                "status": "FAILED",
                "duration": 3.2,
            },
        }
        # This test verifies _tail_log in the mean time
        status_by_test = _parse_log(self.log_file, "test_url", 2)
        self.assertEqual(status_by_test, expected_parsed_logs)

    def test_tail_log_with_no_escaped_logs(self) -> None:
        """
        Verify that _tail_log returns the corresponding amount of tails when the log
        error_message does not end with \n
        """
        returned_log = _tail_log("Ignored Line\nSecond Line from the bottom\nLast Line", 2)
        self.assertEqual(returned_log, "Second Line from the bottom\nLast Line\n")


if __name__ == "__main__":
    unittest.main()
