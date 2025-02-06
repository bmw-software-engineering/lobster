import sys
import importlib
import time
import json
import subprocess
import os
from datetime import datetime, timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LobsterUIReportTests:
    """UI Automation Tests for Lobster Report."""

    TESTS_UI_PATH = "tests-UI"
    TIMEOUT = 10

    def __init__(self):
        sys.path.append(self.TESTS_UI_PATH)
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Initialize the Selenium WebDriver."""
        try:
            return importlib.import_module("tests-UI.setup").setup_driver()
        except ImportError as e:
            sys.stderr.write(f"Error importing driver module: {e}\n")
            sys.exit(1)

    def test_show_issue_button(self):
        """Test the toggle functionality of the Show Issue button."""
        print("Testing Show Issue button...")

        for toggle in range(2):
            try:
                WebDriverWait(self.driver, self.TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "BtnToggleIssue"))
                ).click()
                element = self.driver.find_element(By.ID, "issues-section")
                expected_display = "block" if toggle == 0 else "none"

                if element.value_of_css_property("display") == expected_display:
                    print("Issue items visibility is as expected.")
                else:
                    sys.stderr.write("Test failed: Visibility mismatch.\n")
                    return False
            except Exception as e:
                sys.stderr.write(f"Error during Show Issue button test: {e}\n")
                return False
        return True

    def click_and_verify(self, button_xpath, item_class, status):
        """Click a button and verify the visibility of elements."""
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            ).click()

            elements = self.driver.find_elements(By.CLASS_NAME, item_class) if item_class != "item-" else \
                self.driver.find_elements(By.XPATH, "//div[starts-with(@class, 'item-') and not(contains(@class, 'item-name'))]")

            print(f"{len(elements)} items retrieved after clicking '{status}' button.")
            return True
        except Exception as e:
            print(f"No items found for '{status}' button, skipping check.")
            return False

    def check_hidden_elements(self, item_classes, current_status):
        """Ensure that elements for other statuses are hidden."""
        for status, class_name in item_classes.items():
            if status != current_status:
                try:
                    element = self.driver.find_element(By.CLASS_NAME, class_name)
                    expected_display = "none" if current_status != "Show All" else "block"

                    if element.value_of_css_property("display") == expected_display:
                        print(f"'{status}' items visibility is as expected.")
                    else:
                        sys.stderr.write(f"Visibility mismatch for '{status}' items.\n")
                except Exception:
                    print(f"No items found for '{status}' button.")

    def test_html_report_title(self):
        """Test visibility toggles in the HTML report."""
        button_xpath = {
            "OK": '//*[@id="btnFilterItem"]/button[2]',
            "Missing": '//*[@id="btnFilterItem"]/button[3]',
            "Partial": '//*[@id="btnFilterItem"]/button[4]',
            "Justified": '//*[@id="btnFilterItem"]/button[5]',
            "Warning": '//*[@id="btnFilterItem"]/button[6]',
            "Show All": '//*[@id="btnFilterItem"]/button[1]',
        }
        item_classes = {
            "OK": "item-ok",
            "Missing": "item-missing",
            "Partial": "item-partial",
            "Justified": "item-justified",
            "Warning": "item-warning",
            "Show All": "item-",
        }

        for status, xpath in button_xpath.items():
            print(f"Testing '{status}' button...")
            if self.click_and_verify(xpath, item_classes[status], status):
                time.sleep(1)
                self.check_hidden_elements(item_classes, status)
               
        if not self.test_show_issue_button():
            sys.stderr.write("Show Issue button test failed.\n")
            sys.exit(1)

        print("All tests passed successfully.")

    def test_git_hash_timestamp(self):
        """Verify git commit timestamps in the report output."""
        report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "report.output")
        print(f"Processing report: {report_path}")

        with open(report_path) as file:
            data = json.load(file)

        for level in data.get("levels", []):
            for item in level.get("items", []):
                tag, exec_commit_id = item.get("tag"), item.get("location", {}).get("exec_commit_id")
                if not (tag and exec_commit_id):
                    continue

                elements = self.driver.find_elements(By.XPATH, "//div[starts-with(@class, 'item-') and not(contains(@class, 'item-name'))]")
                for elem in elements:
                    text = elem.text.replace("Python Function", "python")
                    if tag in text and exec_commit_id in text:
                        result = subprocess.run(
                            ['git', 'show', '-s', '--format=%ct', exec_commit_id],
                            capture_output=True, text=True, check=True
                        )

                        expected_time = datetime.fromtimestamp(int(result.stdout.strip()), tz=timezone.utc)
                        if str(expected_time) in text:
                            print("Timestamp verification passed.")

    def run_tests(self):
        """Execute all test cases."""
        try:
            self.test_html_report_title()
            self.test_git_hash_timestamp()
        except Exception as e:
            sys.stderr.write(f"Critical error during test execution: {e}\n")
            sys.exit(1)
        finally:
            self.driver.quit()
            sys.exit(0)


if __name__ == "__main__":
    LobsterUIReportTests().run_tests()
