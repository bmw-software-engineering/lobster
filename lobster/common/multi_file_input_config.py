from dataclasses import dataclass
from typing import Iterable, Optional, Type, Union
from re import Pattern

from lobster.common.items import Activity, Implementation, Requirement


@dataclass
class Config:
    inputs: Optional[Iterable[str]]
    inputs_from_file: Optional[str]
    extensions: Iterable[str]
    exclude_patterns: Optional[Iterable[Pattern]]
    schema: Union[Type[Requirement], Type[Implementation], Type[Activity]]
