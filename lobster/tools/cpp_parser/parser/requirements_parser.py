"""
This script verifies if the test files of a given target contains @requirement tag or not
"""
import logging
from pathlib import Path
from typing import Dict, List, Union

from lobster.tools.cpp_parser.parser.benchmark_test_case import BenchmarkTestCase
from lobster.tools.cpp_parser.parser.common import (
    build_github_base_url,
    execute_path,
    get_files_for_analysis,
    get_github_link,
)
from lobster.tools.cpp_parser.parser.config import config
from lobster.tools.cpp_parser.parser.test_case import TestCase


class ParserForRequirements:
    def __init__(self):
        self.bazel_target = config.build_target
        self.service_pack = config.service_pack
        self.workspace = execute_path("bazel info workspace")
        self.test_type = config.test_type

    def get_target_test_files(self):
        return get_files_for_analysis(self.workspace, self.bazel_target, self.service_pack)

    @staticmethod
    def create_requirement_dict(
        tracking_id: Union[int, str], comp_name: str, test_fixture_name: str, file_gitlink: str
    ) -> Dict:
        """
        Create a dictionnary collecting all info for a test case and its linked requirement
        Tracking_id is either an int if a requirement is linked to the test case, or the string "Missing"
        """
        requirement = {}
        requirement["tracking_id"] = tracking_id
        requirement["component"] = comp_name
        requirement["test_desc"] = test_fixture_name
        requirement["file_name"] = file_gitlink

        return requirement

    def create_requirement_details_list(self, test_case: TestCase, file_gitlink: str) -> List[Dict]:
        reqs = []
        req_ids = test_case.requirements

        if len(req_ids) == 0 and len(test_case.required_by) == 0:
            req_ids = ["Missing"]

        for id in req_ids:
            reqs.append(self.create_requirement_dict(id, test_case.suite_name, test_case.test_name, file_gitlink))
        return reqs

    def fetch_requirement_details_for_test_files(self, test_files: List[str]) -> List:
        """
        For each test_file specified in test_files, search in each source file for
        contained test cases.
        When a test case is found, collect referenced codebeamer id and metadata to locate

        Parameters
        ----------
        test_files: List[str]
            list of test_files to parse

        Returns:
        List[
            {
                filename: {
                    component: --- name of the Component under Test
                    test_desc: --- name of the Component Fixture
                    file_name: --- Github URI, hyperlinking to the exact location in
                                Codecraft
                    tracking_id: --- Req. Id to Codebeamer Spec which this Test is associated with.
                }
            }
        ]
        """
        details = []
        base_url = None
        repo_prefix = None
        gitlink = None
        try:
            base_url, repo_prefix = get_github_link(config.build_target)
        except Exception as exception:
            error = str(exception)

        for file in set(test_files):
            if base_url and repo_prefix:
                gitlink = build_github_base_url(base_url, config.branch) + file.partition(f"/{repo_prefix}")[2]
            test_cases = self.collect_test_cases(file)

            for tc in test_cases:
                file_gitlink_with_line = f'{file}#L{tc.docu_start_line}'
                if gitlink:
                    file_gitlink_with_line = gitlink + "#L" + str(tc.docu_start_line)
                details.extend(self.create_requirement_details_list(tc, file_gitlink_with_line))
        return details

    @staticmethod
    def collect_test_cases(file: Path) -> List[TestCase]:
        """
        Parse a source file for test cases

        Parameters
        ----------
        file: Path
            Source file to parse

        Returns
        -------
        List[TestCase]
           List of parsed TestCase / BenchmarkTestCase
        """

        try:
            with open(file, "r", encoding="UTF-8", errors="ignore") as f:
                lines = f.readlines()

        except Exception as e:
            logging.error(f"exception {e}")
            return []

        test_cases = []
        test_case_types = [
            TestCase,
            BenchmarkTestCase,
        ]  # KHe: I would try to parse the other way round, since BenchmarkTestCase inherits from TestCase

        for i in range(0, len(lines)):
            for type in test_case_types:
                test_case = type.try_parse(file, lines, i)

                if test_case:
                    test_cases.append(test_case)
        return test_cases


def collect_test_requirements() -> List[Dict[str, Dict]]:
    """
    Look for all test targets in config.build_target,
    returns a list of dictionaries containing the linking
    information for each test case to the covered codebeamer
    requirement ID

    Returns:
    list({
        filename: {
            component: --- name of the Component under Test
            test_desc: --- name of the Component Fixture
            file_name: --- Github URI, hyperlinking to the exact location in
                            Codecraft
            tracking_id: --- Req. Id to Codebeamer Spec which this Test is associated with.
        }
    })
    """
    parser = ParserForRequirements()
    test_files = parser.get_target_test_files()
    return parser.fetch_requirement_details_for_test_files(test_files)
