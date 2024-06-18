import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.constants import (
    JOB_OUTPUT_NAME,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts import (
    extract_githash,
    parse_job_output_for_githash,
    parse_yaml_for_githash,
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
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.test.mocks.utils import (
    create_test_zuulbuild,
)

VALID_YAML = """
build:
  date: 20210112T075107528805
  githash:
    adp: f7bef927ba0d418287a43e6253d3f9cdb4484fb6
    amp: 5af1a7f6bf5dbcad74114e4b4f2358fad4a6be36
    ddad: 8483568020aa12aadbad6e0358d907f1f0a53bd8
  other: text
"""

YAML_WITHOUT_BUILD = """
other: text
"""

JOB_OUTPUT = """
| node | Checking out files:  99% (49196/49692)
| node | Checking out files: 100% (49692/49692)
| node | Checking out files: 100% (49692/49692), done.
| node | cc-github.bmwgroup.net/swh/adp checked out to:
| node | f7bef927ba0d418287a43e6253d3f9cdb4484fb6 Merge pull request
| node | cc-github.bmwgroup.net/swh/amp checked out to:
| node | 5af1a7f6bf5dbcad74114e4b4f2358fad4a6be36 Merge pull request
| node | cc-github.bmwgroup.net/swh/ddad checked out to:
| node | 8483568020aa12aadbad6e0358d907f1f0a53bd8 Submodules updated
| node | Checking out files: 100% (15417/15417)
| node | Checking out files: 100% (15417/15417), done.
"""


class TestExtractGithash(TestCase):
    def setUp(self) -> None:
        self.build = create_test_zuulbuild("1234", "name")
        self.output_dir = Path("/mocked_path")
        self.yaml_path = Path("/mocked_path/test_yaml_file.yaml")
        self.log_path = Path("/mocked_path/job_output.txt")
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                enable_caching=True, output_directory=self.output_dir
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(
                builds={
                    self.build.uuid: BuildPaths(
                        yaml_path=self.yaml_path,
                        job_output_path=self.log_path,
                        yaml_name="test_yaml_file",
                    )
                }
            ),
        }
        self.expected_hashes = {
            "adp": "f7bef927ba0d418287a43e6253d3f9cdb4484fb6",
            "amp": "5af1a7f6bf5dbcad74114e4b4f2358fad4a6be36",
            "ddad": "8483568020aa12aadbad6e0358d907f1f0a53bd8",
        }

    def tearDown(self) -> None:
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_yaml = False
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_job_output = False

    # Test cases for parse_yaml_for_githash
    @patch("builtins.open")
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    def test_parse_yaml_no_path(self, mock_logging: MagicMock, mock_open: MagicMock) -> None:
        """
        Verify that if the ZuulBuild has no yaml_path specified, parse_yaml_for_githash does not try to open a yaml file and a warning message is logged
        """
        # Given a ZuulBuild with no yaml_path associated
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].yaml_path = None
        # When parse_yaml_for_githash
        return_value = parse_yaml_for_githash(self.build, self.context)
        # Then open is not called and a warning message is logged
        self.assertIsNone(return_value)
        self.assertEqual(mock_open.call_count, 0)
        mock_logging.warning.assert_called_once()

    @patch("builtins.open")
    @patch.object(Path, "is_file", return_value=False)
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    def test_parse_yaml_no_file(
        self, mock_logging: MagicMock, mock_path_is_file: MagicMock, mock_open: MagicMock
    ) -> None:
        """
        Verify that if the ZuulBuild has a yaml_path specified, but the path specified does not point to a valid file,
        parse_yaml_for_githash does not try to open a yaml file and a warning message is logged
        """
        # Given a ZuulBuild with no yaml_path associated
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].yaml_path = Path(
            "/mocked_path/no_yaml.yaml"
        )  # Not required since is_file is mocked, but added for comprehension
        # When parse_yaml_for_githash
        return_value = parse_yaml_for_githash(self.build, self.context)
        # Then open is not called and a warning message is logged
        self.assertIsNone(return_value)
        self.assertEqual(mock_open.call_count, 0)
        mock_logging.warning.assert_called_once()

    @patch("builtins.open", mock_open(read_data=VALID_YAML))
    @patch.object(Path, "is_file", return_value=True)
    def test_parse_yaml(self, mock_path_is_file: MagicMock) -> None:
        """
        Verify that if the ZuulBuild has a valid yaml containing a build part,
        the githashes contains in the build are copied in the githash attribute of the ZuulBuild
        """
        # When parse_yaml_for_githash
        return_value = parse_yaml_for_githash(self.build, self.context)
        # Then the githash are copied to ZuulBuild.githash
        self.assertIsNone(return_value)
        self.assertEqual(self.build.githash, self.expected_hashes)

    @patch("builtins.open", mock_open(read_data=YAML_WITHOUT_BUILD))
    @patch.object(Path, "is_file", return_value=True)
    def test_parse_yaml_no_build(self, mock_path_is_file: MagicMock) -> None:
        """
        Verify that if the ZuulBuild has a valid yaml that does not contain a build part,
        the githash attribute of the ZuulBuild is still empty after call of parse_yaml_for_githash
        """
        # When parse_yaml_for_githash
        return_value = parse_yaml_for_githash(self.build, self.context)
        # Then ZuulBuild.githash is empty
        self.assertIsNone(return_value)
        self.assertEqual(self.build.githash, {})

    # Test cases for parse_job_output_for_githash
    @patch("builtins.open")
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    def test_parse_job_output_no_path(self, mock_logging: MagicMock, mock_open: MagicMock) -> None:
        """
        Verify that if the ZuulBuild has no job_output_path specified, parse_job_output_for_githash does not try to open a file and a debug message is logged
        """
        # Given a ZuulBuild with no job_output_path associated
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].job_output_path = None
        # When parse_job_output_for_githash
        return_value = parse_job_output_for_githash(self.build, self.context)
        # Then open is not called and a debug message is logged
        self.assertIsNone(return_value)
        self.assertEqual(mock_open.call_count, 0)
        mock_logging.debug.assert_called_once()

    @patch("builtins.open")
    @patch.object(Path, "is_file", return_value=False)
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    def test_parse_job_output_no_file(
        self, mock_logging: MagicMock, mock_path_is_file: MagicMock, mock_open: MagicMock
    ) -> None:
        """
        Verify that if the ZuulBuild has a job_output_path specified, but the path specified does not point to a valid file,
        parse_job_output_for_githash does not try to open a file and a debug message is logged
        """
        # Given a ZuulBuild with no job_output_path associated
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].job_output_path = Path(
            "/mocked_path/no_yaml.yaml"
        )  # Not required since is_file is mocked, but added for comprehension
        # When parse_job_output_for_githash
        return_value = parse_job_output_for_githash(self.build, self.context)
        # Then open is not called and a debug message is logged
        self.assertIsNone(return_value)
        self.assertEqual(mock_open.call_count, 0)
        mock_logging.debug.assert_called_once()

    @patch("builtins.open", mock_open(read_data=JOB_OUTPUT))
    @patch.object(Path, "is_file", return_value=True)
    def test_parse_job_output(self, mock_path_is_file: MagicMock) -> None:
        """
        Verify that if the ZuulBuild has a valid job_output containing lines with 'checked out',
        the githashes contains in the job_output file are copied in the githash attribute of the ZuulBuild
        """
        # When parse_job_output_for_githash
        return_value = parse_job_output_for_githash(self.build, self.context)
        # Then the githash are copied to ZuulBuild.githash
        self.assertIsNone(return_value)
        self.assertEqual(self.build.githash, self.expected_hashes)

    # Test cases for extract_githash
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.parse_yaml_for_githash"
    )
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.download_generic_zuul_content"
    )
    def test_extract_githash_has_yaml(
        self, mock_download_generic_zuul_content: MagicMock, mock_parse_yaml_for_githash: MagicMock
    ) -> None:
        """
        Verify that extract_githash calls parse_yaml_for_githash with the correct parameters if has_yaml is set for the ZuulBuild
        """
        # Given has_yaml is set
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_yaml = True
        download_spec = DownloadSpec(
            file_name="test_yaml_file",
            content_type=ContentType.TEXT,
            cache_prefix=CachePrefixType.ADPBUILD,
        )
        # When extract_githash
        return_value = extract_githash(self.build, self.context)
        # Then the functions are called with the correct parameters
        self.assertIsNone(return_value)
        mock_download_generic_zuul_content.assert_called_with(self.build, self.context, download_spec)
        mock_parse_yaml_for_githash.assert_called_with(self.build, self.context)

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.parse_job_output_for_githash"
    )
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.download_generic_zuul_content"
    )
    def test_extract_githash_has_job_output(
        self, mock_download_generic_zuul_content: MagicMock, mock_parse_job_output_for_githash: MagicMock
    ) -> None:
        """
        Verify that extract_githash calls parse_job_output_for_githash with the correct parameters if has_job_output is set for the ZuulBuild
        """
        # Given has_job_output is set
        self.context["data_collection_pipeline_status"].builds[self.build.uuid].has_job_output = True
        download_spec = DownloadSpec(
            file_name=JOB_OUTPUT_NAME,
            content_type=ContentType.TEXT,
            cache_prefix=CachePrefixType.JOB_OUTPUT,
        )
        # When extract_githash
        return_value = extract_githash(self.build, self.context)
        # Then the functions are called with the correct parameters
        self.assertIsNone(return_value)
        mock_download_generic_zuul_content.assert_called_with(self.build, self.context, download_spec)
        mock_parse_job_output_for_githash.assert_called_with(self.build, self.context)

    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.parse_yaml_for_githash"
    )
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.parse_job_output_for_githash"
    )
    @patch(
        "ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.download_generic_zuul_content"
    )
    @patch("ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.extracts.logging")
    def test_extract_githash_no_file(
        self,
        mock_logging: MagicMock,
        mock_download_generic_zuul_content: MagicMock,
        mock_parse_job_output_for_githash: MagicMock,
        mock_parse_yaml_for_githash: MagicMock,
    ) -> None:
        """
        Verify that extract_githash does not call download_generic_zuul_content, parse_job_output_for_githash and parse_job_output_for_githash
        if neither has_yaml nor has_job_output is set for the ZuulBuild, and a warning message is logged
        """
        # When extract_githash
        return_value = extract_githash(self.build, self.context)
        # Then the functions are called with the correct parameters
        self.assertIsNone(return_value)
        self.assertEqual(mock_download_generic_zuul_content.call_count, 0)
        self.assertEqual(mock_parse_yaml_for_githash.call_count, 0)
        self.assertEqual(mock_parse_job_output_for_githash.call_count, 0)
        self.assertEqual(mock_logging.warning.call_count, 1)


if __name__ == "__main__":
    unittest.main()
