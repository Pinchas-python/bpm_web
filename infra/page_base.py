from playwright.sync_api import Page


class PageBase:
    pw_page: Page = None

    def __init__(self, page):
        self.pw_page = page

    def wait_for_visible(self, selector: str):
        self.pw_page.wait_for_selector(selector, state="visible")
        return self.pw_page.is_visible(selector)