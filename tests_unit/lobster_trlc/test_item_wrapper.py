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

from lobster.tools.trlc.item_wrapper import ItemWrapper
from lobster.tools.trlc.errors import RecordObjectComponentError
from tests_unit.lobster_trlc.test_to_string_rules import TrlcToStringDataTestCase


class ItemWrapperTest(TrlcToStringDataTestCase):
    def test_get_field_existing(self):
        # lobster-trace: trlc_req.Item_Wrapper_Reads_Existing_Fields

        def assertFieldIsNotNone(item_wrapper: ItemWrapper, field_name: str):
            self.assertTrue(item_wrapper.get_field(field_name))
            self.assertTrue(item_wrapper.get_field_raw(field_name))
            self.assertTrue(item_wrapper.get_field_value_or_none(field_name))

        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("fast_boat", "fast_boat"):
                assertFieldIsNotNone(item_wrapper, field_name)
            if record_object.name == "TONY":
                self.assertIsNone(item_wrapper.get_field("berthed_ships"))
                self.assertIsNone(item_wrapper.get_field_value_or_none("berthed_ships"))
                # the raw field should still exist, even if the value is None
                self.assertIsNotNone(item_wrapper.get_field_raw("berthed_ships"))
            else:
                assertFieldIsNotNone(item_wrapper, "berthed_ships")

    def test_get_field_non_existing(self):
        # lobster-trace: trlc_req.Item_Wrapper_Missing_Field_Behavior
        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            with self.assertRaises(RecordObjectComponentError):
                item_wrapper.get_field("non_existing_field")
            with self.assertRaises(RecordObjectComponentError):
                item_wrapper.get_field_raw("non_existing_field")
            self.assertIsNone(item_wrapper.get_field_value_or_none("non_existing_field"))
