import re
from pathlib import Path
from lobster.tools.core.html_report.html_report import get_commit_timestamp_utc


def update_html_output_file(filename: Path, working_dir: Path) -> None:
    """Update timestamp in LOBSTER HTML file with git commit timestamp."""
    if not filename.exists():
        raise FileNotFoundError(f"HTML file not found: {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()
    git_timestamp = get_commit_timestamp_utc("HEAD", str(working_dir))
    updated_content = re.sub(
        r'Timestamp:\s*[^<]+',
        f'Timestamp: {git_timestamp}',
        html_content
    )
    if updated_content != html_content:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(updated_content)
