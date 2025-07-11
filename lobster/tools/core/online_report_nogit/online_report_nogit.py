import argparse
import os
import sys

from dataclasses import dataclass
from typing import Iterable
from urllib.parse import quote

from lobster.items import Item
from lobster.location import File_Reference, Github_Reference
from lobster.report import Report
from lobster.meta_data_tool_base import MetaDataToolBase


@dataclass
class RepoInfo:
    """
    Data class to hold repository information.

    Attributes:
        remote_url (str): The root URL of the GitHub repository.
        root (str): The local path to the root of the repository.
        commit (str): The commit hash to use when building a URL to a file.
    """
    remote_url: str
    root: str
    commit: str


def _file_ref_to_github_ref(
        file_ref: File_Reference,
        repo_info: RepoInfo,
        paths_must_exist: bool,
) -> Github_Reference:
    """
    Convert a File_Reference to a Github_Reference.

    Args:
        file_ref (File_Reference): The file reference to convert (can be a directory).
        repo_data (RepoData): The repository meta information to use for the conversion.
        paths_must_exist (bool): If True, then a sanity check is performed. If the path
          is is not a directory and not a file, then a FileNotFoundError is raised.

    Returns:
        Github_Reference: The converted GitHub reference.
    """
    if (not paths_must_exist) \
            or os.path.isfile(file_ref.filename) or os.path.isdir(file_ref.filename):
        return Github_Reference(
            gh_root=repo_info.remote_url,
            filename=quote(
                os.path.relpath(
                    os.path.realpath(file_ref.filename),
                    os.path.realpath(repo_info.root),
                ).replace(os.sep, "/")
            ),
            line=file_ref.line,
            commit=repo_info.commit,
        )
    raise FileNotFoundError(f"File '{file_ref.filename}' does not exist.")


def _update_items(items: Iterable[Item], repo_info: RepoInfo, paths_must_exist: bool):
    for item in items:
        if isinstance(item.location, File_Reference):
            item.location = _file_ref_to_github_ref(
                item.location,
                repo_info,
                paths_must_exist,
            )


def apply_github_urls(
        in_file: str,
        out_file: str,
        repository_info: RepoInfo,
        paths_must_exist: bool = True):
    """
    Reads a report file, converts all file references to GitHub references,
    and saves the report.

    Args:
        file (str): Path to the input LOBSTER report file.
        out_file (str): Output file for the updated LOBSTER report.
        repo_data (RepoData): object containing remote URL, root path, and commit hash.
        paths_must_exist (bool): If True, then a sanity check is performed. If the path
          is is not a directory and not a file, then a FileNotFoundError is raised.
    """
    report = Report()
    report.load_report(in_file)
    _update_items(report.items.values(), repository_info, paths_must_exist)
    report.write_report(out_file)


class OnlineReportNogitTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="lobster-online-report-nogit",
            description="Update file locations in LOBSTER report to GitHub references.",
            official=True,
        )
        ap = self._argument_parser
        ap.add_argument(dest="report",
                        metavar="LOBSTER_REPORT",
                        help="Path to the input LOBSTER report file.")
        ap.add_argument("--repo-root", required=True,
                        help="Local path to the root of the repository.")
        ap.add_argument("--remote-url", required=True,
                        help="GitHub repository root URL.")
        ap.add_argument("--commit", required=True,
                        help="Git commit hash to use for the references.")
        ap.add_argument("--out", required=True, metavar="OUTPUT_FILE",
                        help="Output file for the updated LOBSTER report."
                            "It can be the same as the input file in order to "
                            "overwrite the input file.",)

    def _run_impl(self, options: argparse.Namespace) -> int:
        try:
            apply_github_urls(
                in_file=options.report,
                repository_info=RepoInfo(
                    remote_url=options.remote_url,
                    root=options.repo_root,
                    commit=options.commit,
                ),
                out_file=options.out,
            )
            print(f"LOBSTER report {options.out} created, using remote URL references.")
        except FileNotFoundError as e:
            print(
                f"Error: {e}\n"
                f"Note: Relative paths are resolved with respect to the "
                f"current working directory '{os.getcwd()}'.",
                file=sys.stderr,
            )
            return 1
        return 0


def main() -> int:
    return OnlineReportNogitTool().run()
