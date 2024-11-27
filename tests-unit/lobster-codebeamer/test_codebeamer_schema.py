import unittest
from lobster.items import Tracing_Tag, Requirement, Implementation, Activity
from lobster.location import Codebeamer_Reference
from lobster.errors import LOBSTER_Error
from lobster.tools.codebeamer.codebeamer import _create_common_params, _create_lobster_item
 
class TestCreateFunctions(unittest.TestCase):


    def setUp(self):
        self.root_url = 'http://root_url'
        self.cb_item_template = {
            'version': 1,
            'tracker': {'id': 123}
        }
 

    def generate_cb_item(self, item_id, name):
        """Generate a codebeamer item dictionary."""
        return {
            'id': item_id,
            **self.cb_item_template,
            'name': name
        }

 
    def generate_common_params(self, namespace, item_name, kind, expected_class):
        """Generate a test case for common params and lobster item creation."""
        cb_item = self.generate_cb_item(1, item_name) 
        common_params = _create_common_params(namespace, cb_item, self.root_url, item_name, kind)
       
        return {
            'common_params': common_params,
            'item_name': item_name,
            'expected_class': expected_class,
            'tag': Tracing_Tag(namespace, str(cb_item["id"]), cb_item["version"]),
            'location': Codebeamer_Reference(self.root_url, cb_item["tracker"]["id"], cb_item["id"], cb_item["version"], item_name),
            'kind' : kind
        }


    def  generate_test_case(self):

        return [
            self.generate_common_params('req', 'Requirement Item', 'requirement', Requirement),
            self.generate_common_params('imp', 'Implementation Item', 'implementation', Implementation),
            self.generate_common_params('act', 'Activity Item', 'activity', Activity),
            ]


    def test_create_common_params(self):
        
        test_cases = self.generate_test_case()

        for case in test_cases:
            with self.subTest(case=case):
                
                self.assertEqual(case['common_params']['tag'].namespace, case['tag'].namespace)
                self.assertEqual(case['common_params']['tag'].tag, case['tag'].tag)
                self.assertEqual(case['common_params']['tag'].version, case['tag'].version)
                self.assertEqual(case['common_params']['location'].cb_root, case['location'].cb_root)
                self.assertEqual(case['common_params']['location'].tracker, case['location'].tracker)
                self.assertEqual(case['common_params']['location'].item, case['location'].item)
                self.assertEqual(case['common_params']['location'].version, case['location'].version)
                self.assertEqual(case['common_params']['location'].name, case['location'].name)
                self.assertEqual(case['common_params']['kind'], case['kind'])
 

    def test_create_lobster_item(self):
        # lobster-trace: codebeamer_req.Dummy_Requirement_Unit_Test
        test_cases = self.generate_test_case()
        for case in test_cases:
            with self.subTest(case=case):
                lobster_item = _create_lobster_item(case['expected_class'], case['common_params'], case['item_name'], None)
                self.assertIsInstance(lobster_item, case['expected_class'])
                self.assertEqual(lobster_item.tag, case['common_params']['tag'])
                self.assertEqual(lobster_item.location, case['common_params']['location'])
                self.assertEqual(lobster_item.kind, case['kind'])

                if case['kind'] == 'requirement':
                    self.assertEqual(lobster_item.framework, 'codebeamer')
                elif case['kind'] == 'implementation':
                    self.assertEqual(lobster_item.language, 'python')
                elif case['kind'] == 'activity':
                    self.assertEqual(lobster_item.framework, 'codebeamer')
 
if __name__ == '__main__':
    unittest.main()