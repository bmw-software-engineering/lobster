import argparse
import os
import unittest
from pathlib import Path, PurePosixPath, PureWindowsPath
from tempfile import NamedTemporaryFile, TemporaryDirectory

import yaml
from lobster.tools.json import json
from lobster.tools.json.json import LOBSTER_Json, Malformed_Input


class Test_Get_Item(unittest.TestCase):
    def test_empty_path_returns_root(self):
        # lobster-trace: json_req.Get_Item_Returns_Root_For_Empty_Path
        root = {"a": {"b": 42}}
        self.assertIs(json.get_item(root, "", required=True), root)

    def test_dotted_path_navigates_nested_dicts(self):
        # lobster-trace: json_req.Get_Item_Navigates_Dotted_Path
        root = {"a": {"b": {"c": "value"}}}
        self.assertEqual(json.get_item(root, "a.b.c", required=True), "value")

    def test_required_missing_key_raises(self):
        # lobster-trace: json_req.Get_Item_Required_Path_Not_Found_Raises
        with self.assertRaises(Malformed_Input):
            json.get_item({"a": 1}, "b", required=True)

    def test_required_non_object_raises(self):
        # lobster-trace: json_req.Get_Item_Required_Path_Not_Found_Raises
        with self.assertRaises(Malformed_Input):
            json.get_item("not-a-dict", "a", required=True)

    def test_optional_missing_key_returns_none(self):
        # lobster-trace: json_req.Get_Item_Optional_Path_Not_Found_Returns_None
        self.assertIsNone(json.get_item({"a": 1}, "b", required=False))

    def test_optional_non_object_returns_none(self):
        # lobster-trace: json_req.Get_Item_Optional_Path_Not_Found_Returns_None
        self.assertIsNone(json.get_item("not-a-dict", "a", required=False))


class Test_Syn_Test_Name(unittest.TestCase):
    def test_syn_test_name(self):
        # lobster-trace: json_req.Syn_Test_Name_Builds_Dotted_Name
        self.assertEqual(
            json.syn_test_name(PurePosixPath("foo/bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PurePosixPath("/foo/bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PureWindowsPath("foo\\bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PureWindowsPath("C:\\foo\\bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PurePosixPath("../../foo/./bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PureWindowsPath("..\\..\\foo\\.\\bar.json")),
            "foo.bar")


class Test_Build_Name(unittest.TestCase):
    def test_uses_name_attribute(self):
        # lobster-trace: json_req.Build_Name_Uses_Name_Attribute
        item = {"name": "My_Test"}
        self.assertEqual(
            json.build_name(item, "name", "file.json", 1),
            "My_Test")

    def test_rejects_non_string_name(self):
        # lobster-trace: json_req.Build_Name_Rejects_Non_String
        item = {"name": 42}
        with self.assertRaises(Malformed_Input):
            json.build_name(item, "name", "file.json", 1)

    def test_falls_back_to_synthetic_name(self):
        # lobster-trace: json_req.Build_Name_Falls_Back_To_Synthetic_Name
        item = {"unrelated": "value"}
        self.assertEqual(
            json.build_name(item, None, PurePosixPath("dir/file.json"), 3),
            "dir.file.3")


class Test_Load_Item(unittest.TestCase):
    def test_parses_valid_json_with_test_list(self):
        # lobster-trace: json_req.Load_Item_Parses_Valid_JSON
        with NamedTemporaryFile("w", suffix=".json", delete=False) as fd:
            fd.write('{"TestCases": [{"name": "a"}, {"name": "b"}]}')
            file_name = fd.name

        ok, data = json.load_item(file_name, "TestCases")
        self.assertTrue(ok)
        self.assertEqual(data, [{"name": "a"}, {"name": "b"}])

    def test_rejects_invalid_json(self):
        # lobster-trace: json_req.Load_Item_Rejects_Invalid_JSON
        with NamedTemporaryFile("w", suffix=".json", delete=False) as fd:
            fd.write("this is not json")
            file_name = fd.name

        ok, data = json.load_item(file_name, "")
        self.assertFalse(ok)
        self.assertEqual(data, [])


class Test_Process(unittest.TestCase):
    def _options(self, **overrides):
        options = argparse.Namespace(
            test_list=overrides.get("test_list", ""),
            name_attribute=overrides.get("name_attribute", None),
            tag_attribute=overrides.get("tag_attribute", "tags"),
            justification_attribute=overrides.get("justification_attribute", None),
        )
        return options

    def test_extracts_tags_given_as_string_or_list(self):
        # lobster-trace: json_req.Process_Extracts_Tags_As_List_Or_String
        with TemporaryDirectory() as tmp_dir:
            file_name = Path(tmp_dir) / "in.json"
            file_name.write_text(
                '[{"name": "a", "tags": "req-1"},'
                ' {"name": "b", "tags": ["req-2", "req-3"]}]')

            ok, items = LOBSTER_Json.process(
                self._options(name_attribute="name"), str(file_name))

            self.assertTrue(ok)
            self.assertEqual(len(items[0].unresolved_references), 1)
            self.assertEqual(len(items[1].unresolved_references), 2)

    def test_extracts_justification_given_as_string_or_list(self):
        # lobster-trace: json_req.Process_Extracts_Justification_As_List_Or_String
        with TemporaryDirectory() as tmp_dir:
            file_name = Path(tmp_dir) / "in.json"
            file_name.write_text(
                '[{"name": "a", "just": "reason-1"},'
                ' {"name": "b", "just": ["reason-2", "reason-3"]}]')

            ok, items = LOBSTER_Json.process(
                self._options(name_attribute="name",
                              justification_attribute="just"),
                str(file_name))

            self.assertTrue(ok)
            self.assertEqual(items[0].just_up, ["reason-1"])
            self.assertEqual(items[1].just_up, ["reason-2", "reason-3"])

    def test_aborts_file_on_load_failure(self):
        # lobster-trace: json_req.Process_Aborts_File_On_Load_Failure
        with TemporaryDirectory() as tmp_dir:
            file_name = Path(tmp_dir) / "in.json"
            file_name.write_text("this is not json")

            ok, items = LOBSTER_Json.process(self._options(), str(file_name))

            self.assertFalse(ok)
            self.assertEqual(items, [])


class Test_Config_Parameters(unittest.TestCase):
    def test_mandatory_parameters_requires_tag_attribute(self):
        # lobster-trace: json_req.Get_Mandatory_Parameters_Requires_Tag_Attribute
        lobster_json = LOBSTER_Json()
        self.assertEqual(lobster_json.get_mandatory_parameters(), {"tag_attribute"})

    def test_invalid_json_parameters(self):
        # lobster-trace: json_req.Config_Keys_Validation_Rejects_Unsupported_Keys
        config = {"invalid_key": "This is an invalid key "
                                  "which is not supported by LOBSTER Json"}
        lobster_json = LOBSTER_Json()

        with self.assertRaises(KeyError):
            lobster_json.validate_yaml_supported_config_parameters(config)

    def test_mandatory_json_parameters(self):
        # lobster-trace: json_req.Get_Mandatory_Parameters_Requires_Tag_Attribute
        config = {"single": True, "name_attribute": "fruit"}
        lobster_json = LOBSTER_Json()

        with self.assertRaises(SystemExit):
            lobster_json.check_mandatory_config_parameters(config)


class Test_Config_File_Handling(unittest.TestCase):
    def test_config_argparse_requires_config_option(self):
        # lobster-trace: json_req.Config_Argparse_Requires_Config_Option
        lobster_json = LOBSTER_Json()
        self.assertEqual(lobster_json.run([]), 2)

    def test_load_yaml_config_exits_when_file_missing(self):
        # lobster-trace: json_req.Load_Yaml_Config_Exits_When_File_Missing
        lobster_json = LOBSTER_Json()
        with self.assertRaises(SystemExit):
            lobster_json.load_yaml_config("/no/such/file.yaml")

    def test_load_yaml_config_propagates_yaml_syntax_errors(self):
        # lobster-trace: json_req.Load_Yaml_Config_Propagates_YAML_Syntax_Errors
        with NamedTemporaryFile("w", suffix=".yaml", delete=False) as fd:
            fd.write("a: : b")
            file_name = fd.name

        lobster_json = LOBSTER_Json()
        with self.assertRaises(yaml.YAMLError):
            lobster_json.load_yaml_config(file_name)


class Test_Process_Common_Options(unittest.TestCase):
    def _options(self, inputs=None, inputs_from_file=None):
        return argparse.Namespace(
            out=None,
            inputs=inputs if inputs is not None else [],
            inputs_from_file=inputs_from_file)

    def test_defaults_to_current_directory(self):
        # lobster-trace: json_req.Process_Common_Options_Defaults_To_Current_Directory
        with TemporaryDirectory() as tmp_dir:
            (Path(tmp_dir) / "a.json").write_text("{}")
            cwd = os.getcwd()
            try:
                os.chdir(tmp_dir)
                work_list = LOBSTER_Json().process_common_options(self._options())
            finally:
                os.chdir(cwd)

            self.assertEqual(work_list, [os.path.join(".", "a.json")])

    def test_uses_configured_inputs(self):
        # lobster-trace: json_req.Process_Common_Options_Uses_Configured_Inputs
        with TemporaryDirectory() as tmp_dir:
            wanted = Path(tmp_dir) / "wanted.json"
            wanted.write_text("{}")
            (Path(tmp_dir) / "unwanted.json").write_text("{}")

            work_list = LOBSTER_Json().process_common_options(
                self._options(inputs=[str(wanted)]))

            self.assertEqual(work_list, [str(wanted)])

    def test_reads_inputs_from_file(self):
        # lobster-trace: json_req.Process_Common_Options_Reads_Inputs_From_File
        with TemporaryDirectory() as tmp_dir:
            wanted = Path(tmp_dir) / "wanted.json"
            wanted.write_text("{}")
            list_file = Path(tmp_dir) / "list.txt"
            list_file.write_text(f"\n# a comment\n{wanted}\n")

            work_list = LOBSTER_Json().process_common_options(
                self._options(inputs_from_file=str(list_file)))

            self.assertEqual(work_list, [str(wanted)])

    def test_combines_inputs_and_inputs_from_file(self):
        # lobster-trace: json_req.Process_Common_Options_Combines_Inputs_And_Inputs_From_File
        with TemporaryDirectory() as tmp_dir:
            from_inputs = Path(tmp_dir) / "from_inputs.json"
            from_inputs.write_text("{}")
            from_file = Path(tmp_dir) / "from_file.json"
            from_file.write_text("{}")
            list_file = Path(tmp_dir) / "list.txt"
            list_file.write_text(str(from_file))

            work_list = LOBSTER_Json().process_common_options(
                self._options(inputs=[str(from_inputs)],
                              inputs_from_file=str(list_file)))

            self.assertEqual(sorted(work_list), sorted([str(from_inputs), str(from_file)]))

    def test_errors_on_invalid_path(self):
        # lobster-trace: json_req.Process_Common_Options_Errors_On_Invalid_Path
        with self.assertRaises(SystemExit) as ctx:
            LOBSTER_Json().process_common_options(
                self._options(inputs=["/no/such/path.json"]))
        self.assertEqual(ctx.exception.code, 1)

    def test_warns_on_wrong_extension(self):
        # lobster-trace: json_req.Process_Common_Options_Warns_On_Wrong_Extension
        with TemporaryDirectory() as tmp_dir:
            wrong_ext = Path(tmp_dir) / "data.txt"
            wrong_ext.write_text("{}")

            work_list = LOBSTER_Json().process_common_options(
                self._options(inputs=[str(wrong_ext)]))

            self.assertEqual(work_list, [str(wrong_ext)])

    def test_collect_files_from_directory_filters_by_extension(self):
        # lobster-trace: json_req.Collect_Files_From_Directory_Filters_By_Extension
        with TemporaryDirectory() as tmp_dir:
            nested = Path(tmp_dir) / "nested"
            nested.mkdir()
            (Path(tmp_dir) / "a.json").write_text("{}")
            (nested / "b.json").write_text("{}")
            (nested / "c.txt").write_text("not json")

            work_list = LOBSTER_Json().process_common_options(
                self._options(inputs=[tmp_dir]))

            self.assertEqual(len(work_list), 2)
            self.assertTrue(all(f.endswith(".json") for f in work_list))


if __name__ == "__main__":
    unittest.main()
