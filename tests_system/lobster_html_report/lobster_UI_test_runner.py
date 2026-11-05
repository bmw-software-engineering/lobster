# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from lobster.tools.core.html_report.html_report import main
from tests_system.testrunner import TestRunner


@dataclass
class CmdArgs:
    lobster_report: Optional[str] = None
    out: Optional[str] = None
    dot: Optional[str] = None
    high_contrast: Optional[str] = None
    render_md: bool = False

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []

        def append_if_string(parameter: str, value: Optional[str]):
            if value is not None:
                cmd_args.append(f"{parameter}={value}")

        if self.lobster_report:
            cmd_args.append(self.lobster_report)

        if self.render_md:
            cmd_args.append("--render-md")

        append_if_string("--out", self.out)
        append_if_string("--dot", self.dot)
        append_if_string("--high-contrast", self.high_contrast)
        return cmd_args


class LobsterUITestRunner(TestRunner):
    """System test runner for lobster-report"""

    def __init__(self, working_dir: Path):
        super().__init__(main, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_driver_options(self):
        """Set and return driver options"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def get_chrome_driver(self):
        """Set up and return a Selenium WebDriver instance for Chrome."""
        logging.getLogger("selenium").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        driver_options = self.get_driver_options()
        chrome = os.environ.get("LOBSTER_TEST_CHROME")
        chromedriver = os.environ.get("LOBSTER_TEST_CHROMEDRIVER")
        if chrome and chromedriver:
            # Under Bazel: use the pinned binaries from runfiles.
            # pylint: disable=import-outside-toplevel,import-error
            from python.runfiles import runfiles
            rf = runfiles.Create()
            driver_options.binary_location = rf.Rlocation(chrome)
            service = Service(executable_path=rf.Rlocation(chromedriver))
            return webdriver.Chrome(service=service, options=driver_options)
        # Without pinned binaries: Selenium Manager resolves the driver on demand.
        os.environ.setdefault("SE_SKIP_DRIVER_IN_PATH", "true")
        return webdriver.Chrome(options=driver_options)

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to start
        'lobster-html-report' under test"""
        return self._cmd_args.as_list()
