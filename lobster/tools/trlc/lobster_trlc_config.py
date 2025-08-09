from dataclasses import dataclass
from pathlib import Path
from typing import List

import yamale
import yaml

from lobster.items import Requirement
from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.to_string_rules import ToStringRules
from lobster.tool2_config import Config


@dataclass
class LobsterTrlcConfig(Config):
    conversion_rules: List[ConversionRule]
    to_string_rules: List[ToStringRules]

    @classmethod
    def from_dict(cls, data: dict) -> "LobsterTrlcConfig":
        conversion_rules = []
        for conversion_rule_dict in data.get("conversion-rules", []):
            conversion_rules.append(ConversionRule(**conversion_rule_dict))

        return LobsterTrlcConfig(
            conversion_rules=conversion_rules,
            to_string_rules=data.get("to-string-rules", {}),
            inputs=data.get("inputs", ""),
            inputs_from_file=data.get("inputs-from-file", ""),
            extensions=(".rsl", ".trlc"),
            exclude_patterns=data.get("exclude-patterns", []),
            schema=Requirement,
        )


def _validate_config(filename: str):
    schema_file = Path(__file__).parent / "schema.yamale"
    schema = yamale.make_schema(schema_file)
    data = yamale.make_data(filename)
    yamale.validate(schema, data)


def load_config(filename: str) -> LobsterTrlcConfig:
    _validate_config(filename)

    with open(filename, "r", encoding="UTF-8") as f:
        config_data = yaml.safe_load(f)

    return LobsterTrlcConfig.from_dict(config_data)
