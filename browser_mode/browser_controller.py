# browser_controller.py
"""
Provides a basic browser controller for loading pages, typing into fields,
clicking elements, and retrieving basic text or HTML from the page.
"""

from playwright.sync_api import sync_playwright

class BrowserController:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.set_viewport_size({"width": 1280, "height": 1024})

    def navigate(self, url):
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(2000)

    def click(self, selector):
        self.page.click(selector, timeout=5000)
        self.page.wait_for_timeout(1000)

    def type(self, selector, text):
        self.page.fill(selector, "")
        self.page.type(selector, text)
        self.page.wait_for_timeout(1000)

    def press_enter(self, selector):
        self.page.focus(selector)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(2000)

    def get_text(self):
        return self.page.inner_text("body")

    def get_state(self):
        try:
            input_value = self.page.eval_on_selector("input[name='q']", "el => el.value")
        except:
            input_value = ""

        # Extract clickable elements (more robust than a[href])
        self.page.set_viewport_size({"width": 1280, "height": 3000})

        dom_snapshot = self.page.evaluate("""
() => {
        function isVisible(el) {
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            return (
            style.display !== 'none' &&
            style.visibility !== 'hidden' &&
            el.offsetHeight > 0
            );
        }

        return Array.from(document.querySelectorAll('a, button, [role], [onclick], input, textarea, label, summary, h1, h2, h3, h4, h5, h6, li'))
            .filter(el => isVisible(el) && (el.innerText.trim() || el.getAttribute('href')))
            .slice(0, 100)
            .map(el => ({
            tag: el.tagName.toLowerCase(),
            text: el.innerText.trim().slice(0, 200),
            id: el.id,
            className: el.className,
            href: el.getAttribute('href'),
            role: el.getAttribute('role'),
            onclick: !!el.getAttribute('onclick'),
            bbox_top: el.getBoundingClientRect().top
            }));
        }

        """)

        return {
            "url": self.page.url,
            "html": self.page.content()[:10000],
            "input": input_value,
            "title": self.page.title(),
            "clickables": dom_snapshot,
            "text": self.get_text()
        }

    def quit(self):
        self.browser.close()
        self.playwright.stop()
