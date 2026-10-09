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

import unittest

from lobster.tools.trlc.item_wrapper import ItemWrapper
from lobster.tools.trlc.errors import RecordObjectComponentError
from tests_unit.lobster_trlc.test_to_string_rules import TrlcToStringDataTestCase


class ItemWrapperTest(TrlcToStringDataTestCase):
    def test_get_field_existing(self):
        # lobster-trace: trlc_req.Item_Wrapper_Reads_Existing_Fields

        def assert_field_matches_record(item_wrapper, record_object, field_name):
            raw_field = record_object.field[field_name]
            self.assertEqual(
                item_wrapper.get_field(field_name),
                record_object.to_python_dict()[field_name],
            )
            self.assertIs(item_wrapper.get_field_raw(field_name), raw_field)
            self.assertEqual(
                item_wrapper.get_field_value_or_none(field_name),
                raw_field.to_python_object(),
            )

        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("fast_boat", "large_boat"):
                assert_field_matches_record(item_wrapper, record_object, field_name)
            if record_object.name == "TONY":
                self.assertIsNone(item_wrapper.get_field("berthed_ships"))
                self.assertIsNone(item_wrapper.get_field_value_or_none("berthed_ships"))
                # the raw field should still exist, even if the value is None
                self.assertIsNotNone(item_wrapper.get_field_raw("berthed_ships"))
            else:
                assert_field_matches_record(item_wrapper, record_object, "berthed_ships")

    def test_get_field_non_existing(self):
        # lobster-trace: trlc_req.Item_Wrapper_Missing_Field_Behavior
        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            with self.assertRaises(RecordObjectComponentError):
                item_wrapper.get_field("non_existing_field")
            with self.assertRaises(RecordObjectComponentError):
                item_wrapper.get_field_raw("non_existing_field")
            self.assertIsNone(item_wrapper.get_field_value_or_none("non_existing_field"))


if __name__ == "__main__":
    unittest.main()
