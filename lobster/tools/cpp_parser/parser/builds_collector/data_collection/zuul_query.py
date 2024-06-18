from typing import List

import pydantic
import requests

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildPaths,
    ContextType,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.event_logger import logging
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import (
    RequestParams,
    ZuulBuild,
)


def zuul_query(context: ContextType) -> List[ZuulBuild]:
    """Queries Zuul for builds.
    Queries the URL specified in the context and tries to parse the result
    as list of ZuulBuilds.
    The request uses three parameters from the context to restrict the builds:
    - limit: The number of builds to consider
    - job_name: The Zuul job.
    - branch: The branch of the repository.
    Parameters
    ----------
    context: ContextType
        Context dictionary containing metadata of the process.
    Returns
    -------
    builds: List[ZuulBuild]
        The list of parsed builds from Zuul.
    """
    request_params = {
        "limit": context["data_collection_pipeline_config"].number_of_last_builds,
        "job_name": context["data_collection_pipeline_config"].zuul_job.job,
        "branch": context["data_collection_pipeline_config"].branch,
        "pipeline": context["data_collection_pipeline_config"].zuul_job.pipeline.value,
    }
    auth = context["data_collection_pipeline_config"].zuul_auth_pair
    zuul_url = context["data_collection_pipeline_config"].zuul_url
    logging.debug(f"Sending request to '{zuul_url}'")

    retry_strategy = requests.packages.urllib3.util.retry.Retry(
        total=3, status_forcelist=[429, 500, 502, 503, 504], method_whitelist=["GET"]
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
    https = requests.Session()
    https.mount("https://", adapter)
    response = https.get(zuul_url, auth=auth, params=RequestParams(**request_params).dict())
    logging.debug(f"Response code {response.status_code}")

    if response.status_code != requests.codes.ok:
        logging.warning(f"Request not ok")
        return []
    if "application/json" not in response.headers["Content-Type"]:
        logging.warning(f"Check authentication")
        return []

    list_of_builds = _parse_response(response)

    for build in list_of_builds:
        if build.uuid not in context["data_collection_pipeline_status"].builds.keys():
            context["data_collection_pipeline_status"].builds[build.uuid] = BuildPaths()

    return list_of_builds


def _parse_response(response: requests.Response) -> List[ZuulBuild]:
    """Parses the respone to a list of ZuulBuilds.
    Tries to parse the response as list of queries.
    Sometimes builds have invalid (meta)data and can not be parsed directly.
    In this case builds are parsed individually.
    Parameters
    ----------
    context: ContextType
        Context dictionary containing metadata of the process.
    Returns
    -------
    builds: List[ZuulBuild]
        The list of parsed builds from Zuul.
    """
    response_json = response.json()
    try:
        builds = pydantic.parse_obj_as(List[ZuulBuild], response_json)
    except pydantic.ValidationError as err_builds:
        logging.info("Some builds do not fit the scheme! Falling back to individual processing.")
        logging.debug(f"pydantic error:\n{str(err_builds)}")
        builds = []
        invalid_builds = []
        for item in response_json:
            try:
                build = ZuulBuild.parse_obj(item)
                builds.append(build)
            except pydantic.ValidationError as err_build:
                bld = item["uuid"]
                logging.debug(f"Build {bld} is invalid. pydantic error:\n{str(err_build)}")
                invalid_builds.append(bld)
        if len(invalid_builds) > len(builds) / 2:
            logging.warning("Most of the builds are invalid. You might want to investigate.")
    if len(builds) == 0:
        logging.warning("No valid Builds detected!")
    logging.debug(f"Zuul query returned {len(builds)} parsed Zuulbuilds")
    return builds
