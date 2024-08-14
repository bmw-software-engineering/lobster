import argparse
import enum
import json
import logging
import os
from pathlib import Path


class Tracker(str, enum.Enum):
    """
    Enum class used to list all implemented trackers.
    """

    REQUIREMENTS = "test_requirements"
    ACCEPTANCES = "test_acceptances"
    PARAMETERS = "test_parameters"
    PRODUCTS = "test_products"
    SYSTEM = "test_system"
    SOFTWARE = "test_software"
    PROTOTYPE_SOFTWARE = "test_prototype_software"
    SHADOW_MODE = "test_shadowmode"
    COMPONENTS_UNITS = "test_components_units"


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return getinstance


@singleton
class ConfigSingleton:
    def __init__(self):
        self.project = ""
        self.service_pack = "21"
        self.throttle_retries = 5
        self.throttle_sleep = 120
        self.build_target = ""
        self.branch = "master"
        self.test_type = "component"
        self.output_dir = str(Path(__file__).resolve().parent)
        self.project_config_file = None
        self.zip = ""
        self.timestamp = None
        self.git_tag = None

        self.download_source = "artifactory"
        self.download = False
        self.artifactory_cache_age_threshold = "24"
        self.teamscale_upload = False
        self.bazel_query = True

        self.exported_columns = [
            "id",
            "type",
            "item",
            "name",
            "path",
            "component",
            "test_desc",
            "file_name",
            "unit_tests",
        ]
        self.tracker_properties = {
            Tracker.REQUIREMENTS: {
                "cb_file_name": "requirements_cb_result.json",
                "column_extension": [{"column_name": "typename", "from": "type/name"}],
            },
            Tracker.ACCEPTANCES: {
                "cb_file_name": "acceptances_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
            Tracker.PARAMETERS: {
                "cb_file_name": "parameters_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
            Tracker.PRODUCTS: {
                "cb_file_name": "products_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
            Tracker.SYSTEM: {
                "cb_file_name": "system_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
            Tracker.SOFTWARE: {
                "cb_file_name": "software_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
            Tracker.PROTOTYPE_SOFTWARE: {
                "cb_file_name": "software_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
            Tracker.SHADOW_MODE: {
                "cb_file_name": "shadow_mode_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
            Tracker.COMPONENTS_UNITS: {
                "cb_file_name": "component_unit_cb_result.json",
                "column_extension": [
                    {"column_name": "typename", "from": "type/name"},
                    {"column_name": "version", "from": "version"},
                ],
            },
        }
        self.non_existing_info = "---"

        self.test_results_file = "test_file_result.json"
        self.codebeamer_results_file = "codebeamer_result.json"

        self.coverage_report_html = "requirements_coverage.html"
        self.coverage_pivot_html = "pivottable.html"
        self.coverage_report_csv = "requirements_export.csv"
        self.coverage_report_filtered_csv = "requirements_export_filtered.csv"
        self.coverage_report_xlsx = "requirements_export.xlsx"
        self.coverage_report_filtered_xlsx = "requirements_export_filtered.xlsx"

        self.git_basedir = "/vispiron-swe"
        self.github_url = "https://github.com/"

        self.artifactory_cache_url = None
        self.codebeamer_url = "https://codebeamer.bmwgroup.net/cb"
        self.codebeamer_tracker_origin = "test_requirements"
        self.codebeamer_key_file = ""

        self.codebeamer_tracker = []

        self.codebeamer_inclusion_filter = None
        self.codebeamer_exclusion_filter = None

        self.builds_results_file = ""
        self.partition = ""
        self.workspace = ""

        self.log_file = ""
        self.log_file_test_verification = ""
        self.log_file_teamscale_upload = ""

        self.argparse_args = None
        self.cfg_file_data = None

        self.diff_version = 0

    def _parse_args(self):
        """Parse the command line options"""

        parser = argparse.ArgumentParser(description="Run requirements coverage tool on selected target")

        parser.add_argument(
            "--project_config_file",
            type=str,
            default=self.project_config_file,
            required=True,
            help="Project configuration file",
        )
        parser.add_argument(
            "--build_target",
            type=str,
            default=self.build_target,
            required=True,
            metavar="PATH",
            help="The bazel build target",
        )
        parser.add_argument(
            "--test_type",
            type=str,
            choices=["unit", "component"],
            default=self.test_type,
            help="(Optional) Test type to query: unit or component",
        )
        parser.add_argument(
            "--output_dir",
            type=str,
            default=self.output_dir,
            help="Absolute path of directory where results will be saved",
        )
        parser.add_argument(
            "-c",
            "--cb_file",
            type=str,
            default=self.codebeamer_results_file,
            dest="codebeamer_results_file",
            help="(Optional) Path of the file containing Codebeamer tracking details",
        )
        parser.add_argument(
            "--cb_access_key_file",
            help="(Optional) File path where codebeamer credentials are stored",
            type=str,
            default=self.codebeamer_key_file,
            dest="codebeamer_key_file",
        )
        parser.add_argument(
            "-ct",
            "--builds_results_file",
            type=str,
            default=self.builds_results_file,
            help="(Optional) Path of the file containing Zuul builds results & status (builds_results_file.json)",
        )
        parser.add_argument(
            "-to",
            "--tracker_origin",
            type=str,
            choices=[
                "test_requirements",
                "test_acceptances",
                "test_parameters",
                "test_products",
                "test_system",
                "test_software",
                "test_all",
                "test_prototype_software",
                "test_shadowmode",
                "test_components_units",
            ],
            default=self.codebeamer_tracker_origin,
            dest="codebeamer_tracker_origin",
            help="(Optional) Filter Codebeamer items according to the tracker origin",
        )
        parser.add_argument(
            "-t",
            "--test_file",
            type=str,
            default=self.test_results_file,
            dest="test_results_file",
            help="(Optional) Path of the file containing test files requirement details",
        )
        parser.add_argument(
            "-d",
            "--download",
            default=self.download,
            action="store_true",
            help="Flag whether to download from Codebeamer or use already downloaded result (default: False)",
        )
        parser.add_argument(
            "-ds",
            "--download_source",
            default=self.download_source,
            choices=["codebeamer", "artifactory"],
            help="config.download_source to download from Artifactory or Codebeamer (default: Artifactory)",
        )
        parser.add_argument(
            "-at",
            "--artifactory_cache_age_threshold",
            default="24",
            help="Time in hours under which to check for artifactory cache (default: 24 hours)",
        )
        parser.add_argument(
            "-ut",
            "--upload_to_teamscale",
            default=self.teamscale_upload,
            dest="teamscale_upload",
            action="store_true",
            help="Flag whether to upload results into Teamscale (default: False)",
        )
        parser.add_argument(
            "-q",
            "--query",
            default=self.bazel_query,
            dest="bazel_query",
            action="store_false",
            help="Flag whether to suppress query bazel for test targets (default: True)",
        )
        parser.add_argument(
            "--url_cb",
            type=str,
            default=self.codebeamer_url,
            dest="codebeamer_url",
            help="config.codebeamer_url for Codebeamer server. default: Productive server. Please change to INT for testing.",
        )
        parser.add_argument(
            "--log_file", type=str, default=self.log_file, help="Path of the log file for requirement coverage tool"
        )
        parser.add_argument(
            "--logfile_test_verification",
            type=str,
            default=self.log_file_test_verification,
            dest="log_file_test_verification",
            help="Path of the log file for verifying requirements",
        )
        parser.add_argument(
            "--logfile_upload_to_ts",
            type=str,
            default=self.log_file_teamscale_upload,
            dest="log_file_teamscale_upload",
            help="Path of the log file for uploading requirement coverage to Teamscale",
        )
        parser.add_argument(
            "--partition", type=str, default=self.partition, help="Name of the teamscale partition to upload findings"
        )
        parser.add_argument("--workspace", type=str, default=self.workspace, help="Workspace path")
        parser.add_argument(
            "--zip", default=self.zip, type=str, help="Path for compressing all the output files into a zip."
        )
        parser.add_argument("--throttle_retries", type=int, default=self.throttle_retries)
        parser.add_argument("--throttle_sleep", type=int, default=self.throttle_sleep)
        parser.add_argument(
            "--timestamp",
            default=None,
            type=str,
            help="Timestamp in YYYY-MM-DD HH:mm:ss format for downloading most closer possible codeBeamer data",
        )
        parser.add_argument(
            "--git_tag",
            default=None,
            type=str,
            help="Git tag name to extract timestamp for downloading most closer possible codeBeamer data",
        )

        return parser.parse_args()

    def _set_member(self, name):
        """Set a config variable

        Config variables provided in the project configuration are overwritten by the
        command line. If the variable is not defined either way, the default value is
        retained.

        name -- config variable name
        config_file_opts -- dict with project configuration file options
        cmd_line_opts -- namespace object as returned by argparse containing the command
                         line options
        """

        arg_val = vars(self.argparse_args).get(name, None)
        cfg_val = self.cfg_file_data.get(name, None)

        if arg_val:
            self.__dict__[name] = arg_val

        elif cfg_val:
            self.__dict__[name] = cfg_val

    def init(self, parse_args=None):
        """Initialise config variables

        Config variables are set based on the command line options and the project
        configuration file. Options given on command line overwrite the ones set
        in the project configuration file. If neither are given the default value
        is used.
        """
        if not parse_args:
            parse_args = self._parse_args
        args = parse_args()

        cfg_file_path = Path.joinpath(Path(__file__).resolve().parent.parent.parent, "config")
        cfg_file = cfg_file_path / args.project_config_file

        try:
            with open(cfg_file) as cfg_file_handle:
                cfg = json.load(cfg_file_handle)

        except Exception as e:
            logging.error(f"Failed reading config {cfg_file} with {e}")
            raise e

        self.argparse_args = args
        self.cfg_file_data = cfg

        self._set_member("project")
        self._set_member("service_pack")
        self._set_member("build_target")
        self._set_member("branch")
        self._set_member("artifactory_cache_url")
        self._set_member("test_type")
        self._set_member("output_dir")
        self._set_member("zip")
        self._set_member("timestamp")
        self._set_member("git_tag")

        self._set_member("download_source")
        self._set_member("download")
        self._set_member("artifactory_cache_age_threshold")
        self._set_member("teamscale_upload")
        self._set_member("bazel_query")

        self._set_member("exported_columns")
        self._set_member("non_existing_info")

        self._set_member("test_results_file")
        self._set_member("codebeamer_results_file")

        self._set_member("coverage_report_html")
        self._set_member("coverage_pivot_html")
        self._set_member("coverage_report_csv")
        self._set_member("coverage_report_filtered_csv")
        self._set_member("coverage_report_xlsx")
        self._set_member("coverage_report_filtered_xlsx")

        self._set_member("git_basedir")
        self._set_member("github_url")

        self._set_member("codebeamer_url")
        self._set_member("codebeamer_tracker_origin")
        self._set_member("codebeamer_key_file")
        self._set_member("codebeamer_tracker")
        self._set_member("codebeamer_inclusion_filter")
        self._set_member("codebeamer_exclusion_filter")

        self._set_member("builds_results_file")
        self._set_member("partition")
        self._set_member("workspace")

        self._set_member("log_file")
        self._set_member("log_file_test_verification")
        self._set_member("log_file_teamscale_upload")
        self._set_member("throttle_retries")
        self._set_member("throttle_sleep")


config = ConfigSingleton()
