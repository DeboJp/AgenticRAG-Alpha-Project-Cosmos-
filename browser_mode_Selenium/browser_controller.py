# browser_controller.py
"""
Provides a basic browser controller for loading pages, typing into fields,
clicking elements, and retrieving basic text or HTML from the page.
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class BrowserController:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = uc.Chrome(version_main=134, options=options)

    def navigate(self, url):
        self.driver.get(url)
        time.sleep(2)

    def click(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.click()
        time.sleep(1)

    def type(self, selector, text):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.clear()
        element.send_keys(text)
        time.sleep(1)

    def press_enter(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.send_keys(Keys.RETURN)
        time.sleep(2)

    def get_text(self):
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except:
            return ""

    def get_state(self):
        try:
            search_box = self.driver.find_element(By.NAME, "q")
            current_input = search_box.get_attribute("value")
        except:
            current_input = ""

        from bs4 import BeautifulSoup
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        for s in soup(["script", "style"]):
            s.decompose()

        body_html = str(soup.body)
        clickables = []
        for a in soup.find_all("a"):
            href = a.get("href", "")
            text = a.get_text(strip=True)
            if href and text:
                try:
                    domain_fragment = href.split("/")[2]
                    selector = f'a[href*="{domain_fragment}"]'
                except IndexError:
                    selector = "a"
                clickables.append({
                    "text": text,
                    "selector": selector
                })


        return {
            "url": self.driver.current_url,
            "html": body_html[:10000],
            "input": current_input,
            "title": self.driver.title,
            "clickables": clickables[:15],
            "text": self.get_text()  # ← add this line
        }


    def quit(self):
        self.driver.quit()
