import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def test_html_report_title(dynamic_dir, report_filename, expected_title):
    """
    Test function to verify the title of an HTML report with dynamic file path.

    Parameters:
    - dynamic_dir (str): Base directory containing the report.
    - report_filename (str): Name of the HTML report file.
    - expected_title (str): Expected title of the report.
 
    Returns:
    - bool: True if the title matches, False otherwise.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))

    file_path = dir_path + "/test_html_report.html"

    report_path = os.path.join(dynamic_dir, report_filename)
    file_url = f"file:///{os.path.abspath(report_path)}"

        # Headless mode options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Automatically download ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        driver.get(file_url)
        actual_title = driver.title
        if actual_title == expected_title:
            print(f"Test Passed: Title is '{actual_title}'")
            sys.exit(0)
        else:
            print(f"Test Failed: Expected '{expected_title}', but got '{actual_title}'")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        return False

    finally:
        driver.quit()

if __name__ == "__main__":

    base_directory = "./tests-system/lobster-core/html_report/selenium-test"
    report_file = "test_html_report.html"
    expected_title = 'L.O.B.S.T.E.R.'
    sys.exit(test_html_report_title(base_directory, report_file, expected_title))


