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

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from lobster.common.raw_policy import RawPolicy
from lobster.common.yaml_policy_reader import read_yaml_policy


class ReadYamlPolicyTest(TestCase):
    def test_reads_policy_levels_and_locations(self):
        """Read policy levels and retain their source locations."""
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


if __name__ == "__main__":
    import unittest

    unittest.main()
