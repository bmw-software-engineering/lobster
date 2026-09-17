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

from unittest import TestCase
from lobster.common.multi_file_input_tool import select_non_comment_parts


class LobsterToolUtilTest(TestCase):
    def test_select_non_comment_parts(self):
        input_text = [
            "This is a line.           ",
            "This is another line. # with a comment",
            "  # This is a full comment line",
            "Yet another line.",
            "",
            "  ",
            "#",
            "##",
            "Line with # two # comment separators"
        ]
        expected_output = [
            "This is a line.",
            "This is another line.",
            "Yet another line.",
            "Line with"
        ]
        result = select_non_comment_parts(input_text)
        self.assertEqual(result, expected_output)
