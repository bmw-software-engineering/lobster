import unittest
from os.path import dirname
from pathlib import Path
from unittest.mock import ANY, MagicMock, Mock, patch

from trlc import ast
from trlc.ast import Package, Record_Object, Record_Type, Symbol_Table
from trlc.errors import Location, Message_Handler, TRLC_Error
from trlc.trlc import Source_Manager
from lobster.items import Requirement
from lobster.tools.trlc.trlc import Config_Parser


class LobsterTrlcTests(unittest.TestCase):
    def setUp(self):
        self.name = "mock_name"
        self.file_name = str(Path(dirname(__file__), "data", "lobster-trlc.conf"))
        self.description = "mock_description"
        self.mh = Message_Handler()
        self.sm = Source_Manager(self.mh)
        self.stab = Symbol_Table()
        self.config_string = "example.Requirement {description = description}"
        self.config_parser = Config_Parser(self.mh, self.config_string, self.stab)
        self.location = Location(self.file_name)
        self.n_package = Package(self.name, self.location, self.stab, False)
        self.n_typ = Record_Type(self.name, self.description, self.location, self.n_package, None, False)
        self.n_obj = Record_Object(self.name, self.location, self.n_typ, None, self.n_package)

    def test_generate_lobster_object_trace_false(self):
        # Test case 1: When trace is False
        self.config_parser.config[self.n_obj.n_typ] = {
            "trace": False
        }
        result = self.config_parser.generate_lobster_object(self.n_obj)
        self.assertIsNone(result)

    @patch("trlc.ast.Record_Object.to_python_dict")
    def test_generate_lobster_object_trace_true_single_description(self, mock_to_python_dict):
        # Test case 2: When trace is True and there is one description field
        mock_to_python_dict.return_value = {
            "field" : "value"
        }
        description_field = Mock(spec=ast.Composite_Component)
        description_field.name = "field"
        self.config_parser.config[self.n_obj.n_typ] = {
            "trace": True,
            "description_fields": [description_field],
            "tag_fields": [],
            "just_up_fields": [],
            "just_down_fields": [],
            "just_global_fields": []
        }

        result = self.config_parser.generate_lobster_object(self.n_obj)
        self.assertIsInstance(result, Requirement)
        self.assertEqual(result.tag.namespace, "req")
        self.assertEqual(result.tag.tag, "mock_name.mock_name")
        self.assertEqual(result.location.filename, self.file_name)
        self.assertEqual(result.location.line, None)
        self.assertEqual(result.location.column, None)
        self.assertEqual(result.framework, "TRLC")
        self.assertEqual(result.kind, self.n_obj.n_typ.name)
        self.assertEqual(result.name, "mock_name.mock_name")
        self.assertEqual(result.text, "value")
        self.assertEqual(len(result.just_up), 0)
        self.assertEqual(len(result.just_down), 0)
        self.assertEqual(len(result.just_global), 0)

    @patch("trlc.ast.Record_Object.to_python_dict")
    def test_generate_lobster_object_trace_true_multiple_description(self, mock_to_python_dict):
        # Test case 3: When trace is True and there are multiple description fields
        self.n_obj.location.line_no = 10
        self.n_obj.location.col_no = 5
        mock_to_python_dict.return_value = {
            "field1": "value1",
            "field2": "value2"
        }
        description_field1 = Mock(spec=ast.Composite_Component)
        description_field1.name = "field1"
        description_field2 = Mock(spec=ast.Composite_Component)
        description_field2.name = "field2"
        self.config_parser.config[self.n_obj.n_typ] = {
            "trace": True,
            "description_fields": [description_field1, description_field2],
            "tag_fields": [],
            "just_up_fields": [],
            "just_down_fields": [],
            "just_global_fields": []
        }

        result = self.config_parser.generate_lobster_object(self.n_obj)
        self.assertEqual(result.text, "field1: value1\n\nfield2: value2")
        self.assertIsInstance(result, Requirement)
        self.assertEqual(result.tag.namespace, "req")
        self.assertEqual(result.tag.tag, "mock_name.mock_name")
        self.assertEqual(result.location.filename, self.file_name)
        self.assertEqual(result.location.line, 10)
        self.assertEqual(result.location.column, 5)
        self.assertEqual(result.framework, "TRLC")
        self.assertEqual(result.kind, self.n_obj.n_typ.name)
        self.assertEqual(result.name, "mock_name.mock_name")
        self.assertEqual(len(result.just_up), 0)
        self.assertEqual(len(result.just_down), 0)
        self.assertEqual(len(result.just_global), 0)

    @patch("lobster.tools.trlc.trlc.Config_Parser.generate_text")
    @patch("trlc.ast.Record_Object.to_python_dict")
    def test_generate_lobster_object_trace_true_with_tag_field(
        self,
        mock_to_python_dict,
        mock_generate_text,
    ):
        # Test case 4: When there are tag fields
        tag_field = Mock(spec=ast.Composite_Component)
        tag_field.name = "tag_field"
        tag_field.n_typ = Mock(spec=ast.Array_Type)
        tag_field.n_typ.element_type = Mock(spec=ast.Tuple_Type)
        mock_generate_text.return_value = "tag_text"
        description_field = Mock(spec=ast.Composite_Component)
        description_field.name = "field"
        self.config_parser.config[self.n_obj.n_typ] = {
            "trace": True,
            "description_fields": [description_field],
            "tag_fields": [("namespace", tag_field)],
            "just_up_fields": [],
            "just_down_fields": [],
            "just_global_fields": []
        }
        mock_to_python_dict.return_value = {
            "field": "value",
            "tag_field": ["tag"]
        }
        result = self.config_parser.generate_lobster_object(self.n_obj)

        self.assertIsInstance(result, Requirement)
        self.assertEqual(result.unresolved_references[0].namespace, "namespace")
        self.assertEqual(result.unresolved_references[0].tag, "tag_text")
        self.assertEqual(len(result.just_up), 0)
        self.assertEqual(len(result.just_down), 0)
        self.assertEqual(len(result.just_global), 0)

    @patch("lobster.tools.trlc.trlc.Config_Parser.generate_text")
    @patch("trlc.ast.Record_Object.to_python_dict")
    def test_generate_lobster_object_trace_true_with_just_up_field(
        self,
        mock_to_python_dict,
        mock_generate_text,
    ):
        # Test case 4: When there are just_up field
        just_up_field = Mock(spec=ast.Composite_Component)
        just_up_field.name = "just_up_field"
        just_up_field.n_typ = Mock(spec=ast.Array_Type)
        just_up_field.n_typ.element_type = Mock(spec=ast.Tuple_Type)
        mock_generate_text.return_value = "just_up_text"
        description_field = Mock(spec=ast.Composite_Component)
        description_field.name = "field"
        self.config_parser.config[self.n_obj.n_typ] = {
            "trace": True,
            "description_fields": [description_field],
            "tag_fields": [],
            "just_up_fields": [just_up_field],
            "just_down_fields": [],
            "just_global_fields": []
        }
        mock_to_python_dict.return_value = {
            "field": "value",
            "just_up_field": ["just_up_field"]
        }
        result = self.config_parser.generate_lobster_object(self.n_obj)

        self.assertIsInstance(result, Requirement)
        self.assertEqual(result.just_up[0], "just_up_text")
        self.assertEqual(len(result.just_up), 1)
        self.assertEqual(len(result.just_down), 0)
        self.assertEqual(len(result.just_global), 0)

    def test_generate_text_with_undefined_tuple_type(self):
        n_typ = MagicMock(spec=ast.Tuple_Type)
        n_typ.location = self.location
        self.config_parser.to_string[n_typ] = ""
        mock_value = "mock_value"

        with self.assertRaises(TRLC_Error):
            self.config_parser.generate_text(n_typ, mock_value)
            self.config_parser.mh.error.assert_called_once_with(
                ANY,
                "please define a to_string function for this type in the lobster-trlc configuration file",
            )

    @patch("trlc.trlc.ast")
    def test_generate_text_with_non_tuple_type(self, mock_ast):
        mock_value = "mock_value"
        result = self.config_parser.generate_text(self.n_typ, mock_value)
        self.assertEqual(result, "mock_value")

    @patch("trlc.errors.Message_Handler.error")
    def test_generate_text_with_valid_tuple_type(self, mock_error):
        self.n_typ = MagicMock(spec=ast.Tuple_Type)
        self.n_typ.location = "test_location"
        func1 = ("text", "Hello, ")
        func2 = ("field", MagicMock(spec=ast.Composite_Component))
        func2[1].name = "field_name"
        func2[1].n_typ = MagicMock(spec=ast.Type)
        self.config_parser.to_string[self.n_typ] = [[func1, func2]]
        mock_value = {"field_name": "World!"}
        result = self.config_parser.generate_text(self.n_typ, mock_value)

        self.assertEqual(result, "Hello, World!")
        mock_error.assert_not_called()

    def test_generate_text_with_invalid_tuple_type(self):
        n_typ = MagicMock(spec=ast.Tuple_Type)
        n_typ.location = self.location
        func1 = ("text", "Hello, ")
        func2 = ("field", MagicMock(spec=ast.Composite_Component))
        func2[1].name = "field_name"
        func2[1].n_typ = MagicMock(spec=ast.Type)
        self.config_parser.to_string[n_typ] = [[func1, func2]]
        mock_value = {"field_name": None}

        with self.assertRaises(TRLC_Error):
            self.config_parser.generate_text(n_typ, mock_value)
            self.mh.error.assert_called_with(
                ANY,
                f"please define a to_string function that can render {mock_value}",
            )

if __name__ == '__main__':
    unittest.main()
