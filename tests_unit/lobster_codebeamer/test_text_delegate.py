import unittest
from unittest.mock import patch

from lobster.common.items import Implementation
from lobster.tools.codebeamer.codebeamer import get_query, to_lobster
from lobster.tools.codebeamer.config import AuthenticationConfig, Config


class TextDelegateTest(unittest.TestCase):

    @staticmethod
    def _create_config(schema):
        return Config(
            num_request_retry=42,
            retry_error_codes=[],
            references=None,
            import_tagged=None,
            import_query=None,
            baseline_id=None,
            verify_ssl=None,
            page_size=444,
            schema=schema,
            timeout=111,
            out=None,
            cb_auth_conf=AuthenticationConfig(
                token=None,
                user=None,
                password=None,
                root="http://the.requirements.server",
            )
        )

    def setUp(self):
        self._supported_schemas = ("Requirement", "Activity")
        self._description_key = "description"
        self._codebeamer_item = {
            "id": 123,
            "version": 456,
            "tracker": {
                "id": 789,
            },
            self._description_key:
                "I told my code it had a bug, "
                "but it just refused to take the feedback.",
        }

    def test_to_lobster_without_item_to_text(self):
        # lobster-trace: codebeamer_text_req.Item_To_Text_Delegate
        for schema in self._supported_schemas:
            with self.subTest(schema=schema):
                item = to_lobster(self._create_config(schema), self._codebeamer_item)

                self.assertIsNone(item.text)

    def test_to_lobster_item_to_text_returns_string(self):
        # lobster-trace: codebeamer_text_req.Item_To_Text_Delegate
        return_message = "So nice here!"
        for schema in self._supported_schemas:
            with self.subTest(schema=schema):
                config = self._create_config(schema)
                config.item_to_text = lambda item: return_message

                item = to_lobster(config, self._codebeamer_item)

                self.assertEqual(item.text, return_message)

    def test_to_lobster_item_to_text_returns_none(self):
        # lobster-trace: codebeamer_text_req.Item_To_Text_Delegate
        for schema in self._supported_schemas:
            with self.subTest(schema=schema):
                config = self._create_config(schema)
                config.item_to_text = lambda item: None

                item = to_lobster(config, self._codebeamer_item)

                self.assertIsNone(item.text)

    def test_to_lobster_item_to_text_exception_propagates(self):
        # lobster-trace: codebeamer_text_req.Item_To_Text_Delegate
        # lobster-trace: codebeamer_text_req.Item_To_Text_Delegate_Error_Propagation
        class DummyException(Exception):
            pass

        def item_to_text(_):
            raise DummyException()

        for schema in self._supported_schemas:
            with self.subTest(schema=schema):
                config = self._create_config(schema)
                config.item_to_text = item_to_text

                with self.assertRaises(DummyException):
                    to_lobster(config, self._codebeamer_item)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_query_passes_item_to_text_delegate(self, mock_query_cb_single):
        # lobster-trace: codebeamer_text_req.Get_Query_Passes_Config_To_To_Lobster
        for schema in self._supported_schemas:
            with self.subTest(schema=schema):

                # GIVEN a Config object with an item_to_text delegate that returns the
                # description of the Codebeamer item
                # and a responsive Codebeamer server
                mock_query_cb_single.return_value = {
                    "page": 1,
                    "pageSize": 757575,
                    "total": 1,
                    "items": [self._codebeamer_item],
                }
                config = self._create_config(schema)
                config.item_to_text = lambda item: item[self._description_key]

                # WHEN get_query is called with the config object
                result = get_query(config, "This is the query string.")

                # THEN the item_to_text delegate is called and its return value is
                # assigned to the text field of the resulting LOBSTER item
                self.assertEqual(
                    result[0].text,
                    self._codebeamer_item[self._description_key],
                )

    def test_to_lobster_does_not_call_item_to_text_for_implementation(self):
        # lobster-trace: codebeamer_text_req.Item_To_Text_Delegate
        config = self._create_config("Implementation")

        def item_to_text(_):
            self.fail("item_to_text must not be called for Implementation")

        config.item_to_text = item_to_text

        item = to_lobster(config, self._codebeamer_item)

        self.assertIsInstance(item, Implementation)

if __name__ == '__main__':
    unittest.main()
