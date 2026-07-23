#!/usr/bin/env python3

import shutil
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    shutil.rmtree(repo_root / "docs", ignore_errors=True)


if __name__ == "__main__":
    main()
