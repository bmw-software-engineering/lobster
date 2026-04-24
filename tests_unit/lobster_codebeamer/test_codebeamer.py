import unittest
from unittest.mock import Mock, patch

from lobster.tools.codebeamer.codebeamer import (
    MismatchException,
    get_query, get_single_item,
    get_many_items, parse_config_data, to_lobster,
    import_tagged,
)

from lobster.tools.codebeamer.config import AuthenticationConfig, Config

LIST_OF_COMPARED_ATTRIBUTES = [
    'name',
    'kind',
    'status',
    'just_down',
    'just_up',
    'just_global'
]


class QueryCodebeamerTest(unittest.TestCase):
    def setUp(self):
        self._mock_cb_config = Config(
            num_request_retry=5,
            retry_error_codes=[],
            references=None,
            import_tagged=None,
            import_query=None,
            baseline_id=None,
            verify_ssl=None,
            page_size=10,
            schema="Requirement",
            timeout=123,
            out=None,
            cb_auth_conf=AuthenticationConfig(
                token=None,
                user=None,
                password=None,
                root="http://some.codebeamer.server",
            )
        )

    def _assertListEqualByAttributes(self, list1, list2):
        self.assertEqual(len(list1), len(list2), "Lists length are not the same")
        for obj1, obj2 in zip(list1, list2):
            for attr in LIST_OF_COMPARED_ATTRIBUTES:
                self.assertEqual(getattr(obj1, attr), getattr(obj2, attr),
                                 f"{obj1} is not like {obj2} in {attr}")

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_query_with_ID(self, mock_query_cb_single):
        mock_query = 171619121
        item_data = [
            {
                "ver_ValRationalargumentation": "Rationale from report wrapper",
                "item": {
                    "id": 34886222,
                    "name" : "mock item",
                    "version": 8,
                    "tracker": {
                        "id": 34158092
                        },
                    "categories": [{"name": "Requirement"}],
                    "status": {"name": "Content Review",}
                }
            }
        ]
        mock_query_cb_single.return_value = {
                "page": 1,
                "pageSize": 100,
                "total": 1,
                "items": item_data
            }

        result = get_query(self._mock_cb_config, mock_query)
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].kind, item_data[0]["item"]["categories"][0]["name"])
        self.assertEqual(result[0].status, item_data[0]["item"]["status"]["name"])
        self.assertEqual(result[0].name, item_data[0]["item"]["name"])
        self.assertEqual(result[0].tag.tag, str(item_data[0]["item"]["id"]))
        self.assertEqual(result[0].location.item, item_data[0]["item"]["id"])
        self.assertEqual(result[0].location.tracker,
                         item_data[0]["item"]["tracker"]["id"])
        self.assertEqual(result[0].location.version, item_data[0]["item"]["version"])
        self.assertEqual(
            result[0].ver_ValRationalargumentation,
            "Rationale from report wrapper",
        )

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    @patch('lobster.tools.codebeamer.codebeamer.get_single_item')
    def test_get_query_with_ID_does_not_override_non_null_with_wrapper_null(
            self,
            mock_get_single_item,
            mock_query_cb_single):
        mock_query = 171619121
        item_data = [
            {
                "ver_ValRationalargumentation": None,
                "item": {
                    "id": 34886222,
                    "name": "mock item",
                    "version": 8,
                    "tracker": {"id": 34158092},
                    "categories": [{"name": "Requirement"}],
                    "status": {"name": "Content Review"},
                    "ver_ValRationalargumentation": "Rationale from item",
                }
            }
        ]
        mock_query_cb_single.return_value = {
            "page": 1,
            "pageSize": 100,
            "total": 1,
            "items": item_data,
        }
        mock_get_single_item.return_value = None

        result = get_query(self._mock_cb_config, mock_query)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0].ver_ValRationalargumentation,
            "Rationale from item",
        )

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    @patch('lobster.tools.codebeamer.codebeamer.get_single_item')
    def test_get_query_with_ID_fetches_details_only_once_per_item(
            self,
            mock_get_single_item,
            mock_query_cb_single):
        mock_query = 171619121
        item_data = [
            {
                "item": {
                    "id": 34886222,
                    "name": "mock item",
                    "version": 8,
                    "tracker": {"id": 34158092},
                    "categories": [{"name": "Requirement"}],
                    "status": {"name": "Content Review"},
                }
            }
        ]
        mock_query_cb_single.return_value = {
            "page": 1,
            "pageSize": 100,
            "total": 1,
            "items": item_data,
        }
        mock_get_single_item.return_value = None

        result = get_query(self._mock_cb_config, mock_query)

        self.assertEqual(len(result), 1)
        self.assertEqual(mock_get_single_item.call_count, 1)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_query_with_query(self, mock_query_cb_single):
        mock_query = ("TeamID IN (10833708) AND workItemStatus IN ('InProgress') "
                      "AND summary LIKE 'Vulnerable Road User'")
        item_data = [
            {
                "id": 34886222,
                "name" : "mock item",
                "version": 8,
                "tracker": {
                    "id": 34158092
                    },
                "categories": [{"name": "Requirement"}],
                "status": {"name": "Content Review",}
            }
        ]
        mock_query_cb_single.return_value = {
                "page": 1,
                "pageSize": 100,
                "total": 1,
                "items": item_data
            }

        result = get_query(self._mock_cb_config, mock_query)
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].kind, item_data[0]["categories"][0]["name"])
        self.assertEqual(result[0].status, item_data[0]["status"]["name"])
        self.assertEqual(result[0].name, item_data[0]["name"])
        self.assertEqual(result[0].tag.tag, str(item_data[0]["id"]))
        self.assertEqual(result[0].location.item, item_data[0]["id"])
        self.assertEqual(result[0].location.tracker, item_data[0]["tracker"]["id"])
        self.assertEqual(result[0].location.version, item_data[0]["version"])

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_query_with_invalid_data(self, mock_query_cb_single):
        query_id = 789
        mock_query_cb_single.return_value = {
                "page": 1,
                "pageSize": 100,
                "total": 1,
                "items": []
            }
        with self.assertRaises(MismatchException):
            get_query(self._mock_cb_config, query_id)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_single_item(self, mock_query_cb_single):
        item_id = 11693324
        mock_response = Mock()
        mock_response.return_value = {
            'page': 1,
            'pageSize': 999,
            'total': 1,
            'items': [{'item': {'id': item_id, 'name': 'test name'}}]
        }

        mock_query_cb_single.return_value = mock_response

        query_result = get_single_item(self._mock_cb_config, item_id)
        self.assertEqual(query_result, mock_response)

    def test_get_single_item_invalid_id(self):
        for item_id in (None, 0, -1, "house", 123.456, "456"):
            with self.subTest(item_id=item_id):
                with self.assertRaises(ValueError):
                    get_single_item(self._mock_cb_config, item_id)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_many_items(self, mock_query_cb_single):
        item_ids = {24406947, 21747817}
        response_items = [
                {'id': 24406947, 'name': 'Test name 1'},
                {'id': 21747817, 'name': 'Test name 2'}
            ]
        mock_response = {
            'page': 1,
            'pageSize': 123,
            'total': len(response_items),
            'items': response_items
        }

        mock_query_cb_single.return_value = mock_response

        query_result = get_many_items(self._mock_cb_config, item_ids)
        self.assertEqual(query_result, response_items)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_import_tagged(self, mock_query_cb_single):
        item_ids = (24406947, 21747817)
        response_items = [
            {
                'id': item_ids[0],
                'name': 'Test name 1',
                'categories': [{'name': 'Folder'}],
                'version': 7,
                'status': {'name': 'status'},
                'tracker': {'id': 123}
            },
            {
                'id': item_ids[1],
                'name': 'Test name 2',
                'categories': [{'name': 'Folder'}],
                'version': 10,
                'status': {'name': 'status'},
                'tracker': {'id': 124}
            }
        ]
        mock_query_cb_single.return_value = {
            'page': 1,
            'pageSize': 100,
            'total': len(response_items),
            'items': response_items
        }

        expected_result = [to_lobster(self._mock_cb_config, items)
                           for items in response_items]

        import_tagged_result = import_tagged(self._mock_cb_config, set(item_ids))

        self._assertListEqualByAttributes(import_tagged_result, expected_result)

    def test_to_lobster_extracts_asil_from_asil_field(self):
        cb_item = {
            "id": 123,
            "name": "ASIL item",
            "version": 1,
            "tracker": {"id": 456},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "aSIL": {"name": "ASIL-B"},
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(item.asil, "ASIL-B")

    def test_to_lobster_extracts_asil_from_custom_fields(self):
        cb_item = {
            "id": 124,
            "name": "ASIL custom field item",
            "version": 1,
            "tracker": {"id": 457},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "customFields": [
                {
                    "name": "aSIL",
                    "values": [{"name": "QM"}],
                }
            ],
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(item.asil, "QM")

    def test_to_lobster_extracts_ver_val_rationalargumentation(self):
        rationale = "Tested as part of module test"
        cb_item = {
            "id": 125,
            "name": "Rationale item",
            "version": 1,
            "tracker": {"id": 458},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "ver_ValRationalargumentation": rationale,
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(item.ver_ValRationalargumentation, rationale)

    def test_to_lobster_extracts_ver_val_setup(self):
        setup = "SW unit/comp test"
        cb_item = {
            "id": 127,
            "name": "Setup item",
            "version": 1,
            "tracker": {"id": 460},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "ver_ValSetup": setup,
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(item.ver_ValSetup, setup)

    def test_to_lobster_keeps_setup_and_rationale_separate(self):
        cb_item = {
            "id": 128,
            "name": "Setup and rationale item",
            "version": 1,
            "tracker": {"id": 461},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "customFields": [
                {
                    "name": "ver_Val setup",
                    "values": ["SW unit/comp test"],
                },
                {
                    "name": "ver_val rational/argumentation",
                    "values": ["This is the rationale"],
                },
            ],
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(item.ver_ValSetup, "SW unit/comp test")
        self.assertEqual(item.ver_ValRationalargumentation, "This is the rationale")

    def test_to_lobster_extracts_rationale_from_spaced_slash_field_name(self):
        cb_item = {
            "id": 129,
            "name": "Rationale variant field name",
            "version": 1,
            "tracker": {"id": 462},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "customFields": [
                {
                    "name": "Ver_Val rational / argumentation",
                    "values": [{"text": "Detailed rationale text"}],
                },
            ],
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(item.ver_ValRationalargumentation, "Detailed rationale text")

    def test_to_lobster_extracts_rationale_from_custom_field_value_key(self):
        cb_item = {
            "id": 131,
            "name": "Rationale value key",
            "version": 1,
            "tracker": {"id": 464},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "customFields": [
                {
                    "name": "Ver_Val rational/argumentation",
                    "type": "WikiTextFieldValue",
                    "value": "Rationale from custom field value",
                },
            ],
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(
            item.ver_ValRationalargumentation,
            "Rationale from custom field value",
        )

    def test_to_lobster_extracts_rationale_from_nested_payload(self):
        cb_item = {
            "id": 130,
            "name": "Nested rationale field",
            "version": 1,
            "tracker": {"id": 463},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
            "payload": {
                "trackerItems": {
                    "items": [
                        {
                            "ver_ValRationalargumentation": "Nested rationale text",
                        },
                    ],
                },
            },
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(item.ver_ValRationalargumentation, "Nested rationale text")

    @patch('lobster.tools.codebeamer.codebeamer.get_single_item')
    def test_to_lobster_fetches_detailed_item_for_missing_rationale(
            self,
            mock_get_single_item):
        cb_item = {
            "id": 126,
            "name": "Rationale via detailed item",
            "version": 1,
            "tracker": {"id": 459},
            "categories": [{"name": "Requirement"}],
            "status": {"name": "Approved"},
        }

        mock_get_single_item.return_value = {
            "id": 126,
            "ver_ValRationalargumentation": "Detailed rationale text",
        }

        item = to_lobster(self._mock_cb_config, cb_item)

        self.assertEqual(
            item.ver_ValRationalargumentation,
            "Detailed rationale text",
        )


class ParseYamlTests(unittest.TestCase):
    def test_codebeamer_base(self):
        config = parse_config_data(
            {
                'root': 'https://example.com',
                'schema': 'Requirement',
                'import_query': 1231323,
            }
        )
        self.assertEqual(config.base, "https://example.com/api/v3")

    def test_parse_config_data_reads_baseline_id(self):
        config = parse_config_data(
            {
                'root': 'https://example.com',
                'schema': 'Requirement',
                'import_query': '375713047',
                'baseline_id': '407126303',
            }
        )

        self.assertEqual(config.import_query, '375713047')
        self.assertEqual(config.baseline_id, 407126303)

if __name__ == '__main__':
    unittest.main()
