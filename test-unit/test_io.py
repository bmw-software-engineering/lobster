import unittest
from unittest.mock import ANY
import io
import json
from unittest.mock import patch, MagicMock, create_autospec, mock_open
from lobster.errors import Message_Handler
from lobster.location import File_Reference
from lobster.items import Tracing_Tag, Requirement, Implementation, Activity
from lobster.io import lobster_write, lobster_read
from lobster.location import Location

class SetUp(unittest.TestCase):
    mock_namespace = "mock_namespace"
    mock_tag = "mock_tag"
    mock_framework = "mock_framework"
    mock_kind = "mock_kind"
    mock_name = "mock_name"
    mock_language = "mock_language"
    mock_location = create_autospec(Location, instance = True)
    tracing_tag = Tracing_Tag(mock_namespace, mock_tag)
    requirement = Requirement(tracing_tag, mock_location, mock_framework, mock_kind, mock_name)
    implementation = Implementation(tracing_tag, mock_location, mock_language, mock_kind, mock_name)
    activity = Activity(tracing_tag, mock_location, mock_framework, mock_kind)

class TestLobsterWrite(unittest.TestCase):
    @patch("lobster.io.json")
    @patch("lobster.items.Tracing_Tag.to_json")
    @patch("lobster.items.Item.to_json")
    def test_lobster_write_requirement(self, mock_item_to_json, mock_tracing_tag_to_json, mock_json):
        self.generator = "mock_generator"
        mock_tracing_tag_to_json.return_value = "mock_value"
        mock_item_to_json.return_value = {
            "tag": "mock_value",
            "location": "mock_location",
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
                    
        items = [SetUp.requirement]
        exptected_value_req = {
            "tag": "mock_value",
            "location": "mock_location",
            "name": "mock_name",
            "messages": ["message1", "message2"],
            "just_up": True,
            "just_down": False,
            "just_global": True,
            "refs": ["mock_value"],
            "ref_up": ["mock_value"],
            "ref_down": ["mock_value"],
            "tracing_status": "mock_status",
            "framework": "mock_framework",
            "kind": "mock_kind",
            "text": None,
            "status": None
        }
        fd_req = io.StringIO()
        mock_data = {
            "data" : [exptected_value_req],
            "generator" : self.generator,
            "schema" : "lobster-req-trace",
            "version" : 4
        }
        lobster_write(fd_req, Requirement, self.generator, items)
        fd_req.seek(0)                    
        mock_json.dump.assert_called_once_with(mock_data, fd_req, indent=2)

    @patch("lobster.io.json")
    @patch("lobster.items.Tracing_Tag.to_json")
    @patch("lobster.items.Item.to_json")
    def test_lobster_write_implementation(self, mock_item_to_json, mock_tracing_tag_to_json, mock_json):
        self.generator = "mock_generator"
        mock_tracing_tag_to_json.return_value = "mock_value"
        mock_item_to_json.return_value = {
            "tag": "mock_value",
            "location": "mock_location",
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
        items = [SetUp.implementation]
        exptected_value_imp = {
            "tag": "mock_value",
            "location": "mock_location",
            "name": "mock_name",
            "messages": ["message1", "message2"],
            "just_up": True,
            "just_down": False,
            "just_global": True,
            "refs": ["mock_value"],
            "ref_up": ["mock_value"],
            "ref_down": ["mock_value"],
            "tracing_status": "mock_status",
            "language": "mock_language",
            "kind": "mock_kind"
        }
        fd_imp = io.StringIO()
        lobster_write(fd_imp, Implementation, self.generator, items)
        fd_imp.seek(0)
        mock_data = {
            "data" : [exptected_value_imp],
            "generator" : self.generator,
            "schema" : "lobster-imp-trace",
            "version" : 3
        }
        mock_json.dump.assert_called_once_with(mock_data, fd_imp, indent=2)

    @patch("lobster.io.json")
    @patch("lobster.items.Tracing_Tag.to_json")
    @patch("lobster.items.Item.to_json")
    def test_lobster_write_activity(self, mock_item_to_json, mock_tracing_tag_to_json, mock_json):
        self.generator = "mock_generator"
        mock_tracing_tag_to_json.return_value = "mock_value"
        mock_item_to_json.return_value = {
            "tag": "mock_value",
            "location": "mock_location",
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
        items = [SetUp.activity]
        exptected_value_act = {
            "tag": "mock_value",
            "location": "mock_location",
            "name": "mock_name",
            "messages": ["message1", "message2"],
            "just_up": True,
            "just_down": False,
            "just_global": True,
            "refs": ["mock_value"],
            "ref_up": ["mock_value"],
            "ref_down": ["mock_value"],
            "tracing_status": "mock_status",
            "framework": "mock_framework",
            "kind": "mock_kind",
            "status": None
        }
        fd_act = io.StringIO()
        lobster_write(fd_act, Activity, self.generator, items)
        fd_act.seek(0)
        mock_data = {
            "data" : [exptected_value_act],
            "generator" : self.generator,
            "schema" : "lobster-act-trace",
            "version" : 3
        }
        mock_json.dump.assert_called_once_with(mock_data, fd_act, indent=2)
    
    def setUp(self):
        self.mh = MagicMock(spec=Message_Handler)
        self.filename = "test.json"
        self.level = "test_level"
        self.items = {}
        self.source_info = None

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"schema": "lobster-req-trace", "version": 4, "generator": "mock_generator", "data": []}')
    def test_lobster_read_valid(self, mock_open, mock_isfile):        
        lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
        self.mh.error.assert_not_called()
        self.assertEqual(len(self.items), 0)

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"schema": "lobster-req-trace", "version": 4, "generator": "mock_generator"}')
    def test_lobster_read_missing_data_key(self, mock_open, mock_isfile):        
        lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
        # Allow any File_Reference object, but striclty check the string of the error message    
        self.mh.error.assert_called_with(ANY, "required top-level key data not present")

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid')
    def test_lobster_read_invalid_json(self, mock_open, mock_isfile):
        lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
        self.mh.error.assert_called()

    @patch("os.path.isfile", return_value=False)
    def test_lobster_read_file_not_found(self, mock_isfile):
        with self.assertRaises(AssertionError):
            lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
