from dataclasses import dataclass


@dataclass
class TagEntry:
    field: str
    namespace: str = 'req'
