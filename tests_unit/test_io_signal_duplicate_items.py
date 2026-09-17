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

from typing import List
from unittest import TestCase
from unittest.mock import Mock
from lobster.common.errors import Message_Handler
from lobster.common.items import Tracing_Tag, Requirement
from lobster.common.io import signal_duplicate_items
from lobster.common.location import File_Reference

class SignalDuplicateItemsTest(TestCase):
    def setUp(self) -> None:
        self._mh = Mock(spec=Message_Handler)
        self._items = {}
        for pizza in ["Capricciosa", "Margherita", "Quattro Stagioni", "Pepperoni"]:
            req = Requirement(
                    Tracing_Tag("Pizza", pizza, "tomatoe"),
                    File_Reference("filename"),
                    "woodstove",
                    "delicious",
                    "name",
                )
            self._items[req.tag.key()] = req

    def _create_duplicates(self, source: List[Requirement], count) -> List[Requirement]:
        """
        Create a list of duplicate items based on the existing items.
        They use the same tracing tag, but a different location.
        The number of duplicates is determined by the count parameter.
        """
        if len(source) < count:
            self.fail("Count exceeds the number of available items.")

        duplicates = []
        for item in source[:count]:
            duplicate = Requirement(
                Tracing_Tag(item.tag.namespace, item.tag.tag, item.tag.version),
                File_Reference(f"{item.location.filename}-duplicated"),
                item.framework,
                item.kind,
                item.name,
            )
            duplicates.append(duplicate)
        return duplicates

    def test_no_duplicates(self):
        signal_duplicate_items(self._mh, self._items, [])
        self.assertEqual(self._mh.error.call_count, 0)

    def test_few_duplicates(self):
        num_duplicates = 2
        duplicate_items = self._create_duplicates(
            list(self._items.values()),
            num_duplicates,
        )

        signal_duplicate_items(self._mh, self._items, duplicate_items)

        self.assertEqual(self._mh.error.call_count, num_duplicates)

        for i, call in enumerate(self._mh.error.call_args_list[:-1]):
            self.assertFalse(
                call.kwargs.get("fatal", False),
                f"Call #{i + 1} did not use fatal=False",
            )
            duplicated_key = duplicate_items[i].tag.key()
            self.assertEqual(
                call.kwargs.get("message"),
                f"duplicate definition of {duplicated_key}, "
                f"previously defined at "
                f"{self._items[duplicated_key].location.to_string()}",
            )
            self.assertIs(duplicate_items[i].location, call.kwargs.get("location"))

        self.assertTrue(
            self._mh.error.call_args_list[-1].kwargs.get("fatal"),
            "Last call did not use fatal=True",
        )
