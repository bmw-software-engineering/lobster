import datetime
from pathlib import PosixPath

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildResult,
    PipelineType,
    ProjectName,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import (
    ZuulBuild,
    ZuulBuildSet,
)


def create_test_zuulbuild(uuid: str, job_name: str, log_url: str = "https://www.url.com") -> PosixPath:
    return ZuulBuild(
        uuid=uuid,
        job_name="name",
        result=BuildResult.SUCCESS,
        start_time=datetime.datetime(2121, 11, 11, 11, 11, 11),
        end_time=datetime.datetime(2121, 11, 11, 11, 11, 11) + datetime.timedelta(minutes=5),
        duration=0.0,
        voting=True,
        log_url=log_url,
        error_detail=None,
        final=True,
        artifacts=[],
        provides=[],
        project=ProjectName.DDAD_CI_CONFIG,
        branch="master",
        pipeline=PipelineType.POST_INDEPENDENT.value,
        change=0,
        patchset="patch",
        ref="https://www.url.com",
        newrev=None,
        ref_url="https://www.url.com",
        event_id=None,
        buildset=ZuulBuildSet(uuid=uuid),
        githash=dict(),
        cached=False,
    )
