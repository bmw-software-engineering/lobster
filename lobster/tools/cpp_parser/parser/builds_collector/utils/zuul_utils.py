import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pydantic

from ..domain_model.datatypes import BuildResult, BuildUuid, PipelineType, ProjectName


class RequestParams(pydantic.BaseModel):
    """This class is responsible for holding request parameters.

    Mostly used when making requests to zuul.
    """

    uuid: Optional[BuildUuid] = None
    job_name: Optional[str] = None
    result: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[float] = None
    voting: Optional[bool] = None
    log_url: Optional[str] = None
    node_name: Optional[str] = None
    error_detail: Optional[str] = None
    final: bool = True
    project: Optional[str] = None
    branch: Optional[str] = None
    pipeline: Optional[str] = None
    change: Optional[int] = None
    patchset: Optional[str] = None
    ref: Optional[str] = None
    newrev: Optional[str] = None
    ref_url: Optional[str] = None
    event_id: Optional[str] = None
    limit: int = 100


class ZuulBuildMetadata(pydantic.BaseModel):
    """This class holds metadata for zuul build"""

    type: str = "zuul_manifest"  ## TODO: Replace with enum


class ZuulBuildArtifact(pydantic.BaseModel):
    """This class preserves zuul build info"""

    name: str  ## TODO: Replace with enum
    url: pydantic.HttpUrl
    metadata: ZuulBuildMetadata


class ZuulBuildSet(pydantic.BaseModel):
    """This class is represents UUID for Zuul Buildset"""

    uuid: BuildUuid


class ZuulBuild(pydantic.BaseModel):
    """This class represents Zuul Build data"""

    uuid: BuildUuid
    job_name: str  ## TODO: Replace with enum.
    result: BuildResult
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: float
    voting: bool
    log_url: Optional[pydantic.AnyHttpUrl]
    error_detail: Optional[str]
    final: bool
    artifacts: List[ZuulBuildArtifact] = []
    provides: List[Any] = []  ## TODO: check possible list entry types
    project: ProjectName
    branch: str
    pipeline: PipelineType
    change: int
    patchset: str
    ref: Path
    newrev: Optional[str]
    ref_url: pydantic.HttpUrl
    event_id: Optional[str]
    buildset: ZuulBuildSet
    githash: Dict[str, str] = dict()
    cached: Optional[bool]
