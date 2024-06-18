from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Tuple

from .datatypes import PipelineType, ZuulJobConfiguration


@dataclass
class DataCollectionPipelineConfig:
    # Disabled since there are too many attributes of DataCollectionPipelineConfig
    # pylint: disable=too-many-instance-attributes
    """This class is used to configure the data collection pipeline."""

    zuul_auth_pair: Tuple[str, str] = ("", "")
    zuul_url: str = ""
    number_of_last_builds: int = 0
    branch: str = ""
    output_directory: Path = ""
    enable_caching: bool = (False,)
    zuul_job: ZuulJobConfiguration = ZuulJobConfiguration("", PipelineType.UNKNOWN)
    keep_artifacts: bool = False
    max_log_length: int = 100
    collect_issues: bool = False
    detect_reruns: bool = False
    gate_to_merge_time: timedelta = timedelta(minutes=600)
    merge_to_post_time: timedelta = timedelta(minutes=240)
