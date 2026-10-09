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

from unittest import TestCase
import unittest

from lobster.common.file_collector import FileCollector


class FileCollectorTest(TestCase):
    def test_empty_extensions_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            FileCollector(extensions=[], directory_exclude_patterns=[])
        self.assertEqual(
            str(context.exception), "'extensions' must not be empty"
        )


if __name__ == '__main__':
    unittest.main()
