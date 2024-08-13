import datetime
import enum
from dataclasses import dataclass
from typing import Any, Dict, NamedTuple, Optional

BuildUuid = str

ContextType = Dict[str, Any]


class BuildSortOrder(enum.Enum):
    """This class is used to determine the order in which Zuul builds shall be sorted"""

    BY_START_TIME = 0
    BY_MERGE_TIME = 1


class PullRequestState(enum.Enum):
    """This class is used to represent merge state of Pull Requests"""

    UNKNOWN = 0
    MERGED = 1
    OPEN = 2
    CLOSED = 4
    NOT_MERGED = 6  # Only needed for as long as we cannot distinguish between open and closed PRs


class PullRequestInfo(NamedTuple):
    """This class is used to represent the state of Pull Requests including their merge time of it, if any"""

    state: PullRequestState
    merge_time: Optional[datetime.datetime] = None


class BuildResult(str, enum.Enum):
    """Enum class used to determine build result.

    Those results are defined by Zuul, except for RERUN which is an additional classification that (potentially) overrides the Zuul build result.
    """

    FAILURE = "FAILURE"
    POST_FAILURE = "POST_FAILURE"
    RETRY = "RETRY"
    RETRY_LIMIT = "RETRY_LIMIT"
    SUCCESS = "SUCCESS"
    TIMED_OUT = "TIMED_OUT"
    ABORTED = "ABORTED"
    CANCELED = "CANCELED"
    RERUN = "RERUN"
    SKIPPED = "SKIPPED"


class BuildMetadata(NamedTuple):
    """This class is used as metadata for builds"""

    pr_url: str
    sort_time: datetime.datetime
    start_time: datetime.datetime
    githash: Dict[str, str]
    ci_result: BuildResult
    pr_info: PullRequestInfo
    pipeline: str


class MergeTimeTolerance(NamedTuple):
    """This class is used to aggregate merging PRs' pipeline transition time"""

    gate_to_merge: datetime.timedelta
    merge_to_post: datetime.timedelta


class ContentType(str, enum.Enum):
    """Enum class used to represent whether the type of the downloaded content is text, json or tar"""

    TEXT = "text/plain"
    JSON = "application/json"
    TAR = "application/x-tar"


class CachePrefixType(str, enum.Enum):
    """Enum class used to represent whether the cache prefix is archive, manifest. adpbuild_yaml or job_output"""

    ARCHIVE = "archive"
    TESTLOG = "testlog"
    MANIFEST = "manifest"
    ADPBUILD = "adpbuild_yaml"
    JOB_OUTPUT = "job_output"


class DownloadSpec(NamedTuple):
    """This class is used to download various elements, e.g. manifests."""

    file_name: str
    content_type: ContentType
    cache_prefix: CachePrefixType

    @property
    def dict_key(self) -> str:
        """
        Returns
        -------
        str
            Dict_key string depending on the cache_prefix attribute
        """
        if self.cache_prefix == CachePrefixType.TESTLOG:
            return "log_path"
        if self.cache_prefix == CachePrefixType.ADPBUILD:
            return "yaml_path"
        if self.cache_prefix in [CachePrefixType.ARCHIVE, CachePrefixType.MANIFEST, CachePrefixType.JOB_OUTPUT]:
            return f"{self.cache_prefix.value}_path"
        return ""


class LogInfo(NamedTuple):
    """This class represents Zuul test logs"""

    log: str
    url: str
    line: int


@dataclass
class BuildPaths:
    # Disabled since there are too many attributes of BuildPaths
    # pylint: disable=too-many-instance-attributes
    """Used to determine the zuul build paths from the Zuul Manifest."""

    json_path: str = None
    archive_path: str = None
    log_path: str = None
    manifest_path: str = None
    yaml_path: str = None
    job_output_path: str = None
    log_url: str = None
    has_archive: bool = False
    has_testlog: bool = False
    has_yaml: bool = False
    has_job_output: bool = False
    yaml_name: str = None


class PipelineType(str, enum.Enum):
    """Enum class used to represent the pipeline type"""

    GATE = "gate"
    PREGATE = "pregate"
    POST_INDEPENDENT = "post-independent"
    PERIODIC_CHECK_0 = "periodic_check_0"
    PERIODIC_CHECK_1 = "periodic_check_1"
    MANUAL_POST = "manual-post"
    TEST = "test"
    UNKNOWN = ""


class ProjectName(str, enum.Enum):
    """
    Enum class used to represent the different projects of Zuul Builds
    If a project is not in this Enum, all builds regarding this project will be excluded from builds_collector analysis
    """

    ADP = "swh/adp"
    ASTAS = "swh/astas"
    BOARDNET = "swh/boardnet"
    CVC = "swh/cvc"
    DDAD = "swh/ddad"
    DDAD_CI_CONFIG = "swh/ddad_ci_config"
    DDAD_PLATFORM = "swh/ddad_platform"
    DEPLOYMENT = "swh/deployment"
    FKR = "swh/fkr"
    FORESIGHT = "swh/foresight"
    GNSS_COMMON = "swh/gnss_common"
    IB_VIP = "swh/ib-vip"
    LTF_DLT = "swh/ltf_dlt"
    ORION_AEB = "swh/orion_aeb_temp"
    QDM = "swh/qdm"
    SYSTEM_DESCRIPTION = "swh/system_description"
    UFM = "swh/ufm"
    VDM = "swh/vdm"
    XPAD_ARA = "swh/xpad-ara"
    XPAD_SHARED = "swh/xpad-shared"
    XPAD_XPC = "swh/xpad-xpc"
    ZUUL_TRUSTED_DDAD = "swh/zuul-trusted-ddad"


class ZuulJobConfiguration(NamedTuple):
    """This class id used to define which pipeline of a job will be investigated by builds_collector"""

    job: str
    pipeline: PipelineType
