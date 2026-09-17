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

from pathlib import Path
from unittest import TestCase

from tests_unit.lobster_trlc.trlc_data_provider import TrlcDataProvider


__unittest = True


class TrlcOptionalFieldTestCase(TestCase):

    PACKAGE_NAME = "optional_field_test"

    def setUp(self) -> None:
        self._trlc_data_provider = TrlcDataProvider(
            callback_test_case=self,
            trlc_input_files=[
                Path(__file__).parent / "data" / "optional_field_test.rsl",
                Path(__file__).parent / "data" / "optional_field_test.trlc",
            ],
            expected_record_object_names={
                "A",
                "B",
                "C",
            },
        )
        super().setUp()
