from unittest import TestCase
import json
import tempfile
from unittest.mock import patch
from lobster.common.report import Coverage, Report
from lobster.common.level_definition import LevelDefinition
from lobster.common.items import Requirement, Tracing_Tag
from lobster.common.location import File_Reference
from lobster.tools.core.report.report import lobster_report


class ReportTests(TestCase):
    def test_compute_coverage(self):
        report = Report()
        level_name = "Calculus Master Mind"

        MAX_SUPPORTED_ITEMS = 100000000

        for num_items in list(range(0, 10000)) \
            + [MAX_SUPPORTED_ITEMS / 2, MAX_SUPPORTED_ITEMS]:
            for ok_items in set(
                (0, 1, 2, int(num_items / 2), max(num_items - 1, 0),
                 num_items),
                 ):
                if num_items < ok_items:
                    continue

                report.coverage[level_name] = Coverage(
                    level=level_name,
                    items=num_items,
                    ok=ok_items,
                    coverage=None
                )
                report.compute_coverage_for_items()
                if num_items == 0:
                    self.assertEqual(report.coverage[level_name].coverage, 0.0)
                else:
                    expected_coverage = (float(ok_items * 100) / float(num_items))
                    if ok_items != num_items:
                        self.assertNotEqual(
                            expected_coverage,
                            100.0,
                            f"Invalid test setup: The expected coverage for {num_items}"
                            f" items with {ok_items} ok items should not be exactly "
                            f"100.0! This is a floating point problem, and not "
                            f"necessarily a bug.",
                        )
                    self.assertEqual(
                        report.coverage[level_name].coverage,
                        expected_coverage,
                        f"Expected coverage for {num_items} items with {ok_items} ok "
                        f"items to be {expected_coverage}, but got "
                        f"{report.coverage[level_name].coverage}",
                    )


    def test_generate_report_file(self):
        apple_config = "apple.conf"
        banana_output = "banana.lobster"

        with patch.object(Report, 'parse_config') as mock_parse_config, \
             patch.object(Report, 'write_report') as mock_write_report:

            lobster_report(
                lobster_config_file=apple_config,
                output_file=banana_output
            )

            # Verify custom parameters were used
            mock_parse_config.assert_called_once_with(apple_config)
            mock_write_report.assert_called_once_with(banana_output)

    def test_write_report_contains_ver_val_fields(self):
        report = Report()
        level_name = "System Requirements"

        report.config = {
            level_name: LevelDefinition(name=level_name, kind="requirements"),
        }
        report.coverage = {
            level_name: Coverage(level=level_name, items=1, ok=1, coverage=100.0),
        }

        item = Requirement(
            tag=Tracing_Tag("req", "123", "1"),
            location=File_Reference("req.trlc", 1, 1),
            framework="codebeamer",
            kind="Requirement",
            name="Requirement with ver/val fields",
            status="Formal Review",
            asil="ASIL B",
            ver_ValSetup="SW unit/comp test",
            ver_ValRationalargumentation="Validation rationale text",
        )
        item.set_level(level_name)
        report.items = {item.tag.key(): item}

        with tempfile.NamedTemporaryFile("w+", suffix=".lobster", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            report.write_report(tmp_path)
            with open(tmp_path, "r", encoding="UTF-8") as fd:
                data = json.load(fd)

            req_item = data["levels"][0]["items"][0]
            self.assertEqual(req_item["ver_ValSetup"], "SW unit/comp test")
            self.assertEqual(
                req_item["ver_ValRationalargumentation"],
                "Validation rationale text",
            )
        finally:
            import os
            os.remove(tmp_path)
