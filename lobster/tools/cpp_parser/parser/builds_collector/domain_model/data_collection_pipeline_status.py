from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Tuple

from .datatypes import BuildPaths


@dataclass
class DataCollectionPipelineStatus:
    """This class is used to store the results of the data collection pipeline."""

    build_metadata_pickle_path: str = ""
    narrow_df_pickle_path: str = ""
    wide_df_pickle_path: str = ""
    test_output_txt_path: Path = ""
    issues_path: Tuple[str, str] = None
    builds: Dict[str, BuildPaths] = field(default_factory=lambda: {})
