from typing import Type
import os
from playwright.sync_api import sync_playwright
from infra.page_base import PageBase




class BrowserOnline:
    playwright = None
    browser = None
    context = None
    page = None
    popup = None

    def __init__(self):
        self.playwright = sync_playwright().start()
        Desktop = self.playwright.devices['Desktop Chrome HiDPI']
        ci_env = os.getenv("CI", "").strip().lower()
        gh_actions = os.getenv("GITHUB_ACTIONS", "").strip().lower()
        ci_mode = ci_env in ("1", "true", "yes") or gh_actions == "true"
        headless_mode = ci_mode

        launch_options = {
            "headless": headless_mode,
        }
        if ci_mode:
            launch_options["args"] = ["--no-sandbox", "--disable-dev-shm-usage"]

        self.browser = self.playwright.chromium.launch(**launch_options)

        context_options = {
            **Desktop,
            "ignore_https_errors": ci_mode,
        }
        self.context = self.browser.new_context(**context_options)
        self.context.tracing.start(screenshots=True, snapshots=True)
        self.page = self.context.new_page()

    def navigate(self, address, page_type: Type[PageBase]):
        self.page.goto(address, wait_until="load")
        return self.create_page(page_type)

    def create_page(self, page_type):
        return page_type(self.page)

    def create_popup(self, popup, new_popup):
        self.popup = popup
        return new_popup(self.popup)

    def stop_trace(self):
        os.makedirs("test-results", exist_ok=True)
        self.context.tracing.stop(path="test-results/trace.zip")

    def close(self):
        try:
            if self.context:
                self.context.close()
        except Exception:
            pass

        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass

        try:
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass


