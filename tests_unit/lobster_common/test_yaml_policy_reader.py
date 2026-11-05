# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import re
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import main, TestCase

from lobster.common.exceptions import LOBSTER_Exception
from lobster.common.raw_policy import RawPolicy
from lobster.common.yaml_policy_reader import read_yaml_policy


class ReadYamlPolicyTest(TestCase):
    def test_reads_policy_levels_and_locations(self):
        """Read policy levels and retain their source locations."""
        # lobster-trace: core_report_req.Yaml_Policy_Reader_Reads_Levels
        # GIVEN a YAML policy with populated and omitted optional fields
        with TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "policy.yaml"
            filename.write_text(
                """levels:
  - name: Animals
    kind: requirements
    source:
      - some-path
    trace-to:
      - implementation
    requires:
      - [cave, nest]
  - name: Plants
    kind: implementation
""",
                encoding="UTF-8",
            )

            # WHEN the policy is read
            policy = read_yaml_policy(str(filename))

        # THEN all levels, fields, defaults, and source locations are preserved
        self.assertIsInstance(policy, RawPolicy)
        self.assertEqual(len(policy.levels), 2)

        animals, plants = policy.levels
        self.assertEqual(animals.name, "Animals")
        self.assertEqual(animals.kind, "requirements")
        self.assertEqual(
            [source.file for source in animals.source],
            ["some-path"],
        )
        self.assertEqual(
            [target.target for target in animals.trace_to],
            ["implementation"],
        )
        self.assertEqual(
            [[candidate.name for candidate in group]
             for group in animals.requires],
            [["cave", "nest"]],
        )
        self.assertEqual(animals.name_loc.to_string(), str(filename))
        self.assertEqual(animals.source[0].loc.to_string(), str(filename))
        self.assertEqual(animals.trace_to[0].loc.to_string(), str(filename))
        self.assertEqual(
            animals.requires[0][0].loc.to_string(), str(filename)
        )

        self.assertEqual(plants.name, "Plants")
        self.assertEqual(plants.kind, "implementation")
        self.assertEqual(plants.source, [])
        self.assertEqual(plants.trace_to, [])
        self.assertEqual(plants.requires, [])

    def test_empty_optional_keys_are_empty_lists(self):
        """Treat optional keys without a value like omitted keys."""
        # lobster-trace: core_report_req.Yaml_Policy_Reader_Reads_Levels
        # GIVEN a level whose optional keys have no value
        with TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "policy.yaml"
            filename.write_text(
                "levels:\n"
                "  - name: A\n"
                "    kind: requirements\n"
                "    source:\n"
                "    trace-to:\n"
                "    requires:\n",
                encoding="UTF-8",
            )

            # WHEN the policy is read
            policy = read_yaml_policy(str(filename))

        # THEN the optional entries are empty
        level = policy.levels[0]
        self.assertEqual(level.source, [])
        self.assertEqual(level.trace_to, [])
        self.assertEqual(level.requires, [])

    def _read_invalid(self, content):
        with TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "policy.yaml"
            filename.write_text(content, encoding="UTF-8")
            with self.assertRaises(LOBSTER_Exception) as ctx:
                read_yaml_policy(str(filename))
        return str(filename), ctx.exception.message

    def test_schema_violation_reports_line(self):
        """Report the line of each schema violation."""
        # lobster-trace: core_report_req.Yaml_Policy_Reader_Reports_Invalid_Policy_With_Line
        # GIVEN a policy with an invalid kind and an unexpected key
        # WHEN the policy is read
        filename, message = self._read_invalid(
            "levels:\n"
            "  - name: A\n"
            "    kind: bogus\n"
            "  - name: B\n"
            "    kind: activity\n"
            "    foo: 1\n"
        )

        # THEN each problem is reported with its line
        self.assertIn(f"{filename}:3: invalid tracing policy", message)
        self.assertIn(f"{filename}:6: invalid tracing policy", message)

    def test_duplicate_key_is_rejected(self):
        """Reject a mapping key that appears twice."""
        # lobster-trace: core_report_req.Yaml_Policy_Reader_Reports_Invalid_Policy_With_Line
        # GIVEN a level with two "source" keys
        # WHEN the policy is read
        filename, message = self._read_invalid(
            "levels:\n"
            "  - name: A\n"
            "    kind: requirements\n"
            "    source: [a]\n"
            "    source: [b]\n"
        )

        # THEN the duplicate is reported with its line
        self.assertIn(f"{filename}:5: invalid tracing policy", message)
        self.assertIn("duplicate key 'source'", message)

    def test_empty_or_group_is_rejected(self):
        """Reject a "requires" OR-group without candidates."""
        # lobster-trace: core_report_req.Yaml_Policy_Reader_Reports_Invalid_Policy_With_Line
        # GIVEN a level with an empty OR-group
        # WHEN the policy is read
        filename, message = self._read_invalid(
            "levels:\n"
            "  - name: A\n"
            "    kind: requirements\n"
            "    requires:\n"
            "      - []\n"
        )

        # THEN the empty group is reported with its line
        self.assertIn(f"{filename}:5: invalid tracing policy", message)

    def test_missing_key_reports_enclosing_line(self):
        """Report the enclosing element's line for a missing key."""
        # lobster-trace: core_report_req.Yaml_Policy_Reader_Reports_Invalid_Policy_With_Line
        # GIVEN a level without a name
        # WHEN the policy is read
        filename, message = self._read_invalid(
            "levels:\n"
            "  - kind: activity\n"
        )

        # THEN the line of the level is reported
        self.assertIn(f"{filename}:2: invalid tracing policy", message)

    def test_malformed_yaml_reports_line(self):
        """Report the line of a YAML syntax error."""
        # lobster-trace: core_report_req.Yaml_Policy_Reader_Reports_Invalid_Policy_With_Line
        # GIVEN a policy with a YAML syntax error
        # WHEN the policy is read
        filename, message = self._read_invalid("levels: [\n  - a: b: c\n")

        # THEN a line is reported
        self.assertRegex(
            message, rf"^{re.escape(filename)}:\d+: invalid tracing policy")


if __name__ == "__main__":
    main()
