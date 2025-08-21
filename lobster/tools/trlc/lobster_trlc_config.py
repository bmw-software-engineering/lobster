from dataclasses import dataclass
from pathlib import Path
from typing import List

import yamale
import yaml

from lobster.common.items import Requirement
from lobster.common.multi_file_input_config import Config
from lobster.tools.trlc.conversion_rule import ConversionRule
from lobster.tools.trlc.to_string_rules import ToStringRules


@dataclass
class LobsterTrlcConfig(Config):
    conversion_rules: List[ConversionRule]
    to_string_rules: List[ToStringRules]

    @classmethod
    def from_dict(cls, data: dict) -> "LobsterTrlcConfig":
        conversion_rules = []
        for conversion_rule_dict in data.get("conversion-rules", []):
            # The YAML schema uses hyphens, but those are not valid Python identifiers.
            # Replace hyphens with underscores to create valid attribute names.
            conversion_rule_dict_updated = {
                key.replace("-", "_"): value
                for key, value in conversion_rule_dict.items()
            }
            conversion_rules.append(ConversionRule(**conversion_rule_dict_updated))

        return LobsterTrlcConfig(
            conversion_rules=conversion_rules,
            to_string_rules=[ToStringRules.from_dict(rules)
                             for rules in data.get("to-string-rules", [])],
            inputs=data.get("inputs", ""),
            inputs_from_file=data.get("inputs-from-file", ""),
            extensions=(".rsl", ".trlc"),
            exclude_patterns=data.get("exclude-patterns", []),
            schema=Requirement,
        )

    @staticmethod
    def _validate_config(filename: str):
        schema_file = Path(__file__).parent / "schema.yamale"
        schema = yamale.make_schema(schema_file)
        # Note: using 'resolve()' only for the purpose that yamale prints the full path
        # in its exception in case of validation errors.
        data = yamale.make_data(Path(filename).resolve())
        yamale.validate(schema, data)

    @classmethod
    def from_file(cls, filename: str) -> "LobsterTrlcConfig":
        cls._validate_config(filename)

        with open(filename, "r", encoding="UTF-8") as f:
            config_data = yaml.safe_load(f)

        return cls.from_dict(config_data)
