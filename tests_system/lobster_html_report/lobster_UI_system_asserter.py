import re

from ..asserter import Asserter, is_valid_json, sort_json


# Setting this flag will tell unittest not to print tracebacks from this frame.
# This way our custom assertions will show the interesting line number from the caller
# frame, and not from this boring file.
__unittest = True


class LobsterUIAsserter(Asserter):
    def assertOutputFiles(self):
        """For each expected file, checks if an actual file has been created with the
        expected content

        Before comparing the actual text with the expected text, we do the
        following replacements:
        a) Replace Windows-like slashes \\ with / in order to be able to
           compare the actual output on all OS against the expected output on
           Linux
        b) Replace the fixed string CURRENT_WORKING_DIRECTORY with the absolute path to
           the current working directory. This is necessary for tools like
           lobster-cpptest which write absolute paths into their *.lobster
           output files.
        c) Normalize Plotly-generated div ids to avoid false negatives in HTML output
           comparison.
        """
        # lobster-trace: system_test.Compare_Output_Files

        def normalize_plotly_ids_and_cdn(html):
            # Normalize Plotly div ids
            html = re.sub(
                r'id="[^"]+" class="plotly-graph-div"',
                'id="PLOTLY_ID" class="plotly-graph-div"',
                html
            )
            html = re.sub(
                r'Plotly\.newPlot\(\s*"[^"]+"',
                'Plotly.newPlot("PLOTLY_ID"',
                html
            )
            html = re.sub(
                r'document\.getElementById\("([^"]+)"\)',
                'document.getElementById("PLOTLY_ID")',
                html
            )
            # Ignore the entire script tag that loads plotly from CDN
            html = re.sub(
                r'<script[^>]*src="https://cdn\.plot\.ly/plotly-[^"]+\.min\.js"[^>]*>'
                r'</script>',
                '<script src="https://cdn.plot.ly/plotly-VERSION.min.js"></script>',
                html
            )
            # Normalize timestamps - replace dynamic timestamps with static placeholder
            html = re.sub(
                r'Timestamp: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{2}:\d{2} UTC',
                'Timestamp: NORMALIZED-TIMESTAMP UTC',
                html
            )

            # Normalize the entire SVG block with all dynamic content
            html = re.sub(
                r'<svg xmlns="http://www\.w3\.org/2000/svg"[^>]*>.*?</svg>',
                '<svg>Normalized SVG Content</svg>',
                html,
                flags=re.DOTALL
            )

            return html

        for expected_file_ref in self._test_runner.tool_output_files:
            expected_location = self._test_runner.working_dir / expected_file_ref.name
            try:
                with open(
                    expected_file_ref,
                    "r",
                    encoding="UTF-8",
                ) as expected_file:
                    try:
                        with open(
                            expected_location,
                            "r",
                            encoding="UTF-8",
                        ) as actual_file:
                            # lobster-trace: system_test.Slashes
                            modified_actual = actual_file.read().replace("\\\\", "/")

                            # lobster-trace: system_test.CWD_Placeholder
                            modified_expected = expected_file.read().replace(
                                "CURRENT_WORKING_DIRECTORY",
                                str(self._test_runner.working_dir),
                            )
                            # Normalize Plotly div ids if this is an HTML file
                            if expected_file_ref.name.endswith(".html") or \
                                    expected_file_ref.name.endswith(".output"):
                                modified_actual = \
                                    normalize_plotly_ids_and_cdn(modified_actual)
                                modified_expected = \
                                    normalize_plotly_ids_and_cdn(modified_expected)
                            modified_actual_json = is_valid_json(modified_actual)
                            modified_expected_json = is_valid_json(modified_expected)
                            if modified_actual_json and modified_expected_json:
                                self._test_case.assertEqual(
                                    sort_json(modified_actual_json),
                                    sort_json(modified_expected_json),
                                    f'File differs from expectation '
                                    f'{expected_file_ref}!',
                                )
                            else:
                                self._test_case.assertEqual(
                                    modified_actual,
                                    modified_expected,
                                    f'File differs from expectation '
                                    f'{expected_file_ref}!',
                                )
                    except FileNotFoundError:
                        self._test_case.fail(f"File {expected_file_ref} was not "
                                             f"generated by the tool under test!")
            except FileNotFoundError as ex:
                self._test_case.fail(f"Invalid test setup: {ex}")
