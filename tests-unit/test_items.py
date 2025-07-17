import unittest
from unittest.mock import patch, MagicMock,create_autospec
from hashlib import sha1
from lobster.items import Tracing_Tag, Tracing_Status, Item, Requirement, Implementation, Activity
from lobster.location import Location

class ItemsTests(unittest.TestCase):
    def setUp(self):
        self.mock_namespace = "mock_namespace"
        self.mock_tag = "mock_tag"
        self.mock_framework = "mock_framework"
        self.mock_kind = "mock_kind"
        self.mock_name = "mock_name"
        self.mock_text = "mock_text"
        self.mock_status = "active"
        self.mock_language = "mock_language"
        self.mock_location = create_autospec(Location, instance=True)
        self.tracing_tag = Tracing_Tag(self.mock_namespace, self.mock_tag)
        self.item = Item(self.tracing_tag, self.mock_location)
        self.requirement = Requirement(
            self.tracing_tag,
            self.mock_location,
            self.mock_framework,
            self. mock_kind,
            self.mock_name,
            self.mock_text,
            self.mock_status,
        )
        self.implementation = Implementation(
            self.tracing_tag,
            self.mock_location,
            self.mock_language,
            self.mock_kind,
            self.mock_name,
        )
        self.activity = Activity(self.tracing_tag, self.mock_location, self.mock_framework, self.mock_kind)

    def set_location_data(self, location_type):
        if location_type == "file":
            location_data = {
            "kind": location_type,
            "file": "example.txt"
        }
        elif location_type == "github":
            location_data = {
                "kind": location_type,
                "gh_root": "https://mysuperserver.com",
                "file": "example.txt",
                "line": 1,
                "commit": "efdc34rfe2345554rfe"
            }
        elif location_type == "codebeamer":
            location_data = {
                "kind": location_type,
                "cb_root": "https://mysuperserver.com",
                "tracker": 1,
                "item": 1,
                "version": 1,
                "name": "name string"
            }
        elif location_type == "void":
            location_data = {
                "kind": location_type
            }
        else:
            raise NotImplementedError(f"No logic implemented for {location_type=}!")
        return location_data

class TestTracingTag(ItemsTests):
    def test_key(self):
        expected_key = "mock_namespace mock_tag"
        actual_key = self.tracing_tag.key()

        self.assertEqual(expected_key, actual_key)

    def test_to_json(self):
        expected_json = "mock_namespace mock_tag"
        actual_json = self.tracing_tag.to_json()

        self.assertEqual(expected_json, actual_json)

    @patch('lobster.items.Tracing_Tag.from_text')
    def test_from_json(self, mock_from_text):
        json_input = "namespace string"
        expected_namespace = "namespace"
        expected_rest_value = "string"
        expected_result = self.tracing_tag
        mock_from_text.return_value = expected_result
        result = self.tracing_tag.from_json(json_input)

        mock_from_text.assert_called_once_with(expected_namespace, expected_rest_value)
        self.assertEqual(result, expected_result)

    def test_from_text_with_version(self):
        text = "mock_tag@version"
        expected_namespace = "mock_namespace"
        expected_tag = "mock_tag"
        expected_version = "version"
        result = self.tracing_tag.from_text(self.tracing_tag.namespace, text)

        self.assertEqual(result.namespace, expected_namespace)
        self.assertEqual(result.tag, expected_tag)
        self.assertEqual(result.version, expected_version)

    def test_from_text_without_version(self):
        namespace = "namespace"
        text = "tag"
        expected_tag = "tag"
        expected_version = None
        result = self.tracing_tag.from_text(namespace, text)

        self.assertEqual(result.namespace, namespace)
        self.assertEqual(result.tag, expected_tag)
        self.assertEqual(result.version, expected_version)

    def test_from_text_invalid_namespace(self):
        with self.assertRaises(AssertionError):
            self.tracing_tag.from_text(123, "tag@version")

    def test_from_text_invalid_text(self):
        with self.assertRaises(AssertionError):
            self.tracing_tag.from_text("namespace", 123)

    def test_hash(self):
        hash_val = self.tracing_tag.hash()
        hfunc = sha1()
        hfunc.update(self.tracing_tag.key().encode("UTF-8"))
        expected_hash = hfunc.hexdigest()

        self.assertEqual(hash_val, expected_hash)

class TestItem(ItemsTests):
    def test_set_level_valid_string(self):
        mock_level = "mock_level"
        self.item.set_level(mock_level)

        self.assertEqual(self.item.level, mock_level)

    def test_set_level_invalid_string(self):
        invalid_level = 10

        with self.assertRaises(AssertionError):
            self.item.set_level(invalid_level)

    def test_error(self):
        mock_message = "mock_message"
        self.item.error(mock_message)

        self.assertIn(mock_message, self.item.messages)
        self.assertTrue(self.item.messages)

    @patch("lobster.items.Tracing_Tag.key")
    def test_add_tracing_target(self, mock_key):
        mock_target = self.tracing_tag
        expected_result = "mock_namespace mock_tag"
        mock_key.return_value = expected_result
        self.item.add_tracing_target(mock_target)

        self.assertIn(mock_target, self.item.unresolved_references)
        self.assertIn(expected_result, self.item.unresolved_references_cache)

    def test_perform_source_checks(self):
        mock_valid_source_info = {"key": "value"}
        try:
            self.item.perform_source_checks(mock_valid_source_info)
        except AssertionError:
            self.fail("perform_source_checks() raised AssertionError unexpectedly!")

    def test_perform_source_checks_with_invalid_type(self):
        mock_invalid_source_info = ["not", "a", "dictionary"]

        with self.assertRaises(AssertionError):
            self.item.perform_source_checks(mock_invalid_source_info)

    @patch("lobster.items.Tracing_Tag.key")
    def test_determine_status_ok(self, mock_key):
        self.item.ref_up = []
        self.item.ref_down = [self.tracing_tag]
        self.item.just_up = []
        self.item.just_down = []
        self.item.just_global = []
        self.item.messages = []
        self.item.has_error = False
        self.item.level = "level1"
        expected_result = "mock_namespace mock_tag"
        mock_key.return_value = expected_result
        config = {
            "level1": {
                "needs_tracing_up": True,
                "needs_tracing_down": True,
                "traces": ["level1"],
                "breakdown_requirements": [["level1"]]
            }
        }
        stab = {
            mock_key() : self.item
        }
        self.item.determine_status(config, stab)

        self.assertEqual(self.item.tracing_status, Tracing_Status.PARTIAL)

    def test_determine_status_missing_up_reference(self):
        mock_namespace = "mock_namespace"
        mock_tag = "mock_tag"
        self.item.level = "level1"
        self.item.just_up = []
        self.item.just_global = []
        self.item.ref_up = []
        config = {
            "level1": {
                "needs_tracing_up": True,
                "needs_tracing_down": False,
                "traces": ["level1"],
                "breakdown_requirements": [["level1"]]
            }
        }
        stab = {
            Tracing_Tag(mock_namespace, mock_tag).key() : self.item
        }
        self.item.determine_status(config, stab)

        self.assertEqual(self.item.tracing_status, Tracing_Status.MISSING)
        self.assertIn("missing up reference", self.item.messages)

    def test_determine_status_missing_down_reference(self):
        mock_namespace = "mock_namespace"
        mock_tag = "mock_tag"
        self.item.level = "level1"
        self.item.just_down = []
        self.item.just_global = []
        self.item.ref_down = []
        config = {
            "level1": {
                "needs_tracing_up": False,
                "needs_tracing_down": True,
                "traces": ["level1"],
                "breakdown_requirements": [["level1"]]
            }
        }
        stab = {
            Tracing_Tag(mock_namespace, mock_tag).key() : self.item
        }
        self.item.determine_status(config, stab)

        self.assertEqual(self.item.tracing_status, Tracing_Status.MISSING)
        self.assertIn("missing reference to level1", self.item.messages)

    @patch("lobster.items.Item.set_level")
    def test_additional_data_from_json_valid_data(self, mock_set_level):
        mock_level = "mock_level"
        mock_set_level.return_value = "mock_level"
        mock_data = {
            "refs": ["mock_namespace mock_tag"],
            "ref_up": ["mock refup"],
            "ref_down": ["mock refdown"],
            "messages": ["message1", "message2"],
            "just_up": ["up1"],
            "just_down": ["down1"],
            "just_global": ["global1"],
            "tracing_status": "OK"
        }
        schema_version = 3
        self.item.additional_data_from_json(mock_level, mock_data, schema_version)

        self.assertEqual(mock_set_level(), mock_level)
        self.assertEqual([tag.namespace + " " + tag.tag for tag in self.item.ref_up], ["mock refup"])
        self.assertEqual([tag.namespace + " " + tag.tag for tag in self.item.ref_down], ["mock refdown"])
        self.assertEqual(self.item.messages, ["message1", "message2"])
        self.assertEqual(self.item.just_up, ["up1"])
        self.assertEqual(self.item.just_down, ["down1"])
        self.assertEqual(self.item.just_global, ["global1"])
        self.assertEqual(self.item.tracing_status, Tracing_Status.OK)

    def test_additional_data_from_json_invalid_level(self):
        level = 123
        data = {}
        schema_version = 3

        with self.assertRaises(AssertionError):
            self.item.additional_data_from_json(level, data, schema_version)

    def test_additional_data_from_json_invalid_data(self):
        level = "info"
        data = ["invalid", "list"]
        schema_version = 3

        with self.assertRaises(AssertionError):
            self.item.additional_data_from_json(level, data, schema_version)

    def test_additional_data_from_json_invalid_schema_version(self):
        level = "info"
        data = {}
        schema_version = 2

        with self.assertRaises(AssertionError):
            self.item.additional_data_from_json(level, data, schema_version)

    @patch("lobster.items.Tracing_Tag.to_json")
    def test_to_json(self, mock_to_json):
        mock_to_json.return_value = "mock_value"
        self.item.name = "mock_name"
        self.item.messages = ["message1", "message2"]
        self.item.just_up = True
        self.item.just_down = False
        self.item.just_global = True
        self.item.unresolved_references = [self.tracing_tag]
        self.item.ref_up = [self.tracing_tag]
        self.item.ref_down = [self.tracing_tag]
        self.item.tracing_status = MagicMock()
        self.item.tracing_status.name = "mock_status"
        expected_json = {
            "tag": "mock_value",
            "location": self.mock_location.to_json(),
            "name": "mock_name",
            "messages": ["message1", "message2"],
            "just_up": True,
            "just_down": False,
            "just_global": True,
            "refs": ["mock_value"],
            "ref_up": ["mock_value"],
            "ref_down": ["mock_value"],
            "tracing_status": "mock_status"
        }
        result = self.item.to_json()

        self.assertEqual(result, expected_json)

class TestRequirement(ItemsTests):
    @patch("lobster.items.Item.to_json")
    def test_to_json(self, mock_super_to_json):
        mock_super_to_json.return_value = {
            "item_property": "item_value"
        }
        expected_result = {
            "item_property": "item_value",
            "framework": "mock_framework",
            "kind": "mock_kind",
            "text": "mock_text",
            "status": "active"
        }
        result = self.requirement.to_json()

        mock_super_to_json.assert_called_once_with()
        self.assertEqual(result, expected_result)

    @patch("lobster.items.Item.error")
    def test_perform_source_checks_valid_status(self, mock_super_error):
        mock_error_message = None
        mock_super_error.return_value = mock_error_message
        source_info = {
            "valid_status": ["active", "inactive"]
        }
        self.requirement.perform_source_checks(source_info)

        self.assertIsNone(mock_super_error())

    @patch("lobster.items.Item.error")
    def test_perform_source_checks_invalid_status(self, mock_super_error):
        mock_error_message = "status is active, expected closed or inactive"
        mock_super_error.return_value = mock_error_message
        source_info = {
            "valid_status": ["inactive", "closed"]
        }
        self.requirement.perform_source_checks(source_info)
        expected_error_message = "status is active, expected closed or inactive"

        self.assertEqual(mock_super_error(), expected_error_message)

    def test_perform_source_checks_invalid_source_info(self):
        invalid_source_info = ["invalid", "list"]

        with self.assertRaises(AssertionError):
            self.requirement.perform_source_checks(invalid_source_info)

    @patch("lobster.items.Tracing_Tag.from_json")
    def test_from_json(self, mock_from_json):
        mock_level = "mock_level"
        mock_schema_version = 3
        mock_from_json.return_value = self.tracing_tag
        for location_type in ["file", "github", "codebeamer", "void"]:
            with self.subTest(location_type):
                location_data = self.set_location_data(location_type)
                mock_data = {
                    "tag": self.tracing_tag,
                    "location": location_data,
                    "framework": "framework_data",
                    "kind": "kind_data",
                    "name": "name_data",
                    "text": "text_data",
                    "status": "status_data"
                }
                result = self.requirement.from_json(mock_level, mock_data, mock_schema_version)

                self.assertEqual(result.tag, self.tracing_tag)
                self.assertEqual(result.framework, "framework_data")
                self.assertEqual(result.kind, "kind_data")
                self.assertEqual(result.name, "name_data")
                self.assertEqual(result.text, "text_data")
                self.assertEqual(result.status, "status_data")
                if location_type == "file":
                    self.assertEqual(result.location.filename, location_data["file"])
                elif location_type == "github":
                    self.assertEqual(result.location.gh_root, location_data["gh_root"])
                    self.assertEqual(result.location.filename, location_data["file"])
                    self.assertEqual(result.location.line, location_data["line"])
                    self.assertEqual(result.location.commit, location_data["commit"])
                elif location_type == "codebeamer":
                    self.assertEqual(result.location.cb_root, location_data["cb_root"])
                    self.assertEqual(result.location.tracker, location_data["tracker"])
                    self.assertEqual(result.location.item, location_data["item"])
                    self.assertEqual(result.location.version, location_data["version"])
                    self.assertEqual(result.location.name, location_data["name"])

class TestImplementation(ItemsTests):
    @patch("lobster.items.Item.to_json")
    def test_to_json(self, mock_super_to_json):
        mock_super_to_json.return_value = {
            "item_property": "item_value"
        }
        expected_result = {
            "item_property": "item_value",
            "language": "mock_language",
            "kind": "mock_kind"
        }
        result = self.implementation.to_json()

        mock_super_to_json.assert_called_once_with()
        self.assertEqual(result, expected_result)

    @patch("lobster.items.Tracing_Tag.from_json")
    def test_from_json(self, mock_from_json):
        mock_level = "mock_level"
        mock_schema_version = 3
        mock_from_json.return_value = self.tracing_tag
        for location_type in ["file", "github", "codebeamer", "void"]:
            with self.subTest(location_type):
                location_data = self.set_location_data(location_type)
                mock_data = {
                    "tag": self.tracing_tag,
                    "location": location_data,
                    "language": "Python",
                    "kind": "kind_data",
                    "name": "name_data",
                }
                result = self.implementation.from_json(mock_level, mock_data, mock_schema_version)

                self.assertEqual(result.tag, self.tracing_tag)
                self.assertEqual(result.language, "Python")
                self.assertEqual(result.kind, "kind_data")
                self.assertEqual(result.name, "name_data")
                if location_type == "file":
                    self.assertEqual(result.location.filename, location_data["file"])
                elif location_type == "github":
                    self.assertEqual(result.location.gh_root, location_data["gh_root"])
                    self.assertEqual(result.location.filename, location_data["file"])
                    self.assertEqual(result.location.line, location_data["line"])
                    self.assertEqual(result.location.commit, location_data["commit"])
                elif location_type == "codebeamer":
                    self.assertEqual(result.location.cb_root, location_data["cb_root"])
                    self.assertEqual(result.location.tracker, location_data["tracker"])
                    self.assertEqual(result.location.item, location_data["item"])
                    self.assertEqual(result.location.version, location_data["version"])
                    self.assertEqual(result.location.name, location_data["name"])

class TestActivity(ItemsTests):
    @patch("lobster.items.Item.to_json")
    def test_to_json(self, mock_super_to_json):
        mock_super_to_json.return_value = {
            "item_property": "item_value"
        }
        expected_result = {
            "item_property": "item_value",
            "framework": "mock_framework",
            "kind": "mock_kind",
            "status": None
        }
        result = self.activity.to_json()

        mock_super_to_json.assert_called_once_with()
        self.assertEqual(result, expected_result)

    @patch("lobster.items.Tracing_Tag.from_json")
    def test_from_json(self, mock_from_json):
        mock_level = "mock_level"
        mock_schema_version = 3
        mock_from_json.return_value = self.tracing_tag
        for location_type in ["file", "github", "codebeamer", "void"]:
            with self.subTest(location_type):
                location_data = self.set_location_data(location_type)
                mock_data = {
                    "tag": self.tracing_tag,
                    "location": location_data,
                    "framework": "framework_data",
                    "kind": "kind_data",
                    "status": None
                }
                result = self.activity.from_json(mock_level, mock_data, mock_schema_version)

                self.assertEqual(result.tag, self.tracing_tag)
                self.assertEqual(result.framework, "framework_data")
                self.assertEqual(result.kind, "kind_data")
                self.assertEqual(result.status, None)
                if location_type == "file":
                    self.assertEqual(result.location.filename, location_data["file"])
                elif location_type == "github":
                    self.assertEqual(result.location.gh_root, location_data["gh_root"])
                    self.assertEqual(result.location.filename, location_data["file"])
                    self.assertEqual(result.location.line, location_data["line"])
                    self.assertEqual(result.location.commit, location_data["commit"])
                elif location_type == "codebeamer":
                    self.assertEqual(result.location.cb_root, location_data["cb_root"])
                    self.assertEqual(result.location.tracker, location_data["tracker"])
                    self.assertEqual(result.location.item, location_data["item"])
                    self.assertEqual(result.location.version, location_data["version"])
                    self.assertEqual(result.location.name, location_data["name"])

if __name__ == '__main__':
    unittest.main()
