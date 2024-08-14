import json
import os
import unittest
from pathlib import Path

from lobster.tools.cpp_doxygen.cpp_doxygen import get_test_file_list, collect_test_cases_from_test_files, \
    create_lobster_implementations_dict_from_test_cases, write_lobster_implementations_to_output, \
    LOBSTER_GENERATOR, lobster_cpp_doxygen, RequirementTypes, parse_cpp_config_file

from lobster.tools.cpp_doxygen.parser.requirements_parser import ParserForRequirements


class LobsterCppDoxygenTests(unittest.TestCase):

    def setUp(self):
        self.unittest_lobster_file = 'unit_tests.lobster'
        self.componenttest_lobster_file = 'component_tests.lobster'
        self.test_fake_dir = str(Path('./not_existing'))
        self.test_data_dir = str(Path('./data'))
        self.test_case_file_dir = str(Path('./data', 'test_case.cpp'))
        self.test_config1_dir = str(Path('./data', 'test_cpp1.config'))
        self.test_config2_dir = str(Path('./data', 'test_cpp2.config'))

        self.req_test_type = [RequirementTypes.REQS.value]
        self.req_by_test_type = [RequirementTypes.REQ_BY.value]
        self.all_test_types = [RequirementTypes.REQS.value, RequirementTypes.REQ_BY.value]

        self.output_file_name = f'{LOBSTER_GENERATOR}_{os.path.basename(self.test_case_file_dir)}'
        self.output_file_name = self.output_file_name.replace('.', '_')
        self.output_file_name += '.lobster'

        self.output_fake_file_name = f'{LOBSTER_GENERATOR}_{os.path.basename(self.test_fake_dir)}'
        self.output_fake_file_name = self.output_fake_file_name.replace('.', '_')
        self.output_fake_file_name += '.lobster'

        self.output_data_file_name = f'{LOBSTER_GENERATOR}_{os.path.basename(self.test_data_dir)}'
        self.output_data_file_name = self.output_data_file_name.replace('.', '_')
        self.output_data_file_name += '.lobster'

        self.output_file_names = [self.output_file_name, self.output_fake_file_name,
                                  self.output_data_file_name, self.unittest_lobster_file,
                                  self.componenttest_lobster_file]

    def test_parse_cpp_config_file_with_different_files(self):
        cpp_output_config = parse_cpp_config_file(self.test_config1_dir)
        self.assertIsNotNone(cpp_output_config)
        self.assertIsInstance(cpp_output_config, dict)
        self.assertEqual(2, len(cpp_output_config))
        self.assertTrue(self.componenttest_lobster_file in cpp_output_config)
        self.assertTrue(self.unittest_lobster_file in cpp_output_config)
        self.assertEqual(1, len(cpp_output_config.get(self.componenttest_lobster_file)))
        self.assertEqual(1, len(cpp_output_config.get(self.unittest_lobster_file)))

    def test_parse_cpp_config_file_with_same_files(self):
        cpp_output_config = parse_cpp_config_file(self.test_config2_dir)
        self.assertIsNotNone(cpp_output_config)
        self.assertIsInstance(cpp_output_config, dict)
        self.assertEqual(1, len(cpp_output_config))
        self.assertTrue(self.componenttest_lobster_file in cpp_output_config)
        self.assertEqual(2, len(cpp_output_config.get(self.componenttest_lobster_file)))

    def test_get_test_file_list(self):
        file_dir_list = [self.test_data_dir ]
        extension_list = [".cpp", ".cc", ".c", ".h"]

        test_file_list, error_list = \
            get_test_file_list(
                file_dir_list=file_dir_list,
                extension_list=extension_list
            )

        self.assertIsNotNone(test_file_list)
        self.assertIsInstance(test_file_list, list)
        self.assertEqual(1, len(test_file_list))
        self.assertTrue('data\\test_case.cpp' in test_file_list)

        self.assertIsNotNone(error_list)
        self.assertIsInstance(error_list, list)
        self.assertEqual(0, len(error_list))

    def test_get_test_file_list_no_file_with_matching_extension(self):
        file_dir_list = [self.test_data_dir ]
        extension_list = [".xyz"]

        test_file_list, error_list = \
            get_test_file_list(
                file_dir_list=file_dir_list,
                extension_list=extension_list
            )

        self.assertIsNotNone(test_file_list)
        self.assertIsInstance(test_file_list, list)
        self.assertEqual(0, len(test_file_list))

        self.assertIsNotNone(error_list)
        self.assertIsInstance(error_list, list)
        self.assertEqual(1, len(error_list))
        self.assertTrue(f'"{file_dir_list}" does not contain any test file' in error_list)

    def test_get_test_file_list_not_existing_file_dir(self):
        file_dir_list = [self.test_fake_dir]
        extension_list = [".cpp", ".cc", ".c", ".h"]

        test_file_list, error_list = \
            get_test_file_list(
                file_dir_list=file_dir_list,
                extension_list=extension_list
            )

        self.assertIsNotNone(test_file_list)
        self.assertIsInstance(test_file_list, list)
        self.assertEqual(0, len(test_file_list))

        self.assertIsNotNone(error_list)
        self.assertIsInstance(error_list, list)
        self.assertEqual(2, len(error_list))
        self.assertTrue('"not_existing" is not a file or directory' in error_list)
        self.assertTrue(f'"{file_dir_list}" does not contain any test file' in error_list)

    def test_lobster_cpp_doxygen_single_file(self):
        file_dir_list = [self.test_case_file_dir]

        if os.path.exists(self.output_file_name):
            os.remove(self.output_file_name)

        file_exists = os.path.exists(self.output_file_name)
        self.assertFalse(file_exists)

        output_config = {self.output_file_name: self.req_test_type}

        error_list = \
            lobster_cpp_doxygen(
                file_dir_list=file_dir_list,
                output_config=output_config
            )

        self.assertIsNotNone(error_list)
        self.assertIsInstance(error_list, list)
        self.assertEqual(0, len(error_list))

        file_exists = os.path.exists(self.output_file_name)
        self.assertTrue(file_exists)

    def test_lobster_cpp_doxygen_single_directory(self):
        file_dir_list = [self.test_data_dir]

        if os.path.exists(self.output_data_file_name):
            os.remove(self.output_data_file_name)

        file_exists = os.path.exists(self.output_data_file_name)
        self.assertFalse(file_exists)

        output_config = {self.output_data_file_name: self.req_test_type}

        error_list = \
            lobster_cpp_doxygen(
                file_dir_list=file_dir_list,
                output_config=output_config
            )

        self.assertIsNotNone(error_list)
        self.assertIsInstance(error_list, list)
        self.assertEqual(0, len(error_list))

        file_exists = os.path.exists(self.output_data_file_name)
        self.assertTrue(file_exists)

    def test_lobster_cpp_doxygen_not_existing_file_dir(self):
        file_dir_list = [self.test_fake_dir]

        if os.path.exists(self.output_fake_file_name):
            os.remove(self.output_fake_file_name)

        file_exists = os.path.exists(self.output_fake_file_name)
        self.assertFalse(file_exists)
        output_config = {self.output_fake_file_name: self.req_test_type}

        error_list = \
            lobster_cpp_doxygen(
                file_dir_list=file_dir_list,
                output_config=output_config
            )

        self.assertIsNotNone(error_list)
        self.assertIsInstance(error_list, list)
        self.assertEqual(2, len(error_list))

        file_exists = os.path.exists(self.output_fake_file_name)
        self.assertFalse(file_exists)

    def test_lobster_cpp_doxygen_multiple_files(self):
        file_dir_list = [self.test_case_file_dir]
        cpp_output_config = parse_cpp_config_file(self.test_config1_dir)
        error_list = \
            lobster_cpp_doxygen(
                file_dir_list=file_dir_list,
                output_config=cpp_output_config
            )
        self.assertIsNotNone(error_list)
        self.assertIsInstance(error_list, list)
        self.assertEqual(0, len(error_list))
        self.assertEqual(os.path.exists(self.unittest_lobster_file), True)
        self.assertEqual(os.path.exists(self.componenttest_lobster_file), True)

        with open(self.unittest_lobster_file, "r") as unittest_file:
            unittest_file_data = json.loads(unittest_file.read())
        with open(self.componenttest_lobster_file, "r") as componenttest_file:
            componenttest_file_data = json.loads(componenttest_file.read())

        expected_unittest_dicts = [
            {
              "tag": "cpp test_case.cpp:RequirementByTest1:130",
              "location": {
                "kind": "file",
                "file": "data\\test_case.cpp",
                "line": 130,
                "column": None
              },
              "name": "RequirementByTest1",
              "messages": [],
              "just_up": [],
              "just_down": [],
              "just_global": [],
              "refs": [
                "req FOO0::BAR0",
                "req FOO1::BAR1"
              ],
              "language": "C/C++",
              "kind": "Function"
            },
            {
                "tag": "cpp test_case.cpp:RequirementByTest1:135",
                "location": {
                    "kind": "file",
                    "file": "data\\test_case.cpp",
                    "line": 135,
                    "column": None
                },
                "name": "RequirementByTest1",
                "messages": [],
                "just_up": [],
                "just_down": [],
                "just_global": [],
                "refs": [
                    "req FOO0::BAR0",
                    "req FOO1::BAR1",
                    "req FOO2::BAR2",
                    "req FOO3::BAR3",
                    "req FOO4::BAR4",
                    "req FOO5::BAR5",
                    "req FOO6::BAR6",
                    "req FOO7::BAR7",
                    "req FOO8::BAR8"
                ],
                "language": "C/C++",
                "kind": "Function"
            }
        ]
        expected_componenttest_dicts = [
            {
                "tag": "cpp test_case.cpp:RequirementTagTest1:70",
                "location": {
                    "kind": "file",
                    "file": "data\\test_case.cpp",
                    "line": 70,
                    "column": None
                },
                "name": "RequirementTagTest1",
                "messages": [],
                "just_up": [],
                "just_down": [],
                "just_global": [],
                "refs": [
                    "req 0815",
                    "req 0816"
                ],
                "language": "C/C++",
                "kind": "Function"
            },
            {
                "tag": "cpp test_case.cpp:RequirementTagTest1:75",
                "location": {
                    "kind": "file",
                    "file": "data\\test_case.cpp",
                    "line": 75,
                    "column": None
                },
                "name": "RequirementTagTest1",
                "messages": [],
                "just_up": [],
                "just_down": [],
                "just_global": [],
                "refs": [
                    "req 0815",
                    "req 0816",
                    "req 0817",
                    "req 0818",
                    "req 0819",
                    "req 0820"
                ],
                "language": "C/C++",
                "kind": "Function"
            }
        ]

        for expected_dict in expected_unittest_dicts:
            self.assertTrue(expected_dict in unittest_file_data['data'])
        for expected_dict in expected_componenttest_dicts:
            self.assertTrue(expected_dict in componenttest_file_data['data'])

    def test_test_case_parsing(self):
        """
        Verify that the test case parsing is working correctly
        The whole TestCase class is tested as one since the test_file contains all possible
        variant of an allowed test case implementation
        """
        # fmt: off
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
             "req": ["CB-#0815"]},
            {"suite": "RequirementTagTest2", "test_name": "URLRequirementsCommaSeparated",
             "req": ["CB-#0815", "CB-#0816"]},
            {"suite": "RequirementTagTest2", "test_name": "URLRequirementsAsCommentsSpaceSeparated",
             "req": ["CB-#0815", "CB-#0816"]},
            {"suite": "RequirementTagTest2", "test_name": "MultipleURLRequirements",
             "req": ["CB-#0815", "CB-#0816", "CB-#0817", "CB-#0818"]},
            {"suite": "RequirementTagTest3", "test_name": "MixedRequirements",
             "req": ["CB-#0816", "CB-#0815"]},
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
            # {"suite": "TestMethodsTagTest2", "test_name": "TestMethodAsCommentsMultipleLines",
            # "testmethods": ["TM_REQUIREMENT", "TM_EQUIVALENCE", "TM_BOUNDARY", "TM_CONDITION"]},
            # TODO: Not supported yet, to be discussed in DCS-3430
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
        # fmt: on

        test_cases = ParserForRequirements.collect_test_cases(self.test_case_file_dir)
        self.assertEqual(len(test_cases), 45)

        for i in range(0, len(expect)):
            self.assertEqual(test_cases[i].file_name, self.test_case_file_dir)
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

    def test_lobster_cpp_doxygen_write_implementations_to_lobster_file(self):
        file_dir_list = [self.test_case_file_dir]

        if os.path.exists(self.output_file_name):
            os.remove(self.output_file_name)

        file_exists = os.path.exists(self.output_file_name)
        self.assertFalse(file_exists)

        test_file_list, error_list = \
            get_test_file_list(
                file_dir_list=file_dir_list,
                extension_list=[".cpp", ".cc", ".c", ".h"]
            )

        self.assertIsNotNone(test_file_list)
        self.assertIsInstance(test_file_list, list)

        test_case_list = \
            collect_test_cases_from_test_files(
                test_file_list=test_file_list
            )

        self.assertIsNotNone(test_case_list)
        self.assertIsInstance(test_case_list, list)

        lobster_implementations_dict: dict = \
            create_lobster_implementations_dict_from_test_cases(
                test_case_list=test_case_list,
                test_types=self.all_test_types
            )

        self.assertIsNotNone(lobster_implementations_dict)
        self.assertIsInstance(lobster_implementations_dict, dict)

        write_lobster_implementations_to_output(
            lobster_implementations_dict=lobster_implementations_dict,
            output=self.output_file_name)

        file_exists = os.path.exists(self.output_file_name)
        self.assertTrue(file_exists)

    def tearDown(self):
        for output_file in self.output_file_names:
            if os.path.exists(output_file):
                os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
