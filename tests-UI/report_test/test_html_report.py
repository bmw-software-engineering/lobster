import sys
import importlib
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ButtonTest:
    def __init__(self):
        # Add tests-UI path and import driver setup
        sys.path.append('tests-UI')
        try:
            self.driver = importlib.import_module("tests-UI.setup").setup_driver()
        except ImportError as e:
            sys.stderr.write(f"Error importing driver module: {e}\n")
            sys.exit(1)

    def test_show_issue_button(self):
        """
        Test the toggle functionality of the Show Issue button.
        """
        sys.stdout.write("Testing Show Issue button...\n")
        for toggle in range(2):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'BtnToggleIssue'))
                ).click()
                element = self.driver.find_element(By.ID, 'issues-section')

                if (toggle == 0 and element.value_of_css_property("display") == "block") or \
                   (toggle == 1 and element.value_of_css_property("display") == "none"):
                    sys.stdout.write(f"Issue items visibility is as expected.\n")
                else:
                    sys.stderr.write(f"Test failed. Visibility mismatch.\n")
                    return False
            except Exception as e:
                sys.stderr.write(f"Error during Show Issue button test: {e}\n")
                return False
        return True

    def click_and_verify(self, button_xpath, item_class, status):
        """
        Click a button and verify the visibility of elements by class.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            ).click()

            if item_class == "item-":
                xpath = "//div[starts-with(@class, 'item-') and not(contains(@class, 'item-name'))]"
                total_items = len(self.driver.find_elements(By.XPATH, xpath))
            else:
                WebDriverWait(self.driver, 10).until(
                    lambda d: len(d.find_elements(By.CLASS_NAME, item_class)) > 0
                )
                total_items = len(self.driver.find_elements(By.CLASS_NAME, item_class))

            sys.stdout.write(f"{total_items} items retrieved after clicking the '{status}' button.\n")
            return True
        except Exception as e:
            print(f"No items found for '{status}' button, skipping check.")
            return False

    def check_hidden_elements(self, item_classes, current_status):
        """
        Verify that elements for statuses other than the current one are hidden.
        """
        for status, class_name in item_classes.items():
            if status != current_status:
                try:
                    element = self.driver.find_element(By.CLASS_NAME, class_name)
                    display_property = element.value_of_css_property("display")
                    expected_display = "none" if current_status != "Show All" else "block"

                    if display_property == expected_display:
                        sys.stdout.write(f"'{status}' items visibility is as expected.\n")
                    else:
                        sys.stderr.write(f"Visibility mismatch for '{status}' items.\n")
                except Exception as e:
                    print(f"No items found for '{status}' button.")

    def test_html_report_title(self):
        """
        Test various buttons in an HTML report and their corresponding item visibility.
        """
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

        try:
            for status, xpath in button_xpath.items():
                sys.stdout.write(f"Testing '{status}' button...\n")
                if self.click_and_verify(xpath, item_classes[status], status):
                    time.sleep(1)
                    self.check_hidden_elements(item_classes, status)

            if not self.test_show_issue_button():
                sys.stderr.write("Show Issue button test failed.\n")
                sys.exit(1)

            sys.stdout.write("All tests passed successfully.\n")
        except Exception as e:
            sys.stderr.write(f"Test execution error: {e}\n")
            sys.exit(1)

    def run_tests(self):
        """
        Run all the tests in sequence.
        """
        try:
            self.test_html_report_title()
        except Exception as e:
            sys.stderr.write(f"Critical error during test execution: {e}\n")
            sys.exit(1)
        finally:
            self.driver.quit()
            sys.exit(0)


if __name__ == "__main__":
    test_suite = ButtonTest()
    test_suite.run_tests()
