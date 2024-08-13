import datetime
import json
import unittest
from tempfile import NamedTemporaryFile
from unittest import TestCase

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildResult,
    PipelineType,
    ZuulJobConfiguration,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.mapping import (
    BuildMetadataMapping,
    create_storage,
)


class TestSqlStorage(TestCase):
    def setUp(self) -> None:
        self.test_file = NamedTemporaryFile()
        self.storage = create_storage(f"sqlite:///{self.test_file.name}:memory:")
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                branch="master", zuul_job=ZuulJobConfiguration("job", PipelineType.POST_INDEPENDENT)
            ),
            "storage": self.storage,
        }
        self.today = datetime.datetime.now()
        self.githash = {"adp": "hash1", "amp": "hash2", "ddad": "hash3"}
        self.build_metadata_mappings = [
            BuildMetadataMapping(
                uuid="1",
                branch="master",
                job_name="job",
                pr_url="url/pull/1",
                start_time=self.today,
                githash=json.dumps(self.githash),
                ci_result=BuildResult.FAILURE,
            ),
            BuildMetadataMapping(
                uuid="2",
                branch="master",
                job_name="job",
                pr_url="url/pull/2",
                start_time=self.today,
                githash=json.dumps(self.githash),
                ci_result=BuildResult.SUCCESS,
            ),
            BuildMetadataMapping(
                uuid="1",
                branch="other",
                job_name="job",
                pr_url="url/pull/1",
                start_time=self.today,
                githash=json.dumps(self.githash),
                ci_result=BuildResult.RETRY_LIMIT,
            ),
        ]
        self.storage.update_mappings(BuildMetadataMapping, self.build_metadata_mappings)

    def tearDown(self) -> None:
        self.test_file.close()

    # Helper function to compare 2 BuildMetadataMapping
    def assert_mapping_equals(self, actual: BuildMetadataMapping, target: BuildMetadataMapping) -> None:
        self.assertEqual(actual.uuid, target.uuid)
        self.assertEqual(actual.job_name, target.job_name)
        self.assertEqual(actual.branch, target.branch)
        self.assertEqual(actual.pr_url, target.pr_url)
        self.assertEqual(actual.start_time, target.start_time)
        self.assertEqual(actual.githash, target.githash)
        self.assertEqual(actual.ci_result, target.ci_result)

    # Test read_dataframe
    # TODO: For now tested as part of manage_cache, but will need separate test cases

    # Test write_dataframe
    # TODO: For now tested as part of manage_cache, but will need separate test cases

    # Test get_mappings
    def test_get_mappings_when_no_criteria(self) -> None:
        """
        Verify that when criteria is not set,
        Then all the builds are returned by get_mappings
        """
        actuals = self.storage.get_mappings(BuildMetadataMapping)
        self.assertEqual(len(actuals), len(self.build_metadata_mappings))

    def test_get_mappings_when_criteria_is_branch(self) -> None:
        """
        Verify that when criteria is set to branch=master,
        Then only the builds for this branch are returned by get_mappings
        """
        criteria = [
            BuildMetadataMapping.branch == "master",
        ]
        returned_builds = self.storage.get_mappings(BuildMetadataMapping, criteria)

        for build in returned_builds:
            self.assertEqual(build.branch, "master")

    # Test update_mappings
    def test_update_mappings(self) -> None:
        """
        Verify that the data is updated after a call of update_mappings
        """
        update_build_metadata = self.build_metadata_mappings[0]
        update_build_metadata.pr_url = "new_url"
        update_build_metadata.ci_result = BuildResult.TIMED_OUT

        self.storage.update_mappings(BuildMetadataMapping, [update_build_metadata])
        returned_builds = self.storage.get_mappings(BuildMetadataMapping)

        expected = [
            BuildMetadataMapping(
                uuid="1",
                branch="master",
                job_name="job",
                pr_url="new_url",  # updated
                start_time=self.today,
                githash=json.dumps(self.githash),
                ci_result=BuildResult.TIMED_OUT,  # updated
            ),
            BuildMetadataMapping(
                uuid="2",
                branch="master",
                job_name="job",
                pr_url="url/pull/2",
                start_time=self.today,
                githash=json.dumps(self.githash),
                ci_result=BuildResult.SUCCESS,
            ),
            BuildMetadataMapping(
                uuid="1",
                branch="other",
                job_name="job",
                pr_url="url/pull/1",
                start_time=self.today,
                githash=json.dumps(self.githash),
                ci_result=BuildResult.RETRY_LIMIT,
            ),
        ]

        for actual_build, expected_build in zip(returned_builds, expected):
            self.assert_mapping_equals(actual_build, expected_build)

    # Test delete_mappings
    def test_delete_mappings_when_criteria_is_branch(self) -> None:
        """
        When criteria is set to branch=master,
        Then only the builds for this branch are deleted by delete_mappings
        """
        criteria = [
            BuildMetadataMapping.branch == "master",
        ]
        actuals = self.storage.get_mappings(BuildMetadataMapping)
        self.assertEqual(len(actuals), 3)

        # The 2 builds for branch master are deleted
        self.storage.delete_mappings(BuildMetadataMapping, criteria)
        actuals = self.storage.get_mappings(BuildMetadataMapping)
        self.assertEqual(len(actuals), 1)

    def test_delete_mappings_when_no_criteria(self) -> None:
        """
        When criteria is set to branch=master,
        Then only the builds for this branch are deleted by delete_mappings
        """
        actuals = self.storage.get_mappings(BuildMetadataMapping)
        self.assertEqual(len(actuals), 3)

        # All builds are deleted
        self.storage.delete_mappings(BuildMetadataMapping)
        actuals = self.storage.get_mappings(BuildMetadataMapping)
        self.assertEqual(len(actuals), 0)

    # Test create_session
    # TODO


if __name__ == "__main__":
    unittest.main()
