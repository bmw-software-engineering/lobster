import datetime
import json
import unittest
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import MagicMock

import pandas as pd

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.manage_cache import (
    get_cached_builds,
    get_table_name_from_context,
    set_cached_in_builds,
    update_builds_cache,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildMetadata,
    BuildResult,
    PipelineType,
    PullRequestInfo,
    PullRequestState,
    ZuulJobConfiguration,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.test_status import (
    TestStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.mapping import (
    BuildMetadataMapping,
    create_storage,
)


class TestManageCache(TestCase):
    def setUp(self) -> None:
        self.storage = create_storage(f"sqlite:///test_manage_cache:memory:")
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
        self.build_metadata = {
            "1": BuildMetadata(
                "url/pull/11",
                self.today,
                self.today,
                self.githash,
                BuildResult.FAILURE,
                PullRequestInfo(PullRequestState.MERGED),
                "post-independent",
            ),
            "2": BuildMetadata(
                "url/pull/2",
                self.today,
                self.today,
                self.githash,
                BuildResult.TIMED_OUT,
                PullRequestInfo(PullRequestState.MERGED),
                "post-independent",
            ),
        }
        self.builds = []
        for uuid in range(5):
            build = MagicMock()
            build.uuid = str(uuid)
            build.cached = False
            self.builds.append(build)
        self.df_cached = pd.DataFrame(
            {
                "uuid": ["0", "1", "2", "1"],
                "test_status": [
                    TestStatus.PASSED,
                    TestStatus.PASSED,
                    TestStatus.PASSED,
                    TestStatus.PASSED,
                ],
                "error_log": [None, None, None, None],
            }
        )

    def tearDown(self) -> None:
        pass

    def test_set_cached_in_builds(self) -> None:
        self.storage.write_dataframe("df_narrow_job_master", self.df_cached)
        set_cached_in_builds(self.builds, self.context)
        self.assertTrue(self.builds[1].cached)
        self.assertTrue(self.builds[2].cached)
        self.assertFalse(self.builds[0].cached)
        self.assertFalse(self.builds[3].cached)
        self.assertFalse(self.builds[4].cached)

    def test_no_cached_builds(self) -> None:
        set_cached_in_builds(self.builds, self.context)
        for build in self.builds:
            self.assertFalse(build.cached)

    def test_get_cached_builds(self) -> None:
        actuals = get_cached_builds(self.context)
        for actual, target in zip(actuals, self.build_metadata_mappings[0:2]):
            self.assert_mapping_equals(actual, target)

    def test_update_builds_cache(self) -> None:
        update_builds_cache(self.build_metadata, self.context)
        criteria = [
            BuildMetadataMapping.branch == "master",
            BuildMetadataMapping.job_name == "job",
        ]
        actuals = self.storage.get_mappings(BuildMetadataMapping, criteria)
        targets = [
            BuildMetadataMapping(
                uuid="1",
                branch="master",
                job_name="job",
                pr_url="url/pull/11",
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
                ci_result=BuildResult.TIMED_OUT,
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

        for actual, target in zip(actuals, targets):
            self.assert_mapping_equals(actual, target)

    def test_get_table_name_from_context(self) -> None:
        self.assertEqual(get_table_name_from_context(self.context), "df_narrow_job_master")

    def assert_mapping_equals(self, actual: BuildMetadataMapping, target: BuildMetadataMapping) -> None:
        self.assertEqual(actual.uuid, target.uuid)
        self.assertEqual(actual.job_name, target.job_name)
        self.assertEqual(actual.branch, target.branch)
        self.assertEqual(actual.pr_url, target.pr_url)
        self.assertEqual(actual.start_time, target.start_time)
        self.assertEqual(actual.githash, target.githash)
        self.assertEqual(actual.ci_result, target.ci_result)


if __name__ == "__main__":
    unittest.main()
