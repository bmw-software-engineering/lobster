import json
from typing import Dict, List

import pandas as pd

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    BuildMetadata,
    BuildUuid,
    ContextType,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.mapping import BuildMetadataMapping
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild


def _update_with_cache(df_narrow: pd.DataFrame, context: ContextType) -> pd.DataFrame:
    """Updates dataframe with cache from storage.

    Gets the cached dataframe from storage and appends the entries for build which
    are also cached. The resulting dataframe gets written back to storage.

    Parameters
    ----------
    df_narrow: pd.Dataframe
        The current dataframe.
    context: ContextType
        Context dictionary containing metadata of the process.

    Returns
    -------
    pd.DataFrame
        The synchronized dataframe.
    """
    storage = context["storage"]
    table_name = get_table_name_from_context(context)
    df_narrow_cached = storage.read_dataframe(table_name)
    cached_builds = [mapping.uuid for mapping in get_cached_builds(context)]
    if df_narrow_cached is not None:
        df_narrow_cached = df_narrow_cached[df_narrow_cached["uuid"].isin(cached_builds)]
        df_narrow = df_narrow.append(df_narrow_cached)
    df_narrow.drop_duplicates(inplace=True, subset=df_narrow.columns.difference(["error_log"]))
    df_narrow.reset_index(inplace=True, drop=True)
    storage.write_dataframe(table_name, df_narrow)
    return df_narrow


def set_cached_in_builds(builds: List[ZuulBuild], context: ContextType) -> None:
    """Sets the cached parameter in the builds list
    Updates the cached parameter for each build we have in storage.
    Each build has to be stored in the dataframe and buildmetadata cache
    to be updated.
    If this is not the case the pipeline did not succeed for this build.
    Parameters
    ----------
    builds: List[ZuulBuild]
        The builds we want to check.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    table_name = get_table_name_from_context(context)
    storage = context["storage"]
    df_narrow_cached = storage.read_dataframe(table_name)
    if df_narrow_cached is None:
        return
    cached_uuids = df_narrow_cached["uuid"].unique()
    cached_builds = get_cached_builds(context)
    cached_builds = [cached_build.uuid for cached_build in cached_builds]
    for build in builds:
        build.cached = bool(build.uuid in cached_uuids and build.uuid in cached_builds)


def get_cached_builds(context: ContextType) -> List[BuildMetadataMapping]:
    """Gets the cached BuildMetadata from storage.
    Returns all mappings according to the branch and job_name given in the context.
    Parameters
    ----------
    context: ContextType
        Context dictionary containing metadata of the process.
    Returns
    -------
    cached_builds: List[BuildMetadataMapping]
        The cached builds according to the database.
    """
    storage = context["storage"]
    branch = context["data_collection_pipeline_config"].branch
    job_name = context["data_collection_pipeline_config"].zuul_job.job
    criteria = [
        BuildMetadataMapping.branch == branch,
        BuildMetadataMapping.job_name == job_name,
    ]
    cached_builds = storage.get_mappings(BuildMetadataMapping, criteria)
    return cached_builds


def update_builds_cache(build_metadata: Dict[BuildUuid, BuildMetadata], context: ContextType) -> None:
    """Updates the build_metadata cache in storage.
    Updates all mappings according to the branch and job_name given in the context.
    Existing once will be replace, new ones added.
    Parameters
    ----------
    build_metadata: Dict[BuildUuid, BuildMetadata]
        The build metadata which should be cached.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    storage = context["storage"]
    branch = context["data_collection_pipeline_config"].branch
    job_name = context["data_collection_pipeline_config"].zuul_job.job
    criteria = [
        BuildMetadataMapping.branch == branch,
        BuildMetadataMapping.job_name == job_name,
    ]
    storage.delete_mappings(BuildMetadataMapping, criteria)
    builds = [
        BuildMetadataMapping(
            uuid=uuid,
            branch=branch,
            job_name=job_name,
            pr_url=build.pr_url,
            start_time=build.start_time,
            githash=json.dumps(build.githash),
            ci_result=build.ci_result.name,
        )
        for uuid, build in build_metadata.items()
    ]
    storage.update_mappings(BuildMetadataMapping, builds)


def get_table_name_from_context(context: ContextType) -> str:
    """Gets the dataframe table name according to the context.
    Parameters
    ----------
    context: ContextType
        Context dictionary containing metadata of the process.
    Returns
    -------
    str
        The dataframe table name.
    """
    branch = context["data_collection_pipeline_config"].branch
    job_name = context["data_collection_pipeline_config"].zuul_job.job
    return f"df_narrow_{job_name}_{branch}"
