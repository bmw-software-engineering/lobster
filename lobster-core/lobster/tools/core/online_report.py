#!/usr/bin/env python3
#
# lobster_online_report - Transform file references to github references
# Copyright (C) 2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import re
import sys
import os
import argparse
import configparser

from lobster.report import Report
from lobster.location import File_Reference, Github_Reference


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lobster_report",
                    nargs="?",
                    default="report.lobster")
    ap.add_argument("--commit",
                    help="commit SHA or branch/tag, by default main",
                    default="main")
    ap.add_argument("--repo-root",
                    help="override git repository root",
                    default=None)
    options = ap.parse_args()

    if not os.path.isfile(options.lobster_report):
        if options.lobster_report == "report.lobster":
            ap.error("specify report file")
        else:
            ap.error("%s is not a file" % options.lobster_report)

    if options.repo_root:
        repo_root = os.path.abspath(os.path.expanduser(options.repo_root))
        if not os.path.isdir(os.path.join(repo_root, ".git")):
            ap.error("cannot find .git directory in %s" % options.repo_root)
    else:
        repo_root = os.getcwd()
        while True:
            if os.path.isdir(os.path.join(repo_root, ".git")):
                break
            new_root = os.path.dirname(repo_root)
            if new_root == repo_root:
                print("error: could not find .git directory")
                return 1
            repo_root = new_root

    git_config = configparser.ConfigParser()
    git_config.read(os.path.join(repo_root, ".git", "config"))
    if 'remote "origin"' not in git_config.sections():
        print("error: could not find remote \"origin\" in git config")
        return 1

    gh_root = git_config['remote "origin"']["url"]
    assert gh_root.endswith(".git")

    if gh_root.startswith("http"):
        gh_root = gh_root[:-4]
    else:
        match = re.match(r"^(.*)@(.*):(.*)\.git$", gh_root)
        if match is None:
            print("could not understand git origin %s" % gh_root)
        gh_root = "https://%s/%s" % (match.group(2),
                                     match.group(3))

    report = Report()
    report.load_report(options.lobster_report)

    for item in report.items.values():
        if isinstance(item.location, File_Reference):
            assert os.path.isfile(item.location.filename)
            loc = Github_Reference(
                gh_root  = gh_root,
                commit   = options.commit,
                filename = os.path.relpath(
                    os.path.abspath(item.location.filename),
                    repo_root),
                line     = item.location.line)
            item.location = loc

    report.write_report(options.lobster_report)
    print("LOBSTER report %s changed to use online references" %
          options.lobster_report)


if __name__ == "__main__":
    sys.exit(main())
