import unittest
from unittest.mock import Mock, patch

from lobster.tools.codebeamer.codebeamer import get_query, get_single_item, get_many_items, to_lobster, \
    import_tagged
from lobster.errors import Message_Handler

list_of_compared_attributes = ['name', 'kind', 'status', 'just_down', 'just_up', 'just_global']


class QueryCodebeamerTest(unittest.TestCase):
    def _assertListEqualByAttributes(self, list1, list2):
        self.assertEqual(len(list1), len(list2), "Lists length are not the same")
        for obj1, obj2 in zip(list1, list2):
            for attr in list_of_compared_attributes:
                self.assertEqual(getattr(obj1, attr), getattr(obj2, attr), f"{obj1} is not like {obj2} in {attr}")

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_query_with_ID(self, mock_query_cb_single):
        mh = Message_Handler()
        mock_cb_config = {
            "root" : "https://codebeamer.bmwgroup.net",
            "base": "https://test.com",
            "page_size": 10
        }
        mock_query = 171619121
        item_data = [
            {
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

        result = get_query(mh, mock_cb_config, mock_query)
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].kind, item_data[0]["item"]["categories"][0]["name"])
        self.assertEqual(result[0].status, item_data[0]["item"]["status"]["name"])
        self.assertEqual(result[0].name, item_data[0]["item"]["name"])
        self.assertEqual(result[0].tag.tag, str(item_data[0]["item"]["id"]))
        self.assertEqual(result[0].location.item, item_data[0]["item"]["id"])
        self.assertEqual(result[0].location.tracker, item_data[0]["item"]["tracker"]["id"])
        self.assertEqual(result[0].location.version, item_data[0]["item"]["version"])

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_query_with_query(self, mock_query_cb_single):
        mh = Message_Handler()
        mock_cb_config = {
            "root" : "https://codebeamer.bmwgroup.net",
            "base": "https://test.com",
            "page_size": 10
        }
        mock_query = "TeamID IN (10833708) AND workItemStatus IN ('InProgress') AND summary LIKE 'Vulnerable Road User'"
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

        result = get_query(mh, mock_cb_config, mock_query)
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
        mock_query = 789
        mh = Message_Handler()
        mock_cb_config = {
            "root" : "https://codebeamer.bmwgroup.net",
            "base": "https://test.com",
            "page_size": 10
        }
        mock_query_cb_single.return_value = {
                "page": 1,
                "pageSize": 100,
                "total": 1,
                "items": []
            }  
        with self.assertRaises(SystemExit):
            get_query(mh, mock_cb_config, mock_query)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_single_item(self, mock_get):
        _item_id = 11693324
        _cb_config = {'base': 'https://test.com'}
        _moch_response = Mock()
        _expected_test_result = {
            'page': 1,
            'pageSize': 100,
            'total': 1,
            'items': [{'item': {'id': 11693324, 'name': 'test name'}}]
        }
        _moch_response.return_value = _expected_test_result

        mock_get.return_value = _moch_response

        query_result = get_single_item(_cb_config, _item_id)
        self.assertEqual(query_result, _moch_response)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_get_many_items(self, mock_get):
        _item_ids = {24406947, 21747817}
        _cb_config = {'base': 'https://test.com', 'page_size': 100}
        _response_items = [
                {'id': 24406947, 'name': 'Test name 1'},
                {'id': 21747817, 'name': 'Test name 2'}
            ]
        _moch_response = {
            'page': 1,
            'pageSize': 100,
            'total': 2,
            'items': _response_items
        }

        mock_get.return_value = _moch_response

        query_result = get_many_items(_cb_config, _item_ids)
        self.assertEqual(query_result, _response_items)

    @patch('lobster.tools.codebeamer.codebeamer.query_cb_single')
    def test_import_tagged(self, mock_get):
        # lobster-trace: codebeamer_req.Dummy_Requirement_Unit_Test
        _mh = Message_Handler()
        _item_ids = {24406947, 21747817}
        _cb_config = {'root': 'https://test.com/', 'base': 'https://test.com/base', 'page_size': 100}
        _response_items = [
            {
                'id': 24406947,
                'name': 'Test name 1',
                'categories': [{'name': 'Folder'}],
                'version': 7,
                'status': {'name': 'status'},
                'tracker': {'id': 123}
            },
            {
                'id': 21747817,
                'name': 'Test name 2',
                'categories': [{'name': 'Folder'}],
                'version': 10,
                'status': {'name': 'status'},
                'tracker': {'id': 123}
            }
        ]
        _mock_response = {
            'page': 1,
            'pageSize': 100,
            'total': 2,
            'items': _response_items
        }
        mock_get.return_value = _mock_response

        _expected_result = [to_lobster(_cb_config, items) for items in _response_items]

        import_tagged_result = import_tagged(_mh, _cb_config, _item_ids)

        self._assertListEqualByAttributes(import_tagged_result, _expected_result)


if __name__ == '__main__':
    unittest.main()
