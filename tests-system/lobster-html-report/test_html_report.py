import sys
import subprocess
from datetime import datetime, timezone
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lobster.tools.core.html_report.html_report import get_commit_timestamp_utc
from .lobster_UI_system_test_case_base import LobsterUISystemTestCaseBase
from ..asserter import Asserter


class LobsterUIReportTests(LobsterUISystemTestCaseBase):
    """UI Automation Tests for Lobster Report."""

    TESTS_UI_PATH = "tests-UI"
    TIMEOUT = 10

    def setUp(self):
        super().setUp()
        sys.path.append(self.TESTS_UI_PATH)
        self._test_runner = self.create_test_runner()
        self.driver = self._test_runner.get_chrome_driver()
        self.OUT_FILE = "test_html_report.html"
        self.input_file = f'file://{self._test_runner.working_dir}/{self.OUT_FILE}'
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.cmd_args.lobster_report = str(
            self._data_directory / "report.output")

    def test_show_issue_button(self):
        """Test the toggle functionality of the Show Issue button."""
        self._test_runner.run_tool_test()
        self.driver.get(self.input_file)
        for toggle in range(2):
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "BtnToggleIssue"))
            ).click()
            element = self.driver.find_element(By.ID, "issues-section")
            expected_display = "block" if toggle == 0 else "none"
            self.assertEqual(element.value_of_css_property("display"), expected_display)

    def click_and_verify(self, button_xpath, item_class, status, item_count, asserter):
        """Click a button and verify the visibility of elements."""

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        ).click()

        if item_class != "item-":
            elements = self.driver.find_elements(By.CLASS_NAME, item_class)
        else:
            elements = self.driver.find_elements(
                By.XPATH, "//div[starts-with(@class, 'item-') "
                          "and not(contains(@class, 'item-name'))]")
        self.assertEqual(len(elements), item_count.get(status))
        return True

    def check_hidden_elements(self, item_classes, current_status, asserter):
        """Ensure that elements for other statuses are hidden."""
        for status, class_name in item_classes.items():
            if status != current_status:
                if self.driver.find_elements(By.CLASS_NAME, class_name):
                    element = self.driver.find_element(By.CLASS_NAME, class_name)
                    expected_display = ("none" if current_status != "Show All" else
                                        "block")

                    self.assertEqual(element.value_of_css_property("display"),
                                     expected_display)

    def test_status_buttons(self):
        """Test the status buttons in the HTML report."""
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.driver.get(self.input_file)

        ok = "ok"
        missing = "missing"
        partial = "partial"
        justified = "justified"
        warning = "warning"
        all = "Show All"
        button_xpath = {
            ok: '//*[@id="btnFilterItem"]/button[2]',
            missing: '//*[@id="btnFilterItem"]/button[3]',
            partial: '//*[@id="btnFilterItem"]/button[4]',
            justified: '//*[@id="btnFilterItem"]/button[5]',
            warning: '//*[@id="btnFilterItem"]/button[6]',
            all: '//*[@id="btnFilterItem"]/button[1]',
        }
        item_classes = {
            ok: "item-ok",
            missing: "item-missing",
            partial: "item-partial",
            justified: "item-justified",
            warning: "item-warning",
            all: "item-",
        }
        item_count = {
            ok: 2,
            missing: 1,
            partial: 0,
            justified: 0,
            warning: 0,
            all: 3
        }
        for status, xpath in button_xpath.items():
            if self.click_and_verify(xpath, item_classes[status], status, item_count,
                                     asserter):
                self.check_hidden_elements(item_classes, status, asserter)

    def test_git_hash_timestamp(self):
        """Verify git commit timestamps in the report output."""
        self._test_runner.run_tool_test()
        self.driver.get(self.input_file)

        report_path = (self._data_directory / "report.output")

        with open(report_path) as file:
            data = json.load(file)

        for level in data.get("levels", []):
            for item in level.get("items", []):
                tag, commit = item.get("tag"), item.get("location", {}).get("commit")
                if not (tag and commit):
                    continue

                elements = self.driver.find_elements(
                    By.XPATH, "//div[starts-with(@class, 'item-') "
                              "and not(contains(@class, 'item-name'))]")
                for elem in elements:
                    text = elem.text.replace("Python Function", "python")
                    if tag in text and commit in text:
                        result = subprocess.run(
                            ['git', 'show', '-s', '--format=%ct', commit],
                            capture_output=True, text=True, check=True
                        )
                        expected_time = str(datetime.fromtimestamp(
                            int(result.stdout.strip()), tz=timezone.utc)) + " UTC"
                        self.assertIn(str(expected_time), text)

    def test_meta_tag(self):
        """Test to check the presence of meta tag in the HTML report."""
        # lobster-trace: html_req.Meta_Tag_In_Html_Report
        self._test_runner.run_tool_test()
        self.driver.get(self.input_file)
        meta_element = self.driver.find_element(By.TAG_NAME, "meta")
        self.assertEqual(meta_element.get_attribute('http-equiv'), "Content-Type")
        self.assertEqual(
            meta_element.get_attribute('content'), "text/html; charset=utf-8")
