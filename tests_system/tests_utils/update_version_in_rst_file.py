"""
Script to update LOBSTER version in a generated RST report file.

Mirrors the pattern used by update_version_in_html.py for HTML reports.
"""

import re

from lobster.common.version import LOBSTER_VERSION


def update_version_in_rst_file(file_path) -> bool:
    """Update the LOBSTER version line in a golden RST file.

    The generated RST header contains a line of the form::

        | LOBSTER Version: X.Y.Z

    This function replaces the version token with the currently installed
    LOBSTER version so that the golden file matches actual tool output
    regardless of which release is under test.

    Args:
        file_path: Path to the RST file to update (str or :class:`pathlib.Path`).

    Returns:
        ``True`` if the version line was found and updated, ``False`` otherwise.
    """
    with open(file_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    version_pattern = r"\| LOBSTER Version: [^\n]+"

    if not re.search(version_pattern, content):
        print(f"LOBSTER version line not found in {file_path}")
        return False

    updated_content = re.sub(
        r"(\| LOBSTER Version: )[^\n]+",
        rf"\g<1>{LOBSTER_VERSION}",
        content,
    )

    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write(updated_content)

    print(
        f"Updated LOBSTER version to {LOBSTER_VERSION} in {file_path}"
    )
    return True
