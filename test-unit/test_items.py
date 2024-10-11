import unittest
from unittest.mock import patch, MagicMock,create_autospec
from lobster.items import Tracing_Tag, Tracing_Status, Item, Requirement, Implementation, Activity
from hashlib import sha1
from lobster.location import Location

class SetUp(unittest.TestCase):
    mock_namespace = "mock_namespace"
    mock_tag = "mock_tag"
    mock_framework = "mock_framework"
    mock_kind = "mock_kind"
    mock_name = "mock_name"
    mock_text = "mock_text"
    mock_status = "active"
    mock_language = "mock_language"
    mock_location = create_autospec(Location, instance=True)
    tracing_tag = Tracing_Tag(mock_namespace, mock_tag)
    item = Item(tracing_tag, mock_location)
    requirement = Requirement(tracing_tag, mock_location, mock_framework, mock_kind, mock_name, mock_text, mock_status)
    implementation = Implementation(tracing_tag, mock_location, mock_language, mock_kind, mock_name)
    activity = Activity(tracing_tag, mock_location, mock_framework, mock_kind)

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
                "commit": "commit string",
                "file": "example.txt",
                "line": 1
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
        return location_data

class TestTracingTag(unittest.TestCase):
    def test_key(self):
        expected_key = "mock_namespace mock_tag"
        actual_key = SetUp.tracing_tag.key()
        self.assertEqual(expected_key, actual_key)

    def test_to_json(self):
        expected_json = "mock_namespace mock_tag"
        actual_json = SetUp.tracing_tag.to_json()
        self.assertEqual(expected_json, actual_json)

    @patch('lobster.items.Tracing_Tag.from_text')
    def test_from_json(self, mock_from_text):
        json_input = "namespace string"
        expected_namespace = "namespace"
        expected_rest_value = "string"
        expected_result = SetUp.tracing_tag
        mock_from_text.return_value = expected_result

        result = SetUp.tracing_tag.from_json(json_input)

        mock_from_text.assert_called_once_with(expected_namespace, expected_rest_value)
        self.assertEqual(result, expected_result)

    def test_from_text_with_version(self):
        text = "mock_tag@version"
        expected_namespace = "mock_namespace"
        expected_tag = "mock_tag"
        expected_version = "version"

        result = SetUp.tracing_tag.from_text(SetUp.tracing_tag.namespace, text)

        self.assertEqual(result.namespace, expected_namespace)
        self.assertEqual(result.tag, expected_tag)
        self.assertEqual(result.version, expected_version)

    def test_from_text_without_version(self):
        namespace = "namespace"
        text = "tag"
        expected_tag = "tag"
        expected_version = None

        result = SetUp.tracing_tag.from_text(namespace, text)

        self.assertEqual(result.namespace, namespace)
        self.assertEqual(result.tag, expected_tag)
        self.assertEqual(result.version, expected_version)

    def test_from_text_invalid_namespace(self):
        with self.assertRaises(AssertionError):
            SetUp.tracing_tag.from_text(123, "tag@version")

    def test_from_text_invalid_text(self):
        with self.assertRaises(AssertionError):
            SetUp.tracing_tag.from_text("namespace", 123)

    def test_hash(self):
        hash_val = SetUp.tracing_tag.hash()
        hfunc = sha1()
        hfunc.update(SetUp.tracing_tag.key().encode("UTF-8"))
        expected_hash = hfunc.hexdigest()
        self.assertEqual(hash_val, expected_hash)

class TestItem(unittest.TestCase):
    def test_set_level_valid_string(self):
        mock_level = "mock_level"

        SetUp.item.set_level(mock_level)

        self.assertEqual(SetUp.item.level, mock_level)

    def test_set_level_invalid_string(self):
        invalid_level = 10

        with self.assertRaises(AssertionError):
            result = SetUp.item.set_level(invalid_level)

    def test_error(self):
        mock_message = "mock_message"

        SetUp.item.error(mock_message)

        self.assertIn(mock_message, SetUp.item.messages)
        self.assertTrue(SetUp.item.messages)

    @patch("lobster.items.Tracing_Tag.key")
    def test_add_tracing_target(self, mock_key):
        mock_target = SetUp.tracing_tag
        expected_result = "mock_namespace mock_tag"

        mock_key.return_value = expected_result

        SetUp.item.add_tracing_target(mock_target)
        self.assertIn(mock_target, SetUp.item.unresolved_references)
        self.assertIn(expected_result, SetUp.item.unresolved_references_cache)

    def test_perform_source_checks(self):
        mock_valid_source_info = {"key": "value"}

        try:
            SetUp.item.perform_source_checks(mock_valid_source_info)
        except AssertionError:
            self.fail("perform_source_checks() raised AssertionError unexpectedly!")

    def test_perform_source_checks_with_invalid_type(self):
        mock_invalid_source_info = ["not", "a", "dict"]

        with self.assertRaises(AssertionError):
            SetUp.item.perform_source_checks(mock_invalid_source_info)

    @patch("lobster.items.Tracing_Tag.key")
    def test_determine_status_ok(self, mock_key):
        SetUp.item.ref_up = []
        SetUp.item.ref_down = [SetUp.tracing_tag]
        SetUp.item.just_up = []
        SetUp.item.just_down = []
        SetUp.item.just_global = []
        SetUp.item.messages = []
        SetUp.item.has_error = False
        SetUp.item.level = "level1"
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
            mock_key() : SetUp.item
        }

        SetUp.item.determine_status(config, stab)
        self.assertEqual(SetUp.item.tracing_status, Tracing_Status.PARTIAL)

    def test_determine_status_missing_up_reference(self):
        mock_namespace = "mock_namespace"
        mock_tag = "mock_tag"
        SetUp.item.level = "level1"
        SetUp.item.just_up = []
        SetUp.item.just_global = []
        SetUp.item.ref_up = []
        config = {
            "level1": {
                "needs_tracing_up": True,
                "needs_tracing_down": False,
                "traces": ["level1"],
                "breakdown_requirements": [["level1"]]
            }
        }
        stab = {
            Tracing_Tag(mock_namespace, mock_tag).key() : SetUp.item
        }

        SetUp.item.determine_status(config, stab)
        self.assertEqual(SetUp.item.tracing_status, Tracing_Status.MISSING)
        self.assertIn("missing up reference", SetUp.item.messages)

    def test_determine_status_missing_down_reference(self):
        mock_namespace = "mock_namespace"
        mock_tag = "mock_tag"
        SetUp.item.level = "level1"
        SetUp.item.just_down = []
        SetUp.item.just_global = []
        SetUp.item.ref_down = []
        config = {
            "level1": {
                "needs_tracing_up": False,
                "needs_tracing_down": True,
                "traces": ["level1"],
                "breakdown_requirements": [["level1"]]
            }
        }
        stab = {
            Tracing_Tag(mock_namespace, mock_tag).key() : SetUp.item
        }

        SetUp.item.determine_status(config, stab)
        self.assertEqual(SetUp.item.tracing_status, Tracing_Status.MISSING)
        self.assertIn("missing reference to level1", SetUp.item.messages)

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

        SetUp.item.additional_data_from_json(mock_level, mock_data, schema_version)

        self.assertEqual(mock_set_level(), mock_level)
        self.assertEqual([tag.namespace + " " + tag.tag for tag in SetUp.item.ref_up], ["mock refup"])
        self.assertEqual([tag.namespace + " " + tag.tag for tag in SetUp.item.ref_down], ["mock refdown"])
        self.assertEqual(SetUp.item.messages, ["message1", "message2"])
        self.assertEqual(SetUp.item.just_up, ["up1"])
        self.assertEqual(SetUp.item.just_down, ["down1"])
        self.assertEqual(SetUp.item.just_global, ["global1"])
        self.assertEqual(SetUp.item.tracing_status, Tracing_Status.OK)

    def test_additional_data_from_json_invalid_level(self):
        level = 123
        data = {}
        schema_version = 3

        with self.assertRaises(AssertionError):
            SetUp.item.additional_data_from_json(level, data, schema_version)

    def test_additional_data_from_json_invalid_data(self):
        level = "info"
        data = ["invalid", "list"]
        schema_version = 3

        with self.assertRaises(AssertionError):
            SetUp.item.additional_data_from_json(level, data, schema_version)

    def test_additional_data_from_json_invalid_schema_version(self):
        level = "info"
        data = {}
        schema_version = 2

        with self.assertRaises(AssertionError):
            SetUp.item.additional_data_from_json(level, data, schema_version)

    @patch("lobster.items.Tracing_Tag.to_json")
    def test_to_json(self, mock_to_json):
        mock_to_json.return_value = "mock_value"
        SetUp.item.name = "mock_name"
        SetUp.item.messages = ["message1", "message2"]
        SetUp.item.just_up = True
        SetUp.item.just_down = False
        SetUp.item.just_global = True
        SetUp.item.unresolved_references = [SetUp.tracing_tag]
        SetUp.item.ref_up = [SetUp.tracing_tag]
        SetUp.item.ref_down = [SetUp.tracing_tag]
        SetUp.item.tracing_status = MagicMock()
        SetUp.item.tracing_status.name = "mock_status"
        expected_json = {
            "tag": "mock_value",
            "location": SetUp.mock_location.to_json(),
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

        result = SetUp.item.to_json()

        self.assertEqual(result, expected_json)

class TestRequirement(unittest.TestCase):
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
        result = SetUp.requirement.to_json()

        mock_super_to_json.assert_called_once_with()
        self.assertEqual(result, expected_result)

    @patch("lobster.items.Item.error")
    def test_perform_source_checks_valid_status(self, mock_super_error):
        mock_error_message = None
        mock_super_error.return_value = mock_error_message
        source_info = {
            "valid_status": ["active", "inactive"]
        }

        SetUp.requirement.perform_source_checks(source_info)

        self.assertIsNone(mock_super_error())

    @patch("lobster.items.Item.error")
    def test_perform_source_checks_invalid_status(self, mock_super_error):
        mock_error_message = "status is active, expected closed or inactive"
        mock_super_error.return_value = mock_error_message
        source_info = {
            "valid_status": ["inactive", "closed"]
        }

        SetUp.requirement.perform_source_checks(source_info)

        expected_error_message = "status is active, expected closed or inactive"
        self.assertEqual(mock_super_error(), expected_error_message)

    def test_perform_source_checks_invalid_source_info(self):
        invalid_source_info = ["invalid", "list"]

        with self.assertRaises(AssertionError):
            SetUp.requirement.perform_source_checks(invalid_source_info)

    @patch("lobster.items.Tracing_Tag.from_json")
    def test_from_json(self, mock_from_json):
        mock_level = "mock_level"
        mock_schema_version = 3
        setup = SetUp()
        mock_from_json.return_value = SetUp.tracing_tag
        for location_type in ["file", "github", "codebeamer", "void"]:
            with self.subTest(location_type):
                location_data = setup.set_location_data(location_type)
                mock_data = {
                    "tag": SetUp.tracing_tag,
                    "location": location_data,
                    "framework": "framework_data",
                    "kind": "kind_data",
                    "name": "name_data",
                    "text": "text_data",
                    "status": "status_data"
                }
                result = setup.requirement.from_json(mock_level, mock_data, mock_schema_version)
                self.assertEqual(result.tag, SetUp.tracing_tag)
                self.assertEqual(result.framework, "framework_data")
                self.assertEqual(result.kind, "kind_data")
                self.assertEqual(result.name, "name_data")
                self.assertEqual(result.text, "text_data")
                self.assertEqual(result.status, "status_data")
                if location_type == "file":
                            self.assertEqual(result.location.filename, location_data["file"])
                elif location_type == "github":
                    self.assertEqual(result.location.gh_root, location_data["gh_root"])
                    self.assertEqual(result.location.commit, location_data["commit"])
                    self.assertEqual(result.location.filename, location_data["file"])
                    self.assertEqual(result.location.line, location_data["line"])
                elif location_type == "codebeamer":
                    self.assertEqual(result.location.cb_root, location_data["cb_root"])
                    self.assertEqual(result.location.tracker, location_data["tracker"])
                    self.assertEqual(result.location.item, location_data["item"])
                    self.assertEqual(result.location.version, location_data["version"])
                    self.assertEqual(result.location.name, location_data["name"])

class TestImplementation(unittest.TestCase):
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

        result = SetUp.implementation.to_json()

        mock_super_to_json.assert_called_once_with()
        self.assertEqual(result, expected_result)

    @patch("lobster.items.Tracing_Tag.from_json")
    def test_from_json(self, mock_from_json):
        mock_level = "mock_level"
        mock_schema_version = 3
        setup = SetUp()
        mock_from_json.return_value = SetUp.tracing_tag
        for location_type in ["file", "github", "codebeamer", "void"]:
            with self.subTest(location_type):
                location_data = setup.set_location_data(location_type)
                mock_data = {
                    "tag": SetUp.tracing_tag,
                    "location": location_data,
                    "language": "Python",
                    "kind": "kind_data",
                    "name": "name_data",
                }
                result = setup.implementation.from_json(mock_level, mock_data, mock_schema_version)
                self.assertEqual(result.tag, SetUp.tracing_tag)
                self.assertEqual(result.language, "Python")
                self.assertEqual(result.kind, "kind_data")
                self.assertEqual(result.name, "name_data")
                if location_type == "file":
                            self.assertEqual(result.location.filename, location_data["file"])
                elif location_type == "github":
                    self.assertEqual(result.location.gh_root, location_data["gh_root"])
                    self.assertEqual(result.location.commit, location_data["commit"])
                    self.assertEqual(result.location.filename, location_data["file"])
                    self.assertEqual(result.location.line, location_data["line"])
                elif location_type == "codebeamer":
                    self.assertEqual(result.location.cb_root, location_data["cb_root"])
                    self.assertEqual(result.location.tracker, location_data["tracker"])
                    self.assertEqual(result.location.item, location_data["item"])
                    self.assertEqual(result.location.version, location_data["version"])
                    self.assertEqual(result.location.name, location_data["name"])

class TestActivity(unittest.TestCase):
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

        result = SetUp.activity.to_json()

        mock_super_to_json.assert_called_once_with()
        self.assertEqual(result, expected_result)

    @patch("lobster.items.Tracing_Tag.from_json")
    def test_from_json(self, mock_from_json):
        mock_level = "mock_level"
        mock_schema_version = 3
        setup = SetUp()
        mock_from_json.return_value = setup.tracing_tag
        for location_type in ["file", "github", "codebeamer", "void"]:
            with self.subTest(location_type):
                location_data = setup.set_location_data(location_type)
                mock_data = {
                    "tag": setup.tracing_tag,
                    "location": location_data,
                    "framework": "framework_data",
                    "kind": "kind_data",
                    "status": None
                }
                result = setup.activity.from_json(mock_level, mock_data, mock_schema_version)
                self.assertEqual(result.tag, setup.tracing_tag)
                self.assertEqual(result.framework, "framework_data")
                self.assertEqual(result.kind, "kind_data")
                self.assertEqual(result.status, None)
                if location_type == "file":
                    self.assertEqual(result.location.filename, location_data["file"])
                elif location_type == "github":
                    self.assertEqual(result.location.gh_root, location_data["gh_root"])
                    self.assertEqual(result.location.commit, location_data["commit"])
                    self.assertEqual(result.location.filename, location_data["file"])
                    self.assertEqual(result.location.line, location_data["line"])
                elif location_type == "codebeamer":
                    self.assertEqual(result.location.cb_root, location_data["cb_root"])
                    self.assertEqual(result.location.tracker, location_data["tracker"])
                    self.assertEqual(result.location.item, location_data["item"])
                    self.assertEqual(result.location.version, location_data["version"])
                    self.assertEqual(result.location.name, location_data["name"])

if __name__ == '__main__':
    unittest.main()
