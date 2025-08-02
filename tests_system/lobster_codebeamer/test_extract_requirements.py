import json
from flask import Response
from .lobster_codebeamer_system_test_case_base import (
    LobsterCodebeamerSystemTestCaseBase)
from .lobster_codebeamer_asserter import LobsterCodebeamerAsserter
from .mock_server_setup import get_mock_app


class LobsterCodebeamerExtractRequirementsTest(LobsterCodebeamerSystemTestCaseBase):

    @classmethod
    def setUpClass(cls):
        """Start the mock server once before any tests run."""
        cls.codebeamer_flask = get_mock_app()

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_extract_requirements_scenarios(self):
        """Validate Codebeamer report generation with mock data using subtests."""
        # lobster-trace: UseCases.Codebeamer_Summary_in_Output
        # lobster-trace: UseCases.Wrong_Codebeamer_IDs_in_Output
        # lobster-trace: UseCases.Incorrect_Number_of_Codebeamer_Items_in_Output

        cfg = self._test_runner.config_file_data
        cfg.set_default_root_token_out()
        cfg.import_query = 54321
        cfg.page_size = 5

        for total_items in [0, 1, 4, 5, 6, 9, 10, 11, 74, 75, 76]:
            with self.subTest(total_items=total_items):
                self.codebeamer_flask.reset()
                out_file = f"{total_items}_items.lobster"

                self._test_runner.config_file_data.out = out_file
                self._test_runner.declare_output_file(
                    self._data_directory / out_file)

                responses = []
                # if total_items == 0 then an response with 0 items is created else
                # the number of responses are created based on the PAGE_SIZE
                # and total_items to simulate the pagination
                if total_items == 0:
                    responses = [self.create_mock_response_items(
                        1, cfg.page_size, total_items)]
                else:
                    for i in range(
                        1, (total_items // cfg.page_size) +
                        (2 if total_items % cfg.page_size > 0 else 1)
                    ):
                        responses.append(self.create_mock_response_items(
                            i, cfg.page_size, total_items))

                self.codebeamer_flask.responses = [
                    Response(json.dumps(response), status=200) for response in responses
                ]
                completed_process = self._test_runner.run_tool_test()

                self.assertEqual(
                    len(self.codebeamer_flask.received_requests),
                    len(responses),
                )

                for i, request in enumerate(self.codebeamer_flask.received_requests,
                                            start=1):
                    actual_url = request['url']
                    expected_url = (
                        f"{cfg.root}/api/v3/reports/"
                        f"{cfg.import_query}/items?page={i}&pageSize={cfg.page_size}"
                    )
                    self.assertEqual(actual_url, expected_url)

                asserter = LobsterCodebeamerAsserter(self,
                                                     completed_process,
                                                     self._test_runner,
                                                     )
                asserter.assertStdOutNumAndFile(
                    num_items=total_items,
                    out_file=self._test_runner.config_file_data.out,
                    page_size=cfg.page_size,
                    import_query=cfg.import_query,
                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()
