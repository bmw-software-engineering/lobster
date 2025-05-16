from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from ..test_runner import TestRunner
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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

    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_driver_options(self):
        """Set and return driver options"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def get_chrome_driver(self):
        """Set up and return a Selenium WebDriver instance for Chrome."""
        driver_options = self.get_driver_options()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=driver_options)
        return driver

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to start
        'lobster-html-report' under test"""
        return self._cmd_args.as_list()
