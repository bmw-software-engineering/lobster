import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# class SeleniumTests:

def setup_driver():
    """
    Set up and return a Selenium WebDriver instance.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = dir_path + "/test_html_report.html"
    file_url = f"file:///{os.path.abspath(file_path)}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(file_url)
    print("Driver setup complete.")
    return driver
