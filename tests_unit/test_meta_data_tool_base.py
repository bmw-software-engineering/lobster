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

from argparse import Namespace
from unittest import TestCase
from lobster.common.meta_data_tool_base import MetaDataToolBase


class CherryPineappleTool(MetaDataToolBase):
    def _run_impl(self, options: Namespace) -> int:
        return 0


class MetaDataToolBaseTest(TestCase):
    def setUp(self):
        self.tool = CherryPineappleTool(
            name="Knorrstraße",
            description="A test tool",
            official=True,
        )

    def test_name(self):
        self.assertEqual(self.tool.name, "lobster-Knorrstraße")
