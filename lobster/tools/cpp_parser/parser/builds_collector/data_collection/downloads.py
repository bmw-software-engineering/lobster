import json
import re

import requests
from pydantic import HttpUrl

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    CachePrefixType,
    ContentType,
    ContextType,
    DownloadSpec,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.event_logger import logging
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild

from .constants import BAZEL_LOGS_NAME, JOB_OUTPUT_NAME, TEST_LOGS_NAME, ZUUL_MANIFEST_NAME

_RE_YAML_PATTERN = re.compile(r"adpbuild_[A-Z|a-z|0-9]+\.yaml")


def _make_zuul_session() -> requests.Session:
    """Returns zuul session instance
    Returns
    -------
    requests.Session
        Zuul session instance
    """
    session = requests.Session()
    retry_strategy = requests.packages.urllib3.util.retry.Retry(
        total=3, status_forcelist=[429, 500, 502, 503, 504], method_whitelist=["GET"]
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session


def get_url(log_url: HttpUrl, url_extension: str) -> str:
    """Creates a downloadable url.
    Creates an url by replacing the base url and adding an extension
    specifying a file.
    Parameters
    ----------
    log_url: pydantic.HttpUrl
        Base url for Zuul logs.
    url_extension: str
        Relative file name or path to download.
    Returns
    -------
    str
        Url for downloadable zuul content.
    """
    base_url_str = log_url.replace("cc-ci.bmwgroup.net/logs/t/", "cc-ci.bmwgroup.net/logs/a/").rstrip("/")
    return f"{base_url_str}/{url_extension}"


def download_generic_zuul_content(
    build: ZuulBuild,
    context: ContextType,
    download_spec: DownloadSpec,
    session: requests.Session = _make_zuul_session(),
) -> None:
    """Download generic content from Zuul.
    The content specified in the download_spec is saved and assigned to the
    corresponding build. After download, a marker given in the spec is set
    to enable caching. The url is saved for log files.
    Parameters
    ----------
    build: ZuulBuild
        The build for which content should be downloaded.
    context: ContextType
        Context dictionary containing metadata of the process.
    download_spec: DownloadSpec
        Specification of the download.
    """
    build_directory = context["data_collection_pipeline_config"].output_directory / build.uuid
    download_path = build_directory / download_spec.file_name
    cached_marker_path = build_directory / (download_spec.cache_prefix.upper() + "_DOWNLOADED")
    cache_downloads = context["data_collection_pipeline_config"].enable_caching
    if not build.log_url:
        logging.debug(f"Log URL not (yet) available for build '{build.uuid}'")
        return

    if cache_downloads and cached_marker_path.exists():
        setattr(context["data_collection_pipeline_status"].builds[build.uuid], download_spec.dict_key, download_path)
        logging.debug(f"'{download_path}' is already downloaded, skipping")
        return

    url = get_url(build.log_url, download_spec.file_name)
    auth = context["data_collection_pipeline_config"].zuul_auth_pair
    logging.debug(f"Downloading '{url}'")
    try:
        response = session.get(url, auth=auth, allow_redirects=True)
    except requests.exceptions.RequestException:
        logging.warning(f"Exception occured while trying to get: '{url}'")
        return
    logging.debug(f"Response code '{response.status_code}'")
    if response.status_code == requests.codes.not_found:
        logging.warning(f"File not found on server: '{url}'")
        return
    elif response.status_code != requests.codes.ok:
        logging.warning(f"Request not ok")
        return

    logging.debug(f"Received {len(response.content):,d} bytes")
    download_path.parent.mkdir(parents=True, exist_ok=True)
    with open(download_path, "wb") as out_file:
        out_file.write(response.content)
    logging.debug(f"Written to file '{download_path}'")
    setattr(context["data_collection_pipeline_status"].builds[build.uuid], download_spec.dict_key, download_path)
    if download_spec.dict_key in {"log_path", "archive_path"}:
        context["data_collection_pipeline_status"].builds[build.uuid].log_url = url
    logging.debug(f"Leaving marker '{cached_marker_path}'")
    cached_marker_path.touch()


def download_log(build: ZuulBuild, context: ContextType) -> None:
    """Download testlogs from Zuul.
    Creates the download spec to download the manifest file of a single build.
    If the logs are zipped use the archive else use the text file.
    Parameters
    ----------
    build: ZuulBuild
        The build for which the test logs should be downloaded.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    if context["data_collection_pipeline_status"].builds[build.uuid].has_archive:
        download_spec = DownloadSpec(
            file_name=BAZEL_LOGS_NAME,
            content_type=ContentType.TAR,
            cache_prefix=CachePrefixType.ARCHIVE,
        )
    elif context["data_collection_pipeline_status"].builds[build.uuid].has_testlog:
        download_spec = DownloadSpec(
            file_name=TEST_LOGS_NAME,
            content_type=ContentType.TEXT,
            cache_prefix=CachePrefixType.TESTLOG,
        )
    else:
        logging.warning("Download log impossible for this ZuulBuild")
        return
    download_generic_zuul_content(build, context, download_spec)


def parse_manifest(build: ZuulBuild, context: ContextType) -> None:
    """Parses the build manifest.
    Parses the manifest specified in the context. Depending on the
    available files certain flags are set, to modify future behaviour
    of the pipeline.
    Parameters
    ----------
    build: ZuulBuild
        The build for which the manifest should be parsed.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    manifest_path = context["data_collection_pipeline_status"].builds[build.uuid].manifest_path

    if not manifest_path or not manifest_path.is_file():
        logging.warning(f"Manifest json file '{manifest_path}' not found")
        return

    with open(manifest_path, "r") as manifest:
        try:
            manifest_data = json.load(manifest)
        except json.JSONDecodeError as exception:
            logging.warning(f"manifest.json for build '{build.uuid}' created the following exception {exception.msg}")
            return
        for item in manifest_data["tree"]:
            # Initialize all attributes
            if item["name"] == BAZEL_LOGS_NAME:
                context["data_collection_pipeline_status"].builds[build.uuid].has_archive = True
            elif item["name"] == TEST_LOGS_NAME:
                context["data_collection_pipeline_status"].builds[build.uuid].has_testlog = True
            elif _RE_YAML_PATTERN.search(item["name"]):
                context["data_collection_pipeline_status"].builds[build.uuid].has_yaml = True
                context["data_collection_pipeline_status"].builds[build.uuid].yaml_name = item["name"]
            elif item["name"] == JOB_OUTPUT_NAME:
                context["data_collection_pipeline_status"].builds[build.uuid].has_job_output = True


def download_manifest(build: ZuulBuild, context: ContextType) -> None:
    """Download manifest file from Zuul.
    Creates the download spec to download the manifest file of a single build.
    Parameters
    ----------
    build: ZuulBuild
        The build for which the manifest should be downloaded.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    download_spec = DownloadSpec(
        file_name=ZUUL_MANIFEST_NAME,
        content_type=ContentType.JSON,
        cache_prefix=CachePrefixType.MANIFEST,
    )
    download_generic_zuul_content(build, context, download_spec)
