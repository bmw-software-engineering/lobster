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

import sys
from unittest import TestCase
from lobster.common.location import Codebeamer_Reference

class CodebeamerReferenceTests(TestCase):
    _CB_ROOT = "http://turtle:123456789"

    def test_codebeamer_reference_to_html(self):
        for name in (None, "pelican"):
            for version in (None, 44):
                with self.subTest(name=name, version=version):
                    cb_ref = Codebeamer_Reference(
                        cb_root=self._CB_ROOT,
                        tracker=42,
                        item=43,
                        version=version,
                        name=name,
                    )
                    version_addon = f"?version={version}" if version else ""
                    expected_html = f'<a href="{self._CB_ROOT}/issue/{cb_ref.item}' \
                        f'{version_addon}" target="_blank">{cb_ref.to_string()}</a>'
                    self.assertEqual(expected_html, cb_ref.to_html())

    def test_codebeamer_reference_to_string(self):
        for name in (None, "duck"):
            for item in (1, 45, sys.maxsize):
                with self.subTest(name=name, item=item):
                    cb_ref = Codebeamer_Reference(
                        cb_root=self._CB_ROOT,
                        tracker=44,
                        item=item,
                        version=46,
                        name=name,
                    )
                    expected_string = f"cb item {cb_ref.item}"
                    if name:
                        expected_string += f" '{name}'"
                    self.assertEqual(expected_string, cb_ref.to_string())

    def test_codebeamer_reference_sorting_key(self):
        cb_ref = Codebeamer_Reference(
            cb_root=self._CB_ROOT,
            tracker=47,
            item=48,
        )
        expected_key = (self._CB_ROOT, cb_ref.tracker, cb_ref.item)
        self.assertEqual(expected_key, cb_ref.sorting_key())
