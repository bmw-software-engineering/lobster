import json
import unittest
from pathlib import Path
from typing import List
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.collect_jsons_to_narrow_df import (
    collect_jsons_to_narrow_df,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_status import (
    DataCollectionPipelineStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import BuildPaths
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.test_status import (
    TestStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.utils import (
    create_test_zuulbuild,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild

VALID_LOG_1 = """{
        "a_test":{
            "error_log" : {"log": "a_test error", "url": "url1", "line": 1},
            "status": "FAILED",
            "duration": 5
        },
        "b_test":{
            "error_log" : {"log": "b_test error", "url": "url1", "line": 5},
            "status": "FAILED",
            "duration": 155
        }
    }"""
VALID_LOG_2 = """{
        "a_test":{
            "error_log" : {"log": "a_test error", "url": "url2", "line": 3},
            "status": "PASSED",
            "duration": 6
        }
    }"""

MISSING_TESTCASE_STATUS_LOG = """{
        "single_test":{
            "error_log" : {"log": "missing test case", "url": "abc", "line": 8},
            "duration": 15
        }
    }"""

MISSING_ERROR_LOG = """{
        "single_test_missing_error_logs":{
            "status": "PASSED",
            "duration": 2023
        }
    }"""


class TestCollectJsonsToNarrowDf(TestCase):
    def setUp(self) -> None:
        self.output_dir = Path("/mocked_path")

    def tearDown(self) -> None:
        pass

    @patch("builtins.open", mock_open())
    def create_builds(self, number) -> List[ZuulBuild]:
        builds = []
        for uuid in range(number):
            builds.append(create_test_zuulbuild(str(uuid), "name"))
        return builds

    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=True)
    def test_collect_jsons_to_narrow_df_one_build(
        self, mock_path_is_file: MagicMock, mock_mock_open: MagicMock
    ) -> None:
        """
        Verify that one build is correctly parsed
        """
        # Given 1 build
        self.builds = self.create_builds(1)
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0", "0"],
                "test_name": [
                    "a_test",
                    "b_test",
                ],
                "test_status": [
                    TestStatus.FAILED,
                    TestStatus.FAILED,
                ],
                "test_duration": [5, 155],
                "error_log": [
                    {"log": "a_test error", "url": "url1", "line": 1},
                    {"log": "b_test error", "url": "url1", "line": 5},
                ],
            }
        )

        handlers = (mock_open(read_data=VALID_LOG_1).return_value,)
        mock_mock_open.side_effect = handlers
        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then the build dataframe is returned
        self.assertTrue(expected_df.equals(actual_df))

    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=True)
    def test_collect_jsons_to_narrow_df_multiple_builds(
        self, mock_path_is_file: MagicMock, mock_mock_open: MagicMock
    ) -> None:
        """
        Verify that multiple build are correctly parsed
        """
        # Given 2 builds
        self.builds = self.create_builds(2)
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                    "1": BuildPaths(json_path=self.output_dir / "1.json"),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0", "0", "1"],
                "test_name": [
                    "a_test",
                    "b_test",
                    "a_test",
                ],
                "test_status": [
                    TestStatus.FAILED,
                    TestStatus.FAILED,
                    TestStatus.PASSED,
                ],
                "test_duration": [5, 155, 6],
                "error_log": [
                    {"log": "a_test error", "url": "url1", "line": 1},
                    {"log": "b_test error", "url": "url1", "line": 5},
                    {"log": "a_test error", "url": "url2", "line": 3},
                ],
            }
        )

        handlers = (
            mock_open(read_data=VALID_LOG_1).return_value,
            mock_open(read_data=VALID_LOG_2).return_value,
        )
        mock_mock_open.side_effect = handlers
        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then all builds dataframe are returned
        self.assertTrue(expected_df.equals(actual_df))

    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=True)
    def test_collect_jsons_to_narrow_df_build_cached(
        self, mock_path_is_file: MagicMock, mock_mock_open: MagicMock
    ) -> None:
        """
        Verify that if a build is cached, the build is not returned by collect_jsons_to_narrow_df
        """
        # Given 2 builds, with the second one .cached = True
        self.builds = self.create_builds(2)
        self.builds[1].cached = True
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                    "1": BuildPaths(json_path=self.output_dir / "1.json"),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0", "0"],
                "test_name": [
                    "a_test",
                    "b_test",
                ],
                "test_status": [
                    TestStatus.FAILED,
                    TestStatus.FAILED,
                ],
                "test_duration": [5, 155],
                "error_log": [
                    {"log": "a_test error", "url": "url1", "line": 1},
                    {"log": "b_test error", "url": "url1", "line": 5},
                ],
            }
        )

        handlers = (
            mock_open(read_data=VALID_LOG_1).return_value,
            mock_open(read_data=VALID_LOG_2).return_value,
        )
        mock_mock_open.side_effect = handlers
        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then only the first build dataframe is returned
        self.assertTrue(expected_df.equals(actual_df))
        # Verify that the second json file is not opened, since the build is already cached
        self.assertEqual(mock_mock_open.call_count, 1)

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.collect_jsons_to_narrow_df.logging"
    )
    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=True)
    def test_collect_jsons_to_narrow_df_no_json_path(
        self, mock_path_is_file: MagicMock, mock_mock_open: MagicMock, mock_logging: MagicMock
    ) -> None:
        """
        Verify that if a build does not have a path to a json file, the build is returned with default values in the dataframe
        """
        # Given 2 builds, with the second one having an empty json path
        self.builds = self.create_builds(2)
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                    "1": BuildPaths(json_path=None),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0", "0", "1"],
                "test_name": ["a_test", "b_test", "<no build result>"],
                "test_status": [TestStatus.FAILED, TestStatus.FAILED, TestStatus.GLOBAL_PROBLEM],
                "test_duration": [5, 155, -1],
                "error_log": [
                    {"log": "a_test error", "url": "url1", "line": 1},
                    {"log": "b_test error", "url": "url1", "line": 5},
                    None,
                ],
            }
        )
        handlers = (
            mock_open(read_data=VALID_LOG_1).return_value,
            mock_open(read_data=VALID_LOG_2).return_value,
        )
        mock_mock_open.side_effect = handlers
        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then the first build dataframe is correctly set, and default values are set for the second build
        self.assertTrue(expected_df.equals(actual_df))
        # Verify that the second json file is not opened, since there is no json path defined for the second build
        self.assertEqual(mock_mock_open.call_count, 1)
        # Verify that a debug call is added to the logs
        self.assertEqual(mock_logging.debug.call_count, 1)

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.collect_jsons_to_narrow_df.logging"
    )
    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=False)  # is_file returns False
    def test_collect_jsons_to_narrow_df_no_json_file(
        self, mock_path_is_file: MagicMock, mock_mock_open: MagicMock, mock_logging: MagicMock
    ) -> None:
        """
        Verify that if a build does not have a path to a json file, the build is returned with default values in the dataframe
        """
        # Given 1 build, with no file located at the json path location (path.is_file returns False)
        self.builds = self.create_builds(1)
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0"],
                "test_name": ["<no build result>"],
                "test_status": [TestStatus.GLOBAL_PROBLEM],
                "test_duration": [-1],
                "error_log": [None],
            }
        )

        handlers = (mock_open(read_data=VALID_LOG_1).return_value,)

        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then default values are set for the build
        self.assertTrue(expected_df.equals(actual_df))
        # Verify that a debug call is added to the logs
        self.assertEqual(mock_logging.debug.call_count, 1)

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.collect_jsons_to_narrow_df.logging"
    )
    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=True)
    @patch.object(json, "load", return_value={})
    def test_collect_jsons_to_narrow_df_no_json_path(
        self,
        mock_json_load: MagicMock,
        mock_path_is_file: MagicMock,
        mock_mock_open: MagicMock,
        mock_logging: MagicMock,
    ) -> None:
        """
        Verify that if the json file associated to a build is empty, the build is returned with default values in the dataframe
        """
        # Given 1 build, with empty json file
        self.builds = self.create_builds(1)
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0"],
                "test_name": ["<no build result>"],
                "test_status": [TestStatus.GLOBAL_PROBLEM],
                "test_duration": [-1],
                "error_log": [None],
            }
        )

        # Open returns whatever (we just dont want to raise Exception here)
        handlers = (mock_open(read_data="{}").return_value,)

        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then default values are set for the build
        self.assertTrue(expected_df.equals(actual_df))
        # Verify that a warning call is added to the logs
        self.assertEqual(mock_logging.warning.call_count, 1)

    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=True)
    def test_collect_jsons_to_narrow_df_missing_test_status(
        self, mock_path_is_file: MagicMock, mock_mock_open: MagicMock
    ) -> None:
        """
        Verify that if one test case of the build is missing a test status, the TestStatus.FAILED is assigned by default and duration is set to 0
        """
        # Given 1 build
        self.builds = self.create_builds(1)
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0"],
                "test_name": ["single_test"],
                "test_status": [TestStatus.FAILED],
                "test_duration": [0],
                "error_log": [{"log": "missing test case", "url": "abc", "line": 8}],
            }
        )

        handlers = (mock_open(read_data=MISSING_TESTCASE_STATUS_LOG).return_value,)
        mock_mock_open.side_effect = handlers
        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then the build dataframe is returned with a TestStatus.FAILED and a duration of 0
        self.assertTrue(expected_df.equals(actual_df))

    @patch("builtins.open", new_callable=mock_open)
    @patch.object(Path, "is_file", return_value=True)
    def test_collect_jsons_to_narrow_df_missing_test_status(
        self, mock_path_is_file: MagicMock, mock_mock_open: MagicMock
    ) -> None:
        """
        Verify that if one test case of the build is missing an error_log, the error_log is set to None
        """
        # Given 1 build
        self.builds = self.create_builds(1)
        self.context = {
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    "0": BuildPaths(json_path=self.output_dir / "0.json"),
                }
            )
        }
        expected_df = pd.DataFrame(
            {
                "uuid": ["0"],
                "test_name": ["single_test_missing_error_logs"],
                "test_status": [TestStatus.PASSED],
                "test_duration": [2023],
                "error_log": [None],
            }
        )

        handlers = (mock_open(read_data=MISSING_ERROR_LOG).return_value,)
        mock_mock_open.side_effect = handlers
        # When calling function
        actual_df = collect_jsons_to_narrow_df(self.builds, self.context)
        # Then the build dataframe is returned with a error_log None
        self.assertTrue(expected_df.equals(actual_df))


if __name__ == "__main__":
    unittest.main()
