from lobster.tools.trlc.item_wrapper import ItemWrapper
from lobster.tools.trlc.errors import RecordObjectComponentError
from tests_unit.lobster_trlc.test_to_string_rules import TrlcToStringDataTestCase


class ItemWrapperTest(TrlcToStringDataTestCase):
    def test_get_field_existing(self):

        def assertFieldIsNotNone(item_wrapper: ItemWrapper, field_name: str):
            self.assertTrue(item_wrapper.get_field(field_name))
            self.assertTrue(item_wrapper.get_field_raw(field_name))

        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            for field_name in ("fast_boat", "fast_boat"):
                assertFieldIsNotNone(item_wrapper, field_name)
            if record_object.name == "TONY":
                self.assertIsNone(item_wrapper.get_field("berthed_ships"))
                # the raw field should still exist, even if the value is None
                self.assertIsNotNone(item_wrapper.get_field_raw("berthed_ships"))
            else:
                assertFieldIsNotNone(item_wrapper, "berthed_ships")

    def test_get_field_non_existing(self):
        for record_object in self._trlc_data_provider.get_record_objects():
            item_wrapper = ItemWrapper(record_object)
            with self.assertRaises(RecordObjectComponentError):
                item_wrapper.get_field("non_existing_field")
            with self.assertRaises(RecordObjectComponentError):
                item_wrapper.get_field_raw("non_existing_field")
