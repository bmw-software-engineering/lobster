# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

import yamale
import yaml

@dataclass
class TagEntry:
    field: str
    namespace: str = 'req'


@dataclass
class ExtractionInfo:
    def __init__(
            self,
            description_fields: Optional[Union[str, List[str]]] = None,
            justification_up_fields: Optional[Union[str, List[str]]] = None,
            justification_down_fields: Optional[Union[str, List[str]]] = None,
            justification_global_fields: Optional[Union[str, List[str]]] = None,
            tags: Optional[List[Union[str, Dict[str, str]]]] = None,
    ):
        self._description_fields = self._as_string_list(description_fields)
        self._justification_up_fields = self._as_string_list(justification_up_fields)
        self._justification_down_fields = self._as_string_list(justification_down_fields)
        self._justification_global_fields = self._as_string_list(justification_global_fields)
        self._tags = self._as_tag_list(tags)

    @staticmethod
    def _as_string_list(value: Optional[Union[str, List[str]]]) -> List[str]:
        if value is None:
            return []
        elif isinstance(value, str):
            return [value]
        elif isinstance(value, list):
            return value
        else:
            raise ValueError(f"Expected str or list, got {type(value)}")

    @staticmethod
    def _as_tag_list(tags: Optional[Iterable[Union[str, Dict[str, str]]]]) -> List[TagEntry]:
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


@dataclass
class Config:
    extractions: Dict[str, ExtractionInfo]
    to_string_rules: Dict[str, List[str]]

    def get_extraction_info(self, record_type_name: str) -> ExtractionInfo:
        return self.extractions[record_type_name]
    
    def get_to_string_rules(self, record_type_name: str) -> List[str]:
        return self.to_string_rules[record_type_name]

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        extractions = {}
        for d in data.get("extractions", []):
            for record_type_name, extraction_info_dict in d.items():
                extractions[record_type_name] = ExtractionInfo(**extraction_info_dict)

        return Config(
            extractions=extractions,
            to_string_rules=data.get("to_string_rules", {})
        )


def _validate_config(filename: str):
    schema_file = Path(__file__).parent / "schema.yamale"
    schema = yamale.make_schema(schema_file)
    data = yamale.make_data(filename)
    yamale.validate(schema, data)


def load_config(filename: str) -> Config:
    _validate_config(filename)

    with open(filename, "r", encoding="UTF-8") as f:
        config_data = yaml.safe_load(f)

    config = Config.from_dict(config_data)
    for k, v in config.extractions.items():
        #print(f"{k}: {v.description_fields=}, {v.justification_up_fields=}, {v.justification_down_fields=}, {v.justification_global_fields=}")
        print(f"{k}: {v.tags=}")

    return Config.from_dict(config_data)
