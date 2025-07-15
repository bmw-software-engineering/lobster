import argparse
import os.path
import sys

from dataclasses import dataclass
from typing import Iterable
from urllib.parse import quote

from lobster.items import Item
from lobster.location import File_Reference, Github_Reference
from lobster.report import Report
from lobster.meta_data_tool_base import MetaDataToolBase


@dataclass
class RepoData:
    """
    Data class to hold repository information.

    Attributes:
        remote_url (str): The root URL of the GitHub repository.
        repo_root (str): The local path to the root of the repository.
        commit (str): The commit hash to use when building a URL to a file.
    """
    remote_url: str
    root: str
    commit: str


def file_ref_to_remote_ref(file_ref: File_Reference, repo_data: RepoData) -> (
        Github_Reference):
    """
    Convert a File_Reference to a Github_Reference.

    Args:
        file_ref (File_Reference): The file reference to convert.
        repo_data (RepoData): The repository meta information to use for the conversion.

    Returns:
        Github_Reference: The converted GitHub reference.
    """
    if os.path.isfile(file_ref.filename) or os.path.isdir(file_ref.filename):
        return Github_Reference(
            gh_root=repo_data.remote_url,
            filename=quote(
                os.path.relpath(
                    os.path.realpath(file_ref.filename),
                    os.path.realpath(repo_data.root),
                ).replace(os.sep, "/")
            ),
            line=file_ref.line,
            commit=repo_data.commit,
        )
    raise FileNotFoundError(f"File '{file_ref.filename}' does not exist.")


def update_items(items: Iterable[Item], repo_data: RepoData):
    for item in items:
        if isinstance(item.location, File_Reference):
            item.location = file_ref_to_remote_ref(item.location, repo_data)


def update_lobster_file(file: str, repo_data: RepoData, out_file: str):
    """
    Update the LOBSTER report file to use GitHub references.

    Args:
        file (str): Path to the input LOBSTER report file.
        repo_data (RepoData): object containing remote URL, root path,
                              and commit hash.
        out_file (str): Output file for the updated LOBSTER report.
    """
    report = Report()
    report.load_report(file)
    update_items(report.items.values(), repo_data)
    report.write_report(out_file)
    print(f"LOBSTER report {out_file} created, using remote URL references.")


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
            update_lobster_file(
                file=options.report,
                repo_data=RepoData(
                    remote_url=options.remote_url,
                    root=options.repo_root,
                    commit=options.commit,
                ),
                out_file=options.out,
            )
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
