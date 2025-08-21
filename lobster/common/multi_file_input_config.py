from dataclasses import dataclass
from typing import Iterable, List, Type, Union
from re import Pattern

from lobster.common.items import Activity, Implementation, Requirement


@dataclass
class Config:
    inputs: str
    inputs_from_file: str
    extensions: Iterable[str]
    exclude_patterns: List[Pattern]
    schema: Union[Type[Requirement], Type[Implementation], Type[Activity]]
