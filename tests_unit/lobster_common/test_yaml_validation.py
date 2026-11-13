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
from unittest import main, TestCase
from unittest.mock import patch

from lobster.common.yaml_validation import validate_yaml_file


class ValidateYamlFileTest(TestCase):
    @patch("lobster.common.yaml_validation.yamale.validate")
    @patch("lobster.common.yaml_validation.yamale.make_schema")
    def test_validates_data_against_schema(self, make_schema, validate):
        """Test that the UTF-8 file content is validated against the loaded schema."""
        # lobster-trace: core_report_req.Yaml_Validation_Validates_File_Against_Schema
        schema_file = "schema.yamale"
        make_schema.return_value = object()

        with TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "file.yaml"
            filename.write_text("name: Grüße\n", encoding="UTF-8")

            validate_yaml_file(schema_file, str(filename))

            expected = [({"name": "Grüße"}, str(filename.resolve()))]

        make_schema.assert_called_once_with(schema_file)
        validate.assert_called_once_with(make_schema.return_value, expected)


if __name__ == "__main__":
    main()
