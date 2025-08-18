
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Union

from lobster.tools.trlc.tag_entry import TagEntry


@dataclass
class ConversionRule:
    """Specifies how to convert TRLC Record_Objects to LOBSTER items."""

    def __init__(
            self,
            package: str,
            record_type: str,
            namespace: str,
            description_fields: Optional[Union[str, Iterable[str]]] = None,
            justification_up_fields: Optional[Union[str, Iterable[str]]] = None,
            justification_down_fields: Optional[Union[str, Iterable[str]]] = None,
            justification_global_fields: Optional[Union[str, Iterable[str]]] = None,
            tags: Optional[Iterable[Union[str, Dict[str, str]]]] = None,
            applies_to_derived_types: bool = True,
    ):
        self._record_type_name = record_type
        self._package_name = package
        self._lobster_namespace = namespace
        self._description_fields = self._as_string_list(description_fields)
        self._justification_up_fields = self._as_string_list(justification_up_fields)
        self._justification_down_fields = self._as_string_list(
            justification_down_fields)
        self._justification_global_fields = self._as_string_list(
            justification_global_fields)
        self._tags = self._as_tag_list(tags)
        self._applies_to_derived_types = applies_to_derived_types

    def __hash__(self) -> int:
        return id(self)

    @property
    def type_name(self) -> str:
        return self._record_type_name

    @property
    def package_name(self) -> str:
        return self._package_name

    @property
    def applies_to_derived_types(self) -> bool:
        return self._applies_to_derived_types

    @property
    def lobster_namespace(self) -> str:
        return self._lobster_namespace

    @staticmethod
    def _as_string_list(value: Optional[Union[str, Iterable[str]]]) -> List[str]:
        if value is None:
            return []
        elif isinstance(value, str):
            return [value]
        elif isinstance(value, list):
            return value
        else:
            raise ValueError(f"Expected str or list, got {type(value)}")

    @staticmethod
    def _as_tag_list(
        tags: Optional[Iterable[Union[str, Dict[str, str]]]],
    ) -> List[TagEntry]:
        result = []
        if tags is not None:
            for tag in tags:
                if isinstance(tag, str):
                    result.append(TagEntry(field=tag))
                elif isinstance(tag, dict):
                    result.append(TagEntry(**tag))
                else:
                    raise ValueError(f"Expected str or dict, got {type(tag)}")
        return result

    @property
    def tags(self) -> List[TagEntry]:
        return self._tags

    @property
    def description_fields(self) -> List[str]:
        return self._description_fields

    @property
    def justification_up_fields(self) -> List[str]:
        return self._justification_up_fields

    @property
    def justification_down_fields(self) -> List[str]:
        return self._justification_down_fields

    @property
    def justification_global_fields(self) -> List[str]:
        return self._justification_global_fields
