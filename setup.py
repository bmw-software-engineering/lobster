#!/usr/bin/env python3

import re
import setuptools
from lobster import version

gh_root = "https://github.com"
gh_project = "DiFerMa/lobster"

with open("README.md", "r") as fd:
    long_description = fd.read()

# For the readme to look right on PyPI we need to translate any
# relative links to absolute links to github.
fixes = []
for match in re.finditer(r"\[(.*)\]\((.*)\)", long_description):
    if not match.group(2).startswith("http"):
        fixes.append((match.span(0)[0], match.span(0)[1],
                      "[%s](%s/%s/blob/main/%s)" % (match.group(1),
                                                    gh_root,
                                                    gh_project,
                                                    match.group(2))))

for begin, end, text in reversed(fixes):
    long_description = (long_description[:begin] +
                        text +
                        long_description[end:])

project_urls = {
    "Bug Tracker"   : "%s/%s/issues" % (gh_root, gh_project),
    "Documentation" : "%s/pages/%s/" % (gh_root, gh_project),
    "Source Code"   : "%s/%s"        % (gh_root, gh_project),
}

setuptools.setup(
    name="LOBSTER",
    version=version.LOBSTER_VERSION,
    author="Bayerische Motoren Werke Aktiengesellschaft (BMW AG)",
    author_email="philipp.wullstein-kammler@bmw.de",
    description="The Lightweight Open BMW Software Traceability Evidence Report for requirements coverage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=project_urls["Source Code"],
    project_urls=project_urls,
    license="GNU General Public License v3",
    packages=setuptools.find_packages(),
    install_requires="PyVCG[api]==1.0.7",
    python_requires=">=3.8, <3.13",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Documentation",
        "Topic :: Software Development",
    ],
#  is this entry point correct?
    entry_points={
        "console_scripts": [
            "lobster = lobster.lobster:main",
        ],
    },
)
