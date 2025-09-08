import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def get_git_commit_timestamp(commit_hash: str, working_dir: Path) -> str:
    """Get timestamp of a commit formatted for HTML."""
    cmd = ['git', '-C', str(working_dir), 'show', '-s', '--format=%ct', commit_hash]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    epoch = int(result.stdout.strip())
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S+00:00") + " UTC"


def extract_commit_hash_from_html(html_content: str) -> str:
    """Extract commit hash from HTML Build Reference."""
    match = re.search(
        r'Build Reference:\s*<strong>([a-f0-9]+|HEAD)</strong>',
        html_content
    )
    if not match:
        raise ValueError("No commit hash found in HTML file")
    return match.group(1)


def update_html_output_file(filename: Path, working_dir: Path) -> None:
    """Update timestamp in LOBSTER HTML file with git commit timestamp."""
    if not filename.exists():
        raise FileNotFoundError(f"HTML file not found: {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()
    commit_hash = extract_commit_hash_from_html(html_content)
    git_timestamp = get_git_commit_timestamp(commit_hash, working_dir)
    updated_content = re.sub(
        r'Timestamp:\s*[^<]+',
        f'Timestamp: {git_timestamp}',
        html_content
    )
    if updated_content != html_content:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(updated_content)
