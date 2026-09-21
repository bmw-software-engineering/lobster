# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
from lobster.common.file_tag_generator import FileTagGenerator


class FileTagGeneratorTest(TestCase):
    def setUp(self):
        self.generator = FileTagGenerator()

    def test_unique_tags(self):
        basename = "file.txt"
        tag1 = self.generator.get_tag(f"/path/to/{basename}")
        tag2 = self.generator.get_tag(f"/another/path/to/{basename}")
        self.assertEqual(tag1, f"{basename}:1")
        self.assertEqual(tag2, f"{basename}:2")

    def test_same_file_same_tag(self):
        path = "/path/to/file.abc"
        tag1 = self.generator.get_tag(path)
        tag2 = self.generator.get_tag(path)
        self.assertEqual(tag1, tag2)

    def test_basename_only(self):
        file = "document.abc"
        tag1 = self.generator.get_tag(file)
        self.assertEqual(tag1, f"{file}:1")

    def test_pathlib_integration(self):
        gen = FileTagGenerator()

        tag1 = gen.get_tag("/tmp/file.txt")
        tag2 = gen.get_tag("/another/path/file.txt")

        self.assertEqual(tag1, "file.txt:1")
        self.assertEqual(tag2, "file.txt:2")

    def test_tag_with_plain_filename(self):
        gen = FileTagGenerator()

        tag = gen.get_tag("file.txt")
        self.assertEqual(tag, "file.txt:1")
