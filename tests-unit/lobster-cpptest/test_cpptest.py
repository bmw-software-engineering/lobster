import os
import unittest
from os.path import dirname
from pathlib import Path

from lobster.tools.cpptest.cpptest import *
from lobster.tools.cpptest.parser.constants import Constants
from lobster.tools.cpptest.parser.requirements_parser import ParserForRequirements


class LobsterCpptestTests(unittest.TestCase):
    # unit tests for lobster-cpptest

    def setUp(self):
        self.lobster_generator = Constants.LOBSTER_GENERATOR
        self.other_test_lobster_file = 'other_tests.lobster'
        self.unit_test_lobster_file = 'unit_tests.lobster'
        self.component_test_lobster_file = 'component_tests.lobster'
        self.test_fake_dir = str(Path(dirname(__file__), "not_existing"))
        self.test_data_dir = str(Path(dirname(__file__), "data"))
        self.test_case_file = str(Path(dirname(__file__), "data", "test_case.cpp"))
        self.test_config_1 = str(Path(dirname(__file__), "data", "test_1.config"))
        self.test_config_2 = str(Path(dirname(__file__), "data", "test_2.config"))

        self.req_test_type = [RequirementTypes.REQS.value]
        self.req_by_test_type = [RequirementTypes.REQ_BY.value]
        self.all_markers_data = {
            MARKERS: [RequirementTypes.REQS.value, RequirementTypes.REQ_BY.value],
            KIND: "req"
        }
        self.output_file_name = f'{self.lobster_generator}_{os.path.basename(self.test_case_file)}'
        self.output_file_name = self.output_file_name.replace('.', '_')
        self.output_file_name += '.lobster'

        self.output_fake_file_name = f'{self.lobster_generator}_{os.path.basename(self.test_fake_dir)}'
        self.output_fake_file_name = self.output_fake_file_name.replace('.', '_')
        self.output_fake_file_name += '.lobster'

        self.output_data_file_name = f'{self.lobster_generator}_{os.path.basename(self.test_data_dir)}'
        self.output_data_file_name = self.output_data_file_name.replace('.', '_')
        self.output_data_file_name += '.lobster'

        self.output_file_names = [self.output_file_name, self.output_fake_file_name,
                                  self.output_data_file_name, self.unit_test_lobster_file,
                                  self.component_test_lobster_file, self.other_test_lobster_file]

    def test_parse_config_file_with_two_markers_for_two_outputs(self):
        config_dict = parse_config_file(self.test_config_1)
        self.assertIsNotNone(config_dict)
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(2, len(config_dict))
        self.assertTrue(OUTPUT in config_dict.keys())

        output_config_dict = config_dict.get(OUTPUT)
        self.assertIsNotNone(output_config_dict)
        self.assertIsInstance(output_config_dict, dict)
        self.assertEqual(3, len(output_config_dict))
        self.assertTrue(self.component_test_lobster_file in output_config_dict.keys())
        self.assertTrue(self.unit_test_lobster_file in output_config_dict.keys())
        self.assertTrue(self.other_test_lobster_file in output_config_dict.keys())

        component_test_config_dict = output_config_dict.get(self.component_test_lobster_file)
        self.assertIsNotNone(component_test_config_dict)
        self.assertIsInstance(component_test_config_dict, dict)
        self.assertEqual(2, len(component_test_config_dict))
        self.assertTrue(MARKERS in component_test_config_dict.keys())
        self.assertTrue(KIND in component_test_config_dict.keys())

        component_test_markers_list = component_test_config_dict.get(MARKERS)
        self.assertIsNotNone(component_test_markers_list)
        self.assertIsInstance(component_test_markers_list, list)
        self.assertEqual(1, len(component_test_markers_list))
        self.assertTrue('@requirement' in component_test_markers_list)

        component_test_kind_value = component_test_config_dict.get(KIND)
        self.assertIsNotNone(component_test_kind_value)
        self.assertIsInstance(component_test_kind_value, str)
        self.assertEqual('req', component_test_kind_value)

        unit_test_config_dict = output_config_dict.get(self.unit_test_lobster_file)
        self.assertIsNotNone(unit_test_config_dict)
        self.assertIsInstance(unit_test_config_dict, dict)
        self.assertEqual(2, len(unit_test_config_dict))
        self.assertTrue(MARKERS in unit_test_config_dict.keys())
        self.assertTrue(KIND in unit_test_config_dict.keys())

        unit_test_markers_list = unit_test_config_dict.get(MARKERS)
        self.assertIsNotNone(unit_test_markers_list)
        self.assertIsInstance(unit_test_markers_list, list)
        self.assertEqual(1, len(unit_test_markers_list))
        self.assertTrue('@requiredby' in unit_test_markers_list)

        unit_test_kind_value = unit_test_config_dict.get(KIND)
        self.assertIsNotNone(unit_test_kind_value)
        self.assertIsInstance(unit_test_kind_value, str)
        self.assertEqual('req', unit_test_kind_value)

        other_test_config_dict = output_config_dict.get(self.other_test_lobster_file)
        self.assertIsNotNone(other_test_config_dict)
        self.assertIsInstance(other_test_config_dict, dict)
        self.assertEqual(2, len(other_test_config_dict))
        self.assertTrue(MARKERS in other_test_config_dict.keys())
        self.assertTrue(KIND in other_test_config_dict.keys())

        other_test_markers_list = other_test_config_dict.get(MARKERS)
        self.assertIsNotNone(other_test_markers_list)
        self.assertIsInstance(other_test_markers_list, list)
        self.assertEqual(0, len(other_test_markers_list))

        other_test_kind_value = other_test_config_dict.get(KIND)
        self.assertIsNotNone(other_test_kind_value)
        self.assertIsInstance(other_test_kind_value, str)
        self.assertEqual('', other_test_kind_value)

    def test_parse_config_file_with_two_markers_for_one_output(self):
        config_dict = parse_config_file(self.test_config_2)
        self.assertIsNotNone(config_dict)
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(2, len(config_dict))
        self.assertTrue(OUTPUT in config_dict.keys())

        output_config_dict = config_dict.get(OUTPUT)
        self.assertIsNotNone(output_config_dict)
        self.assertIsInstance(output_config_dict, dict)
        self.assertEqual(2, len(output_config_dict))
        self.assertTrue(self.component_test_lobster_file in output_config_dict.keys())
        self.assertTrue(self.other_test_lobster_file in output_config_dict.keys())

        component_test_config_dict = output_config_dict.get(self.component_test_lobster_file)
        self.assertIsNotNone(component_test_config_dict)
        self.assertIsInstance(component_test_config_dict, dict)
        self.assertEqual(2, len(component_test_config_dict))
        self.assertTrue(MARKERS in component_test_config_dict.keys())
        self.assertTrue(KIND in component_test_config_dict.keys())

        component_test_markers_list = component_test_config_dict.get(MARKERS)
        self.assertIsNotNone(component_test_markers_list)
        self.assertIsInstance(component_test_markers_list, list)
        self.assertEqual(2, len(component_test_markers_list))
        self.assertTrue('@requirement' in component_test_markers_list)
        self.assertTrue('@requiredby' in component_test_markers_list)

        component_test_kind_value = component_test_config_dict.get(KIND)
        self.assertIsNotNone(component_test_kind_value)
        self.assertIsInstance(component_test_kind_value, str)
        self.assertEqual('req', component_test_kind_value)

        other_test_config_dict = output_config_dict.get(self.other_test_lobster_file)
        self.assertIsNotNone(other_test_config_dict)
        self.assertIsInstance(other_test_config_dict, dict)
        self.assertEqual(2, len(other_test_config_dict))
        self.assertTrue(MARKERS in other_test_config_dict.keys())
        self.assertTrue(KIND in other_test_config_dict.keys())

        other_test_markers_list = other_test_config_dict.get(MARKERS)
        self.assertIsNotNone(other_test_markers_list)
        self.assertIsInstance(other_test_markers_list, list)
        self.assertEqual(0, len(other_test_markers_list))

        other_test_kind_value = other_test_config_dict.get(KIND)
        self.assertIsNotNone(other_test_kind_value)
        self.assertIsInstance(other_test_kind_value, str)
        self.assertEqual('', other_test_kind_value)

    def test_get_test_file_list(self):
        file_dir_list = [self.test_data_dir]
        extension_list = [".cpp", ".cc", ".c", ".h"]

        test_file_list = \
            get_test_file_list(
                file_dir_list=file_dir_list,
                extension_list=extension_list
            )

        self.assertIsNotNone(test_file_list)
        self.assertIsInstance(test_file_list, list)
        self.assertEqual(1, len(test_file_list))
        self.assertTrue(self.test_case_file in test_file_list)

    def test_get_test_file_list_no_file_with_matching_extension(self):
        file_dir_list = [self.test_data_dir]
        extension_list = [".xyz"]

        with self.assertRaises(Exception) as test_get_test_file_list:
            test_file_list = \
                get_test_file_list(
                    file_dir_list=file_dir_list,
                    extension_list=extension_list
                )

            self.assertIsNone(test_file_list)

        exception_string = str(test_get_test_file_list.exception)
        self.assertEqual(f'"{file_dir_list}" does not contain any test file.', exception_string)

    def test_get_test_file_list_not_existing_file_dir(self):
        file_dir_list = [self.test_fake_dir]
        extension_list = [".cpp", ".cc", ".c", ".h"]

        with self.assertRaises(Exception) as test_get_test_file_list:
            test_file_list = \
                get_test_file_list(
                    file_dir_list=file_dir_list,
                    extension_list=extension_list
                )

            self.assertIsNone(test_file_list)

        exception_string = str(test_get_test_file_list.exception)
        self.assertEqual(f'"{self.test_fake_dir}" is not a file or directory.', exception_string)

    def test_single_file(self):
        file_dir_list = [self.test_case_file]

        if os.path.exists(self.output_file_name):
            os.remove(self.output_file_name)

        file_exists = os.path.exists(self.output_file_name)
        self.assertFalse(file_exists)

        config_dict = {
            OUTPUT: {
                self.output_file_name: {
                    MARKERS: self.req_test_type,
                    KIND: "req"
                },
                self.other_test_lobster_file: {
                    MARKERS: [],
                    KIND: ''
                }
            },
            CODEBEAMER_URL: "https://codebeamer.com"
        }

        lobster_cpptest(
            file_dir_list=file_dir_list,
            config_dict=config_dict
        )

        file_exists = os.path.exists(self.output_file_name)
        self.assertTrue(file_exists)

    def test_single_directory(self):
        file_dir_list = [self.test_data_dir]

        if os.path.exists(self.output_data_file_name):
            os.remove(self.output_data_file_name)

        file_exists = os.path.exists(self.output_data_file_name)
        self.assertFalse(file_exists)

        config_dict = {
            OUTPUT: {
                self.output_data_file_name: {
                    MARKERS: self.req_test_type,
                    KIND: "req"
                },
                self.other_test_lobster_file: {
                    MARKERS: [],
                    KIND: ''
                }
            },
            CODEBEAMER_URL: "https://codebeamer.com"
        }

        lobster_cpptest(
            file_dir_list=file_dir_list,
            config_dict=config_dict
        )

        file_exists = os.path.exists(self.output_data_file_name)
        self.assertTrue(file_exists)

    def test_not_existing_file_dir(self):
        file_dir_list = [self.test_fake_dir]

        if os.path.exists(self.output_fake_file_name):
            os.remove(self.output_fake_file_name)

        file_exists = os.path.exists(self.output_fake_file_name)
        self.assertFalse(file_exists)

        config_dict = {
            OUTPUT: {
                self.output_file_name: {
                    MARKERS: self.req_test_type,
                    KIND: "req"
                }
            },
            CODEBEAMER_URL: "https://codebeamer.com"
        }

        with self.assertRaises(Exception) as wrapper:
            lobster_cpptest(
                file_dir_list=file_dir_list,
                config_dict=config_dict
            )

        exception_string = str(wrapper.exception)
        self.assertEqual(f'"{self.test_fake_dir}" is not a file or directory.', exception_string)

        file_exists = os.path.exists(self.output_fake_file_name)
        self.assertFalse(file_exists)

    def test_separate_output_config(self):
        file_dir_list = [self.test_case_file]
        config_dict: dict = parse_config_file(self.test_config_1)

        lobster_cpptest(
            file_dir_list=file_dir_list,
            config_dict=config_dict
        )

        self.assertEqual(os.path.exists(self.unit_test_lobster_file), True)

        with open(self.unit_test_lobster_file, "r") as unit_test_file:
            unit_test_lobster_file_dict = json.loads(unit_test_file.read())

        unit_test_lobster_items = unit_test_lobster_file_dict.get('data')
        self.assertIsNotNone(unit_test_lobster_items)
        self.assertIsInstance(unit_test_lobster_items, list)
        self.assertEqual(5, len(unit_test_lobster_items))

        # just check a few refs from the written unit test lobster items
        expected_unit_test_refs_dicts = {
            "cpp test_case.cpp:RequirementByTest1:130":
                ["req FOO0::BAR0", "req FOO1::BAR1"],
            "cpp test_case.cpp:RequirementByTest1:135":
                ["req FOO0::BAR0", "req FOO1::BAR1", "req FOO2::BAR2", "req FOO3::BAR3", "req FOO4::BAR4",
                 "req FOO5::BAR5", "req FOO6::BAR6", "req FOO7::BAR7", "req FOO8::BAR8"]
        }

        for lobster_item in unit_test_lobster_items:
            self.assertIsNotNone(lobster_item)
            self.assertIsInstance(lobster_item, dict)
            tag = lobster_item.get('tag')
            refs = lobster_item.get('refs')
            self.assertIsInstance(refs, list)
            if tag in expected_unit_test_refs_dicts.keys():
                expected_refs = expected_unit_test_refs_dicts.get(tag)
                self.assertListEqual(expected_refs, refs)

        self.assertEqual(os.path.exists(self.component_test_lobster_file), True)

        with open(self.component_test_lobster_file, "r") as component_test_file:
            component_test_lobster_file_dict = json.loads(component_test_file.read())

        component_test_lobster_items = component_test_lobster_file_dict.get('data')
        self.assertIsNotNone(component_test_lobster_items)
        self.assertIsInstance(component_test_lobster_items, list)
        self.assertEqual(9, len(component_test_lobster_items))

        # just check a few refs from the written component test lobster items
        expected_component_test_refs_dicts = {
            "cpp test_case.cpp:RequirementTagTest1:70":
                ["req 0815", "req 0816"],
            "cpp test_case.cpp:RequirementTagTest1:75":
                ["req 0815", "req 0816", "req 0817", "req 0818", "req 0819", "req 0820"]
        }

        for lobster_item in component_test_lobster_items:
            self.assertIsNotNone(lobster_item)
            self.assertIsInstance(lobster_item, dict)
            tag = lobster_item.get('tag')
            refs = lobster_item.get('refs')
            self.assertIsInstance(refs, list)
            if tag in expected_component_test_refs_dicts.keys():
                expected_refs = expected_component_test_refs_dicts.get(tag)
                self.assertListEqual(expected_refs, refs)

        self.assertEqual(os.path.exists(self.other_test_lobster_file), True)

        with open(self.other_test_lobster_file, "r") as other_test_file:
            other_test_lobster_file_dict = json.loads(other_test_file.read())

        other_test_lobster_items = other_test_lobster_file_dict.get('data')
        self.assertIsNotNone(other_test_lobster_items)
        self.assertIsInstance(other_test_lobster_items, list)
        self.assertEqual(32, len(other_test_lobster_items))

    def test_test_case_parsing(self):
        """
        Verify that the test case parsing is working correctly
        The whole TestCase class is tested as one since the test_file contains all possible
        variant of an allowed test case implementation
        """
        codebeamer_url = "https://codebeamer.com"
        expect = [
            # Verify that test macros, test suite, test name and documentation comments are correctly parsed
            {"suite": "TestMacrosTest", "test_name": "TestPInstance",
             "docu_start": 3, "docu_end": 3, "def_start": 3, "def_end": 3},
            {"suite": "TestMacrosTest", "test_name": "TestTest",
             "docu_start": 4, "docu_end": 4, "def_start": 4, "def_end": 4},
            {"suite": "TestMacrosTest1", "test_name": "TestTestF",
             "docu_start": 5, "docu_end": 5, "def_start": 5, "def_end": 5},
            {"suite": "TestMacrosTest1", "test_name": "TestTestP",
             "docu_start": 6, "docu_end": 6, "def_start": 6, "def_end": 6},
            {"suite": "TestMacrosTest2", "test_name": "TestTypedTest",
             "docu_start": 7, "docu_end": 7, "def_start": 7, "def_end": 7},
            {"suite": "TestMacrosTest2", "test_name": "TestTypedTestP",
             "docu_start": 8, "docu_end": 8, "def_start": 8, "def_end": 8},
            {"suite": "TestMacrosTest2", "test_name": "TestTypedTestSuite",
             "docu_start": 9, "docu_end": 9, "def_start": 9, "def_end": 9},
            {"suite": "TestMacrosTest3", "test_name": "TestFInstance",
             "docu_start": 10, "docu_end": 10, "def_start": 10, "def_end": 10},
            # Verify that test implementation is correctly parsed (def_start, def_end)
            {"suite": "ImplementationTest", "test_name": "TestMultiLine",
             "docu_start": 14, "docu_end": 14, "def_start": 14, "def_end": 17},
            {"suite": "ImplementationTest", "test_name": "EmptyImplementation",
             "docu_start": 19,  "docu_end": 19, "def_start": 19, "def_end": 19},
            {"suite": "ImplementationTest", "test_name": "ImplementationMultipleLines",
             "docu_start": 21, "docu_end": 21, "def_start": 21, "def_end": 23},
            {"suite": "ImplementationTest", "test_name": "MultipleLinesWithComments",
             "docu_start": 25, "docu_end": 25, "def_start": 25, "def_end": 30},
            # Verify that the test tag is correctly parsed
            {"suite": "TestTagTest", "test": "foo1", "test_name": "TestTagInOnline"},
            {"suite": "TestTagTest", "test": "foo2", "test_name": "TestTagPrecededByComment"},
            {"suite": "TestTagTest", "test": "foo3", "test_name": "TestTagFollowedByComment"},
            {"suite": "TestTagTest", "test": "foo4", "test_name": "TestTagWithCommentsAround"},
            {"suite": "TestTagTest", "test": "lorem ipsum", "test_name": "TestTagAsText"},
            # Verify that the brief tag is correctly parsed
            {"suite": "BriefTagTest", "brief": "Some nasty bug1", "test_name": "BriefTagInOnline"},
            {"suite": "BriefTagTest", "brief": "This is a brief field with a long description",
             "test_name": "BriefTagMultipleLines"},
            # Verify that the requirement tags are correctly parsed
            {"suite": "RequirementTagTest", "test_name": "Requirement",
             "req": ["CB-#0815"]},
            {"suite": "RequirementTagTest1", "test_name": "RequirementAsOneLineComments",
             "req": ["CB-#0815", "CB-#0816"]},
            {"suite": "RequirementTagTest1", "test_name": "RequirementAsComments",
             "req": ["CB-#0815", "CB-#0816"]},
            {"suite": "RequirementTagTest1", "test_name": "RequirementsAsMultipleComments",
             "req": ["CB-#0815", "CB-#0816", "CB-#0817", "CB-#0818", "CB-#0819", "CB-#0820"]},
            {"suite": "RequirementTagTest2", "test_name": "URLRequirement",
             "req": []},
            {"suite": "RequirementTagTest2", "test_name": "URLRequirementsCommaSeparated",
             "req": []},
            {"suite": "RequirementTagTest2", "test_name": "URLRequirementsAsCommentsSpaceSeparated",
             "req": []},
            {"suite": "RequirementTagTest2", "test_name": "MultipleURLRequirements",
             "req": []},
            {"suite": "RequirementTagTest3", "test_name": "MixedRequirements",
             "req": ["CB-#0816"]},
            {"suite": "RequirementTagTest4", "test_name": "InvalidRequirement",
             "req": []},
            {"suite": "RequirementTagTest4", "test_name": "MissingRequirementReference",
             "req": []},
            # Verify that the required-by tag is correctly parsed
            {"suite": "RequirementByTest1", "test_name": "RequiredByWithAt",
             "req_by": ["FOO0::BAR0"]},
            {"suite": "RequirementByTest1", "test_name": "MultipleRequiredByCommaSeparated",
             "req_by": ["FOO0::BAR0", "FOO1::BAR1"]},
            {"suite": "RequirementByTest1", "test_name": "MultipleRequiredByAsComments",
             "req_by": ["FOO0::BAR0", "FOO1::BAR1", "FOO2::BAR2", "FOO3::BAR3", "FOO4::BAR4", "FOO5::BAR5",
                        "FOO6::BAR6", "FOO7::BAR7", "FOO8::BAR8"]},
            {"suite": "RequirementByTest2", "test_name": "RequiredByWithNewLines",
             "req_by": ["FOO0::BAR0", "FOO1::BAR1", "FOO2::BAR2", "FOO3::BAR3", "FOO4::BAR4", "FOO5::BAR5",
                        "FOO6::BAR6", "FOO7::BAR7", "FOO8::BAR8"]},
            # Verify that the test methods tag is correctly parsed
            {"suite": "TestMethodsTagTest", "test_name": "TestMethod",
             "testmethods": ["TM_REQUIREMENT"]},
            {"suite": "TestMethodsTagTest2", "test_name": "TestMethodAsCommentsSpaceSeparated",
             "testmethods": ["TM_PAIRWISE", "TM_BOUNDARY"]},
            {"suite": "TestMethodsTagTest2", "test_name": "TestMethodAsCommentsCommaSeparated",
             "testmethods": ["TM_REQUIREMENT", "TM_EQUIVALENCE"]},
            {"suite": "TestMethodsTagTest3", "test_name": "InvalidTestMethod", "testmethods": []},
            {"suite": "TestMethodsTagTest4", "test_name": "MissingTestMethod", "testmethods": []},
            # Verify that the version tag is correctly parsed
            {"suite": "VersionTagTest", "test_name": "VersionTagTestInOnline", "version": ["1"]},
            {"suite": "VersionTagTest", "test_name": "MultipleVersionTagTestInOnline", "version": ["1", "42"]},
            {"suite": "VersionTagTest", "test_name": "MoreVersionsThanRequirements", "version": ["12", "70"],
             "req": ["CB-#0815"]},
            {"suite": "VersionTagTest", "test_name": "MoreRequirementsThanVersions", "version": ["28", "28"],
             "req": ["CB-#0815", "CB-#0816"]},
            {"suite": "VersionTagTest", "test_name": "VersionSpaceSeparated", "version": ["28", "99"],
             "req": ["CB-#123", "CB-#456"]},
            # Verify that all at once is correctly parsed
            {"suite": "AllTogetherTest", "test_name": "ImplementationMultipleLines",
             "docu_start": 207, "docu_end": 214, "def_start": 215, "def_end": 217, "version": ["42", "2"],
             "test": "foo", "brief": "this test tests something",
             "req": ["CB-#0815", "CB-#0816"],
             "req_by": ["FOO0::BAR0"], "testmethods": ["TM_BOUNDARY", "TM_REQUIREMENT"]}
        ]

        test_cases = ParserForRequirements.collect_test_cases(self.test_case_file, codebeamer_url)
        self.assertEqual(len(test_cases), 45)

        for i in range(0, len(expect)):
            self.assertEqual(test_cases[i].file_name, self.test_case_file)
            self.assertEqual(test_cases[i].suite_name, expect[i]["suite"])
            self.assertEqual(test_cases[i].test_name, expect[i]["test_name"])
            if "docu_start" in expect[i]:
                self.assertEqual(
                    test_cases[i].docu_start_line,
                    expect[i]["docu_start"],
                    "docu_start does not match for test_name " + test_cases[i].test_name,
                )
                self.assertEqual(
                    test_cases[i].docu_end_line,
                    expect[i]["docu_end"],
                    "docu_end does not match for test_name " + test_cases[i].test_name,
                )
                self.assertEqual(
                    test_cases[i].definition_start_line,
                    expect[i]["def_start"],
                    "def_start does not match for test_name " + test_cases[i].test_name,
                )
                self.assertEqual(
                    test_cases[i].definition_end_line,
                    expect[i]["def_end"],
                    "def_end does not match for test_name " + test_cases[i].test_name,
                )
            if "req" in expect[i]:
                self.assertEqual(
                    test_cases[i].requirements,
                    expect[i]["req"],
                    "req does not match for test_name " + test_cases[i].test_name,
                )
            if "req_by" in expect[i]:
                self.assertEqual(
                    test_cases[i].required_by,
                    expect[i]["req_by"],
                    "req_by does not match for test_name " + test_cases[i].test_name,
                )
            if "version" in expect[i]:
                self.assertEqual(
                    test_cases[i].version_id,
                    expect[i]["version"],
                    "version does not match for test_name " + test_cases[i].test_name,
                )
            if "test" in expect[i]:
                self.assertEqual(
                    test_cases[i].test,
                    expect[i]["test"],
                    "test does not match for test_name " + test_cases[i].test_name,
                )
            if "testmethods" in expect[i]:
                self.assertEqual(
                    test_cases[i].testmethods,
                    expect[i]["testmethods"],
                    "testmethods does not match for test_name " + test_cases[i].test_name,
                )
            if "brief" in expect[i]:
                self.assertEqual(
                    test_cases[i].brief,
                    expect[i]["brief"],
                    "brief does not match for test_name " + test_cases[i].test_name,
                )

    def tearDown(self):
        # lobster-trace: cpptest_req.Dummy_Requirement_Unit_Test
        for output_file in self.output_file_names:
            if os.path.exists(output_file):
                os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
