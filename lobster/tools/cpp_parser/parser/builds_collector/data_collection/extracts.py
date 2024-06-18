import re
import shutil
import tarfile
from pathlib import Path

import yaml

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    CachePrefixType,
    ContentType,
    ContextType,
    DownloadSpec,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.event_logger import logging
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild

from .constants import JOB_OUTPUT_NAME, TAR_LOGS_NAME, TEST_LOGS_NAME
from .downloads import download_generic_zuul_content

_RE_REPOSITORY_PATTERN = re.compile(r"cc-github\.bmwgroup\.net/swh/([a-z-_]+)")
_RE_GITHASH_PATTERN = re.compile(r"[a-f0-9]{40}")


def extract_build_archive(build: ZuulBuild, context: ContextType) -> None:
    """Extracts test logs from the build archive.
    Extracts the archive specified in the context to the correct location.
    Afterwards a marker given set to enable caching.

    Parameters
    ----------
    build: ZuulBuild
        The build for which the test logs should be extracted.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    build_directory = context["data_collection_pipeline_config"].output_directory / build.uuid
    log_path = build_directory / TEST_LOGS_NAME
    context["data_collection_pipeline_status"].builds[build.uuid].log_path = log_path
    cached_marker_path = build_directory / "CACHED_EXTRACTED"

    cache_extraction = context["data_collection_pipeline_config"].enable_caching
    if cache_extraction and cached_marker_path.exists():
        logging.debug(f"'{build_directory}' is already extracted, skipping")
        return
    tar_path = context["data_collection_pipeline_status"].builds[build.uuid].archive_path

    if not tar_path.is_file():
        logging.warning(f"tar path '{tar_path}' not found")
        return
    _extract_archive(tar_path, build_directory)
    logging.debug("Copy logs")
    if not (build_directory / TAR_LOGS_NAME).is_file():
        logging.warning(f"No log file in archive of {build.uuid}")
        return
    shutil.copyfile(build_directory / TAR_LOGS_NAME, log_path)
    logging.debug(f"Leaving marker '{cached_marker_path}'")
    cached_marker_path.touch()


def _extract_archive(archive: Path, extract_to: Path) -> None:
    """Helper to extract archives.
    Parameters
    ----------
    archive: pathlib.Path
        Archive to be extracted.
    extract_to: pathlib.Path
        Location where to extract to.
    """
    logging.debug(f"Extracting '{archive}'")
    with tarfile.open(archive) as tar:
        tar.extractall(path=extract_to)


def parse_yaml_for_githash(build: ZuulBuild, context: ContextType) -> None:
    """Parses githash information in yaml file.
    The file gets read to find all the githashes and the information is added to the build.
    Parameters
    ----------
    build: ZuulBuild
        The build for which the yaml should be parsed.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    yaml_file_path = context["data_collection_pipeline_status"].builds[build.uuid].yaml_path
    if not yaml_file_path or not yaml_file_path.is_file():
        logging.warning(f"adpbuild '{yaml_file_path}' not found")
        return
    with open(yaml_file_path, "r") as in_file:
        data = yaml.safe_load(in_file)
    data_build = data.get("build")
    if data_build:
        build.githash = data_build.get("githash")


def parse_job_output_for_githash(build: ZuulBuild, context: ContextType) -> None:
    """Parses githash information in text file.
    The file gets parsed to find all the githashes and the information is added to the build.
    The phrase "checked out" indicates a repository, the next line contains the githash.
    Parameters
    ----------
    build: ZuulBuild
        The build for which the JOB_OUTPUT_NAME should be parsed.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    job_output_path = context["data_collection_pipeline_status"].builds[build.uuid].job_output_path
    if not job_output_path or not job_output_path.is_file():
        logging.debug(f"Job output '{job_output_path}' not (yet) found")
        return
    with open(job_output_path, "r") as in_file:
        for line in in_file:
            if "checked out" in line:
                repo_key = _RE_REPOSITORY_PATTERN.search(line).group(1)
                line = in_file.readline()
                commit_hash = _RE_GITHASH_PATTERN.search(line).group()
                build.githash[repo_key] = commit_hash


def extract_githash(build: ZuulBuild, context: ContextType) -> None:
    """Download and parse githash information from Zuul.
    Creates the download spec to download the correct file of a single build.
    The file gets parsed to find all the githashes and the information is added to the build.
    If the yaml file exists use it else fall back to the job output text file.
    Parameters
    ----------
    build: ZuulBuild
        The build for which the githashes should be extracted.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    if context["data_collection_pipeline_status"].builds[build.uuid].has_yaml:
        yaml_name = context["data_collection_pipeline_status"].builds[build.uuid].yaml_name
        download_spec = DownloadSpec(
            file_name=yaml_name,
            content_type=ContentType.TEXT,
            cache_prefix=CachePrefixType.ADPBUILD,
        )
        download_generic_zuul_content(build, context, download_spec)
        parse_yaml_for_githash(build, context)
    elif context["data_collection_pipeline_status"].builds[build.uuid].has_job_output:
        download_spec = DownloadSpec(
            file_name=JOB_OUTPUT_NAME,
            content_type=ContentType.TEXT,
            cache_prefix=CachePrefixType.JOB_OUTPUT,
        )
        download_generic_zuul_content(build, context, download_spec)
        parse_job_output_for_githash(build, context)
    else:
        logging.warning("Impossible to parse githashes for this ZuulBuild")
