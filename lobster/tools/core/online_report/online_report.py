#!/usr/bin/env python3
#
# lobster_online_report - Transform file references to github references
# Copyright (C) 2023-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import os
import sys
from typing import Optional, Sequence, Union
from argparse import Namespace
from pathlib import Path
from dataclasses import dataclass
import yaml
from lobster.common.exceptions import LOBSTER_Exception
from lobster.common.errors import LOBSTER_Error
from lobster.common.report import Report
from lobster.common.location import File_Reference, Github_Reference
from lobster.common.meta_data_tool_base import MetaDataToolBase
from lobster.tools.core.online_report.path_to_url_converter import (
    PathToUrlConverter,
    NotInsideRepositoryException
)

LOBSTER_REPORT = "report"
COMMIT_ID = "commit_id"
BASE_URL = "base_url"
REPO_ROOT = "repo_root"


@dataclass
class Config:
    repo_root: str
    base_url: str
    commit_id: str
    report: str = "report.lobster"


TOOL_NAME = "lobster-online-report"


def load_config(file_name: str) -> Config:
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f'{file_name} is not an existing file!')

    with open(file_name, "r", encoding='utf-8') as file:
        try:
            config_dict = yaml.safe_load(file)
        except yaml.scanner.ScannerError as ex:
            raise LOBSTER_Exception(message="Invalid config file") from ex
    return parse_config_data(config_dict)


def parse_config_data(config_dict: dict) -> Config:
    """Parse a YAML configuration file for the online report tool.

    This function reads a YAML configuration file and extracts the necessary
    configuration parameters for transforming file references to GitHub references
    in a LOBSTER report.

    Args:
        config_dict (dict): YAML configuration file converted to dict.

    Returns:
        Config: A configuration object containing the following attributes:
            - report (str): Path to the input LOBSTER report file
            (defaults to "report.lobster").
            - base_url (str): Base URL for GitHub references.
            - commit_id (str): Git commit ID to use for references.
            - repo_root (str): Path to the root of the Git repository.

    Raises:
        FileNotFoundError: If the specified configuration file doesn't exist.
        LOBSTER_Exception: If the YAML file has syntax errors.
        ValueError: If required attributes are missing or have incorrect types.

    """
    if (not config_dict or
            COMMIT_ID not in config_dict):
        raise KeyError(f'Please follow the right config file structure! '
                         f'Missing attribute {COMMIT_ID}')

    if BASE_URL not in config_dict:
        raise KeyError(f'Please follow the right config file structure! '
                         f'Missing attribute {BASE_URL}')

    if REPO_ROOT not in config_dict:
        raise KeyError(f'Please follow the right config file structure! '
                         f'Missing attribute {REPO_ROOT}')

    base_url = config_dict.get(BASE_URL)
    repo_root = config_dict.get(REPO_ROOT)
    commit_id = config_dict.get(COMMIT_ID)
    report = config_dict.get(LOBSTER_REPORT, "report.lobster")

    if not isinstance(base_url, str):
        raise ValueError(f'Please follow the right config file structure! '
                         f'{BASE_URL} must be a string but got '
                         f'{type(base_url).__name__}.')

    if not isinstance(repo_root, str):
        raise ValueError(f'Please follow the right config file structure! '
                         f'{REPO_ROOT} must be a string but got '
                         f'{type(repo_root).__name__}.')

    if not isinstance(commit_id, str):
        raise ValueError(f'Please follow the right config file structure! '
                         f'{COMMIT_ID} must be a string but got '
                         f'{type(commit_id).__name__}.')

    if not isinstance(report, str):
        raise ValueError(f'Please follow the right config file structure! '
                         f'{LOBSTER_REPORT} must be a string but got '
                         f'{type(report).__name__}.')

    return Config(
        report=report,
        repo_root=repo_root,
        base_url=base_url,
        commit_id=commit_id
    )


def add_github_reference_to_items(
        repo_root: str,
        base_url: str,
        report: Report,
        commit_id: str
):

    repo_root = os.path.abspath(os.path.expanduser(repo_root))
    path_to_url_converter = PathToUrlConverter(repo_root, base_url)

    for item in report.items.values():
        if isinstance(item.location, File_Reference):
            file_path = Path(item.location.filename).resolve()
            try:
                url_parts = path_to_url_converter.path_to_url(file_path, commit_id)
                item.location = Github_Reference(
                    gh_root=url_parts.url_start,
                    filename=url_parts.path_html,
                    line=item.location.line,
                    commit=url_parts.commit_hash,
                )
            except NotInsideRepositoryException as e:
                print(f"Error converting path to URL for {file_path}: {e}")
                continue


class OnlineReportTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="lobster-online-report",
            description="Update file locations in LOBSTER report to GitHub references.",
            official=True,
        )
        self._argument_parser.add_argument(
            "--config",
            help=("Path to YAML file with arguments, "
                  "by default (online-report-config.yaml)"),
            default="online-report-config.yaml",
        )
        self._argument_parser.add_argument(
            "--out",
            help="output file, by default overwrite input",
            default="online_report.lobster",
        )

    def _run_impl(self, options: Namespace) -> int:
        try:
            self._execute(options)
            return 0
        except FileNotFoundError as file_not_found_error:
            self._print_error(file_not_found_error)
        except FileExistsError as file_exists_error:
            self._print_error(file_exists_error)
        except ValueError as value_error:
            self._print_error(value_error)
        except KeyError as key_error:
            self._print_error(key_error)
        except LOBSTER_Error as lobster_error:
            self._print_error(lobster_error)
        return 1

    @staticmethod
    def _print_error(error: Union[Exception, str]):
        print(f"{TOOL_NAME}: {error}", file=sys.stderr)

    @staticmethod
    def _execute(options: Namespace) -> None:
        config = load_config(options.config)
        lobster_online_report(
            config, options.out
        )


def lobster_online_report(config: Config, out_file: str) -> None:
    # This is an API function for Lobster online report tool.
    report = Report()
    report.load_report(config.report)
    add_github_reference_to_items(
        config.repo_root, config.base_url, report, config.commit_id
    )
    report.write_report(out_file)


def main(args: Optional[Sequence[str]] = None) -> int:
    return OnlineReportTool().run(args)
