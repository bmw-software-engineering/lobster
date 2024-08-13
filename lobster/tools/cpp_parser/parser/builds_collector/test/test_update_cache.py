import datetime
import json
import unittest
from pathlib import Path
from unittest import TestCase

import pandas as pd

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.data_collection.manage_cache import (
    _update_with_cache,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_config import (
    DataCollectionPipelineConfig,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.data_collection_pipeline_status import (
    DataCollectionPipelineStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildResult,
    PipelineType,
    ZuulJobConfiguration,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.test_status import (
    TestStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.mapping.db_config import (
    BuildMetadataMapping,
    create_storage,
)


class TestCreateDataframes(TestCase):
    def setUp(self) -> None:
        self.output_dir = Path("/mocked_path")
        self.storage = create_storage(f"sqlite:///test_create_data_frames:memory:")
        self.context = {
            "data_collection_pipeline_config": DataCollectionPipelineConfig(
                branch="master",
                zuul_job=ZuulJobConfiguration("job", PipelineType.POST_INDEPENDENT),
                output_directory=self.output_dir,
            ),
            "data_collection_pipeline_status": DataCollectionPipelineStatus(),
            "storage": self.storage,
        }

        self.today = datetime.datetime.now(datetime.timezone.utc)
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
        self.df_cached = pd.DataFrame(
            {
                "uuid": ["0", "1", "1", "2"],
                "test_name": ["a_test", "a_test", "c_test", "<no build result>"],
                "test_status": [
                    TestStatus.PASSED,
                    TestStatus.FAILED,
                    TestStatus.PASSED,
                    TestStatus.GLOBAL_PROBLEM,
                ],
                "test_duration": [10, 0, 166, -1],
                "error_log": ["", "a_test error", "", ""],
            }
        )
        self.storage.write_dataframe("df_narrow_job_master", self.df_cached)
        self.storage.update_mappings(BuildMetadataMapping, self.build_metadata_mappings)

    def tearDown(self) -> None:
        pass

    def test_update_with_cache(self) -> None:
        df_narrow = pd.DataFrame(
            {
                "uuid": ["0", "0", "1", "1"],
                "test_name": ["a_test", "b_test", "a_test", "c_test"],
                "test_status": [
                    TestStatus.FAILED,
                    TestStatus.FAILED,
                    TestStatus.FAILED,
                    TestStatus.PASSED,
                ],
                "test_duration": [5, 155, 0, 166],
                "error_log": ["a_test error", "b_test error", "a_test error", ""],
            }
        )
        actual = _update_with_cache(df_narrow, self.context)
        target = pd.DataFrame(
            {
                "uuid": ["0", "0", "1", "1", "2"],
                "test_name": [
                    "a_test",
                    "b_test",
                    "a_test",
                    "c_test",
                    "<no build result>",
                ],
                "test_status": [
                    TestStatus.FAILED,
                    TestStatus.FAILED,
                    TestStatus.FAILED,
                    TestStatus.PASSED,
                    TestStatus.GLOBAL_PROBLEM,
                ],
                "test_duration": [5, 155, 0, 166, -1],
                "error_log": ["a_test error", "b_test error", "a_test error", "", ""],
            }
        )
        self.assertTrue(actual.equals(target))


if __name__ == "__main__":
    unittest.main()
