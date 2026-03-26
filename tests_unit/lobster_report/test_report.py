from unittest import TestCase
from unittest.mock import patch
from lobster.common.report import Coverage, Report
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


    def test_generate_report_file_conf(self):
        apple_config = "apple.conf"
        banana_output = "banana.lobster"

        with patch.object(Report, 'validate_config_from_yaml_file') as mock_validate_config_from_yaml_file, \
             patch.object(Report, 'load_config_from_yaml_file') as mock_load_config_from_yaml_file, \
             patch.object(Report, 'print_deprecated_warning') as mock_print_deprecated_warning, \
             patch.object(Report, 'load_config_from_conf_file') as mock_load_config_from_conf_file, \
             patch.object(Report, 'write_report') as mock_write_report:

            lobster_report(
                lobster_config_file=apple_config,
                output_file=banana_output
            )

            # Verify custom parameters were used
            mock_print_deprecated_warning.assert_called_once_with(apple_config)
            mock_load_config_from_conf_file.assert_called_once_with(apple_config)
            mock_write_report.assert_called_once_with(banana_output)

            mock_validate_config_from_yaml_file.assert_not_called()
            mock_load_config_from_yaml_file.assert_not_called()

    def test_generate_report_file_yaml(self):
        apple_config = "apple.yaml"
        banana_output = "banana.lobster"

        with patch.object(Report, 'validate_config_from_yaml_file') as mock_validate_config_from_yaml_file, \
             patch.object(Report, 'load_config_from_yaml_file') as mock_load_config_from_yaml_file, \
             patch.object(Report, 'print_deprecated_warning') as mock_print_deprecated_warning, \
             patch.object(Report, 'load_config_from_conf_file') as mock_load_config_from_conf_file, \
             patch.object(Report, 'write_report') as mock_write_report:

            lobster_report(
                lobster_config_file=apple_config,
                output_file=banana_output
            )

            # Verify custom parameters were used
            mock_validate_config_from_yaml_file.assert_called_once_with(apple_config)
            mock_load_config_from_yaml_file.assert_called_once_with(apple_config)
            mock_write_report.assert_called_once_with(banana_output)

            mock_print_deprecated_warning.assert_not_called()
            mock_load_config_from_conf_file.assert_not_called()
