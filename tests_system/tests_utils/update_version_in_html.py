
"""
Script to update LOBSTER version in HTML footer
"""

import re
import sys

from lobster.common.version import LOBSTER_VERSION


def update_version_in_html_file(file_path):
    """
    Update the LOBSTER version in the HTML footer if present

    Args:
        file_path (str): Path to the HTML file
        new_version (str): New version string to replace

    Returns:
        bool: True if version was found and updated, False otherwise
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the pattern to match <p>LOBSTER Version: any_version</p>
    version_pattern = r'<p>LOBSTER Version: [^<]+</p>'

    # Check if the version tag is present
    if not re.search(version_pattern, content, re.IGNORECASE):
        print(f"LOBSTER version tag not found in {file_path}")
        return False

    print(f"Found LOBSTER version tag in {file_path}")

    # Replace the version in the <p> tag
    updated_content = re.sub(
        r'(<p>LOBSTER Version: )[^<]+</p>',
        rf'\g<1>{LOBSTER_VERSION}</p>',
        content,
        flags=re.IGNORECASE
    )

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Successfully updated LOBSTER version to {LOBSTER_VERSION} in {file_path}")
    return True


if __name__ == "__main__":
    update_version_in_html_file(sys.argv[1])
