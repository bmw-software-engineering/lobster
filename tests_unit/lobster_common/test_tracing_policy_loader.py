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

import io
from contextlib import redirect_stdout
from unittest import main, TestCase
from unittest.mock import MagicMock, patch

from lobster.common.tracing_policy_loader import load_tracing_policy

MODULE = "lobster.common.tracing_policy_loader"


class LoadTracingPolicyTest(TestCase):
    def test_yaml_extensions_use_yaml_reader(self):
        """Use the YAML reader for .yaml and .yml files, case-insensitively."""

        extensions = (".yaml", ".YAML", ".yAml", ".yml", ".YML", ".yMl")
        for extension in extensions:
            filename = f"policy{extension}"
            with self.subTest(filename=filename):
                # GIVEN mocked reader, legacy parser and builder
                with patch(f"{MODULE}.read_yaml_policy") as read_yaml, \
                        patch(f"{MODULE}.Parser") as parser, \
                        patch(f"{MODULE}.build_tracing_policy") as build:
                    mh = MagicMock()
                    stdout = io.StringIO()

                    # WHEN the policy is loaded
                    with redirect_stdout(stdout):
                        result = load_tracing_policy(mh, filename)

                    # THEN the YAML reader result is built and returned
                    read_yaml.assert_called_once_with(filename)
                    parser.assert_not_called()
                    build.assert_called_once_with(read_yaml.return_value)
                    self.assertIs(result, build.return_value)
                    # AND no deprecation warning is printed
                    self.assertEqual(stdout.getvalue(), "")

    def test_other_extensions_use_legacy_parser_with_warning(self):
        """Use the legacy parser and warn for non-YAML files."""
        # GIVEN mocked reader, legacy parser and builder
        with patch(f"{MODULE}.read_yaml_policy") as read_yaml, \
                patch(f"{MODULE}.Parser") as parser, \
                patch(f"{MODULE}.build_tracing_policy") as build:
            mh = MagicMock()
            stdout = io.StringIO()

            # WHEN a legacy policy is loaded
            with redirect_stdout(stdout):
                result = load_tracing_policy(mh, "policy.conf")

            # THEN the legacy parser result is built and returned
            read_yaml.assert_not_called()
            parser.assert_called_once_with(mh, "policy.conf")
            build.assert_called_once_with(parser.return_value.parse.return_value)
            self.assertIs(result, build.return_value)
            # AND a deprecation warning is printed
            self.assertIn("policy.conf: warning:", stdout.getvalue())
            self.assertIn("deprecated", stdout.getvalue())


if __name__ == "__main__":
    main()
