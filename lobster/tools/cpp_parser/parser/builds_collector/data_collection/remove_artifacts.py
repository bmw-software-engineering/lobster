import shutil

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import ContextType
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.event_logger import logging
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild

ARTIFACTS = {"testlogs", "bazel_test_log.txt", "bazel_logs.tar.gz"}


def remove_artifact(build: ZuulBuild, context: ContextType, artifact_name: str) -> None:
    """Removes a single artifact.
    Removes the artifact from the temporary build directory.
    Parameters
    ----------
    build: ZuulBuild
        The build for which the artifact should be removed.
    context: ContextType
        Context dictionary containing metadata of the process.
    artifact_name: str
        The artifact to be removed.
    """
    build_directory = context["data_collection_pipeline_config"].output_directory / build.uuid
    logging.debug(f"Removing {build.uuid}/{artifact_name} from disk")
    artifact_path = build_directory / artifact_name
    if artifact_path.is_file():
        artifact_path.unlink()
    elif artifact_path.is_dir():
        shutil.rmtree(artifact_path)
