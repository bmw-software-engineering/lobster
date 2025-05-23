import json
from flask import Response
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from .lobster_codebeamer_asserter import LobsterCodebeamerAsserter
from .mock_server_setup import start_mock_server, get_mock_app


class LobsterCodebeamerExtractRequirementsTest(LobsterCodebeamerSystemTestCaseBase):

    @classmethod
    def setUpClass(cls):
        """Start the mock server once before any tests run."""
        start_mock_server()
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_extract_requirements_scenarios(self):
        # lobster-trace: UseCases.Partial_Codebeamer_IDs_in_Output
        # lobster-trace: UseCases.Codebeamer_Summary_in_Output
        # lobster-trace: UseCases.Wrong_Codebeamer_IDs_in_Output
        # lobster-trace: UseCases.Incorrect_Number_of_Codebeamer_IDs_in_Output

        self.set_config_file_data()
        PAGE_SIZE = 5
        self._test_runner.config_file_data.page_size = PAGE_SIZE

        """Validate Codebeamer report generation with mock data using subtests."""
        test_cases = [
            {"total_items": 0, "output": "zero_item.lobster"},
            {"total_items": 1, "output": "one_item.lobster"},
            {"total_items": 4, "output": "four_items.lobster"},
            {"total_items": 5, "output": "five_items.lobster"},

            {"total_items": 6, "output": "six_items.lobster"},
            {"total_items": 9, "output": "nine_items.lobster"},
            {"total_items": 10, "output": "ten_items.lobster"},

            {"total_items": 11, "output": "eleven_items.lobster"},

            {"total_items": 74, "output": "seventy_four_items.lobster"},
            {"total_items": 75, "output": "seventy_five_items.lobster"},

            {"total_items": 76, "output": "seventy_six_items.lobster"},
        ]

        for case in test_cases:
            with self.subTest(total_items=case["total_items"]):
                self.codebeamer_flask.counter = 0
                total_items = case["total_items"]
                out_file = case.get("output")

                self._test_runner.config_file_data.out = out_file
                self._test_runner.declare_output_file(
                    self._data_directory / out_file)

                responses = []
                # if total_items == 0 then an response with 0 items is created else
                # the number of responses are created based on the PAGE_SIZE
                # and total_items to simulate the pagination
                if total_items == 0:
                    responses = [self.create_mock_response_items(
                        1, PAGE_SIZE, total_items)]
                else:
                    for i in range(
                        1, (total_items // PAGE_SIZE) +
                        (2 if total_items % PAGE_SIZE > 0 else 1)
                    ):
                        responses.append(self.create_mock_response_items(
                            i, PAGE_SIZE, total_items))

                self.codebeamer_flask.responses = [
                    Response(json.dumps(response), status=200) for response in responses
                ]
                completed_process = self._test_runner.run_tool_test()

                if total_items == 0:
                    self.assertEqual(self.codebeamer_flask.counter, 1)
                else:
                    self.assertEqual(self.codebeamer_flask.counter, len(responses))
                asserter = LobsterCodebeamerAsserter(self,
                                                     completed_process,
                                                     self._test_runner,
                                                     )
                asserter.assertStdOutNumAndFile(total_items,
                                                self._test_runner.config_file_data.out,
                                                PAGE_SIZE,
                                                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()
