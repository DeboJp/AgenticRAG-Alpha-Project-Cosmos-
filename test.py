"""
Tool: google_search
Purpose: Opens a Google search in the browser using a query and returns visible text results.
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = None

def start_browser():
    global driver
    if driver is None:
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        driver = uc.Chrome(version_main=134, options=options)

def run_search(query):
    global driver
    if driver is None:
        start_browser()

    driver.get("https://www.google.com")
    time.sleep(2)  # Wait for page to load

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)

    result_text = driver.find_element(By.TAG_NAME, "body").text
    return result_text

if __name__ == '__main__':
    query = "distance from oliv madison to computer science building google maps"
    search_results = run_search(query)
    print(search_results)
