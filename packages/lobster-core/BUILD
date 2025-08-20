load("@rules_python//python:defs.bzl", "py_test")
load("@rules_python//python:packaging.bzl", "py_package", "py_wheel", "py_wheel_dist")

VERSION = "0.14.1-dev"

gh_root = "https://github.com"

gh_project = "bmw-software-engineering/lobster"

project_urls = {
    "Bug Tracker": "%s/%s/issues" % (gh_root, gh_project),
    "Documentation": "%s/pages/%s/" % (gh_root, gh_project),
    "Source Code": "%s/%s" % (gh_root, gh_project),
}

py_package(
    name = "package",
    packages = [
        "lobster",
        "lobster.config",
        "lobster.html",
        "lobster.tools.core.ci_report",
        "lobster.tools.core.html_report",
        "lobster.tools.core.online_report",
        "lobster.tools.core.online_report_nogit",
        "lobster.tools.core.report",
    ],
    deps = [
        "//:lobster-core",
    ],
)

py_wheel(
    name = "wheel",
    author = "Bayerische Motoren Werke Aktiengesellschaft (BMW AG)",
    author_email = "philipp.wullstein-kammler@bmw.de",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Documentation",
        "Topic :: Software Development",
    ],
    description_content_type = "text/markdown",
    description_file = "README.md",
    distribution = "bmw-lobster-core",
    entry_points = {
        "console_scripts": [
            "lobster-report=lobster.tools.core.report.report:main",
            "lobster-html-report=lobster.tools.core.html_report.html_report:main",
            "lobster-online-report=lobster.tools.core.online_report.online_report:main",
            "lobster-online-report-nogit=lobster.tools.core.online_report_nogit.online_report_nogit:main",
            "lobster-ci-report=lobster.tools.core.ci_report.ci_report:main",
        ],
    },
    homepage = project_urls["Source Code"],
    license = "GNU Affero General Public License v3",
    project_urls = project_urls,
    python_requires = ">=3.7, <4",
    requires = [
        "Markdown~=3.7",
        "PyYAML>=6.0",
        "yamale>=6.0.0",
    ],
    summary = "Lightweight Open BMW Software Traceability Evidence Report",
    version = VERSION,
    deps = [":package"],
)
