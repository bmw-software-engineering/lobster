import unittest
import io
import json
from unittest.mock import patch, create_autospec, mock_open, ANY
from lobster.errors import Message_Handler, LOBSTER_Error
from lobster.location import File_Reference
from lobster.items import Tracing_Tag, Requirement, Implementation, Activity
from lobster.io import lobster_write, lobster_read
from lobster.location import Location

class LobsterWriteReadTests(unittest.TestCase):
    # unit tests for io.py file

    def setUp(self):
        self.mock_namespace = "mock_namespace"
        self.mock_tag = "mock_tag"
        self.mock_framework = "mock_framework"
        self.mock_kind = "mock_kind"
        self.mock_name = "mock_name"
        self.mock_language = "mock_language"
        self.mock_location = create_autospec(Location, instance = True)
        self.tracing_tag = Tracing_Tag(self.mock_namespace, self.mock_tag)
        self.requirement = Requirement(
            self.tracing_tag,
            self.mock_location,
            self.mock_framework,
            self.mock_kind,
            self.mock_name,
        )
        self.implementation = Implementation(
            self.tracing_tag,
            self.mock_location,
            self.mock_language,
            self.mock_kind,
            self.mock_name,
        )
        self.activity = Activity(
            self.tracing_tag,
            self.mock_location,
            self.mock_framework,
            self.mock_kind,
        )
        self.mh = Message_Handler()
        self.filename = "test.json"
        self.level = "test_level"
        self.items = {}
        self.source_info = None
        self.source_data = {
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
        }

    @patch("lobster.io.json")
    @patch("lobster.items.Tracing_Tag.to_json")
    @patch("lobster.items.Item.to_json")
    def test_lobster_write_requirement(self, mock_item_to_json, mock_tracing_tag_to_json, mock_json):
        generator = "mock_generator"
        mock_tracing_tag_to_json.return_value = "mock_value"
        self.source_data["tracing_status"] = "mock_status"
        mock_item_to_json.return_value = self.source_data
        items = [self.requirement]
        self.source_data["tracing_status"] = "mock_status"
        self.source_data["framework"] = "mock_framework"
        self.source_data["kind"] = "mock_kind"
        self.source_data["text"] = None
        self.source_data["status"] = None
        fd_req = io.StringIO()
        mock_data = {
            "data" : [self.source_data],
            "generator" : generator,
            "schema" : "lobster-req-trace",
            "version" : 4
        }
        lobster_write(fd_req, Requirement, generator, items)
        fd_req.seek(0)
        mock_json.dump.assert_called_once_with(mock_data, fd_req, indent=2)

    @patch("lobster.io.json")
    @patch("lobster.items.Tracing_Tag.to_json")
    @patch("lobster.items.Item.to_json")
    def test_lobster_write_implementation(self, mock_item_to_json, mock_tracing_tag_to_json, mock_json):
        generator = "mock_generator"
        mock_tracing_tag_to_json.return_value = "mock_value"
        self.source_data["tracing_status"] = "mock_status"
        mock_item_to_json.return_value = self.source_data
        items = [self.implementation]
        self.source_data["tracing_status"] = "mock_status"
        self.source_data["language"] = "mock_language"
        self.source_data["kind"] = "mock_kind"
        fd_imp = io.StringIO()
        lobster_write(fd_imp, Implementation, generator, items)
        fd_imp.seek(0)
        mock_data = {
            "data" : [self.source_data],
            "generator" : generator,
            "schema" : "lobster-imp-trace",
            "version" : 3
        }
        mock_json.dump.assert_called_once_with(mock_data, fd_imp, indent=2)

    @patch("lobster.io.json")
    @patch("lobster.items.Tracing_Tag.to_json")
    @patch("lobster.items.Item.to_json")
    def test_lobster_write_activity(self, mock_item_to_json, mock_tracing_tag_to_json, mock_json):
        generator = "mock_generator"
        mock_tracing_tag_to_json.return_value = "mock_value"
        self.source_data["tracing_status"] = "mock_status"
        mock_item_to_json.return_value = self.source_data
        items = [self.activity]
        self.source_data["tracing_status"] = "mock_status"
        self.source_data["framework"] = "mock_framework"
        self.source_data["kind"] = "mock_kind"
        self.source_data["status"] = None
        fd_act = io.StringIO()
        lobster_write(fd_act, Activity, generator, items)
        fd_act.seek(0)
        mock_data = {
            "data" : [self.source_data],
            "generator" : generator,
            "schema" : "lobster-act-trace",
            "version" : 3
        }
        mock_json.dump.assert_called_once_with(mock_data, fd_act, indent=2)

    @patch("lobster.items.Item.additional_data_from_json")
    @patch("lobster.items.Tracing_Tag.key")
    @patch("lobster.items.Tracing_Tag.from_json")
    def test_lobster_read_valid_requirement(self, mock_from_json, mock_key, mock_additional_data_from_json):
        mock_key.return_value = "mock_namespace mock_tag"
        mock_from_json.return_value = self.tracing_tag
        self.source_data.update({"location" : {
                    "kind": "file",
                    "file": "example.txt"
                }})
        self.source_data["tracing_status"] = "mock_status"
        self.source_data["framework"] = "mock_framework"
        self.source_data["kind"] = "mock_kind"
        self.source_data["text"] = None
        self.source_data["status"] = None
        mock_data_req = {
            "schema" : "lobster-req-trace",
            "version" : 4,
            "generator" : "mock_generator",
            "data" : [self.source_data]
            }
        read_data = json.dumps(mock_data_req, indent=4)
        with patch("os.path.isfile", return_value=True):
            with patch("builtins.open", mock_open(read_data=read_data)):
                lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
                self.assertEqual(len(self.items), 1)
                mock_additional_data_from_json.assert_called_once_with(
                    self.level,
                    self.source_data, mock_data_req["version"],
                )

    @patch("lobster.items.Item.additional_data_from_json")
    @patch("lobster.items.Tracing_Tag.key")
    @patch("lobster.items.Tracing_Tag.from_json")
    def test_lobster_read_valid_implementation(
        self,
        mock_from_json, mock_key,
        mock_additional_data_from_json,
    ):
        mock_key.return_value = "mock_namespace mock_tag"
        mock_from_json.return_value = self.tracing_tag
        self.source_data.update({"location" : {
                    "kind": "file",
                    "file": "example.txt"
                }})
        self.source_data["tracing_status"] = "mock_status"
        self.source_data["language"] = "mock_language"
        self.source_data["kind"] = "mock_kind"
        mock_data_imp = {
            "schema" : "lobster-imp-trace",
            "version" : 3,
            "generator" : "mock_generator",
            "data" : [self.source_data]
            }
        read_data = json.dumps(mock_data_imp, indent=4)
        with patch("os.path.isfile", return_value=True):
            with patch("builtins.open", mock_open(read_data=read_data)):
                lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
                self.assertEqual(len(self.items), 1)
                mock_additional_data_from_json.assert_called_once_with(
                    self.level,
                    self.source_data, mock_data_imp["version"],
                )

    @patch("lobster.items.Item.additional_data_from_json")
    @patch("lobster.items.Tracing_Tag.key")
    @patch("lobster.items.Tracing_Tag.from_json")
    def test_lobster_read_valid_activity(self, mock_from_json, mock_key, mock_additional_data_from_json):
        mock_key.return_value = "mock_namespace mock_tag"
        mock_from_json.return_value = self.tracing_tag
        self.source_data.update({"location" : {
                    "kind": "file",
                    "file": "example.txt"
                }})
        self.source_data["tracing_status"] = "mock_status"
        self.source_data["framework"] = "mock_framework"
        self.source_data["kind"] = "mock_kind"
        self.source_data["status"] = None
        mock_data_act = {
            "schema" : "lobster-act-trace",
            "version" : 3,
            "generator" : "mock_generator",
            "data" : [self.source_data]
            }
        read_data = json.dumps(mock_data_act, indent=4)
        with patch("os.path.isfile", return_value=True):
            with patch("builtins.open", mock_open(read_data=read_data)):
                lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
                self.assertEqual(len(self.items), 1)
                mock_additional_data_from_json.assert_called_once_with(
                    self.level,
                    self.source_data, mock_data_act["version"],
                )

    @patch("os.path.isfile", return_value=True)
    @patch(
        "builtins.open",
        new_callable=unittest.mock.mock_open,
        read_data='{"schema": "lobster-req-trace", "version": 4, "generator": "mock_generator"}',
    )
    def test_lobster_read_missing_data_key(self, mock_file_open, mock_isfile):
        with self.assertRaises(LOBSTER_Error):
            lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
            self.mh.error.assert_called_with(ANY, "required top-level key data not present")

    @patch("os.path.isfile", return_value=True)
    @patch(
        "builtins.open",
        new_callable=unittest.mock.mock_open,
        read_data='{"schema": "lobster-req-trace", "version": 5, "generator": "test_gen", "data": []}',
    )
    def test_lobster_read_unsupported_version(self, mock_file_open, mock_isfile):
        with self.assertRaises(LOBSTER_Error):
            lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
            self.mh.error.assert_called_with(
                File_Reference(self.filename),
                "version 5 for schema lobster-req-trace is not supported",
            )

    @patch("os.path.isfile", return_value=True)
    @patch(
        "builtins.open",
        new_callable=unittest.mock.mock_open,
        read_data='{"schema": "unknown-schema", "version": 4, "generator": "test_gen", "data": []}',
    )
    def test_lobster_read_unknown_schema(self, mock_file_open, mock_isfile):
        with self.assertRaises(LOBSTER_Error):
            lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid')
    def test_lobster_read_invalid_json(self, mock_file_open, mock_isfile):
        with self.assertRaises(LOBSTER_Error):
            lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)

    @patch("os.path.isfile", return_value=False)
    def test_lobster_read_file_not_found(self, mock_isfile):
        with self.assertRaises(FileNotFoundError):
            lobster_read(self.mh, self.filename, self.level, self.items, self.source_info)
