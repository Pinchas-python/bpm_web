from infra.page_base import PageBase
from logic.pages.patient_admission_page import PatientAdmissionPage


class SessionManagementPage(PageBase):
    URL_FRAGMENT = "session-management"

    # Top-level navigation / section entry points
    SESSION_MANAGEMENT_HEADER = "a[aria-label='Session Management']"
    PATIENT_ADMISSION_NAV = "a[aria-label='Patient Admission']"
    PATIENT_LOOKUP_NAV = "a[aria-label='Patient Lookup']"

    # Session grid controls (from session management landing page)
    SEARCH_SESSION_INPUT = (
        "input[placeholder='Search Session'], "
        "input[placeholder*='Search Session'], "
        "input[aria-label*='Search Session']"
    )
    FILTER_BY_STATUS_DROPDOWN = (
        "text=Filter by Status"
    )
    SHOW_HIDE_COLUMNS_DROPDOWN = (
        "text=Show/Hide Columns"
    )
    REFRESH_BUTTON = (
        "button[aria-label*='Refresh'], button[aria-label*='refresh']"
    )

    # Settings menu controls
    SETTINGS_BUTTON = (
        "//button[@id='profile-button']"
    )
    SETTINGS_MENU_CONTAINER = "#popover-content"
    SETTINGS_CLIENT_NAME = "#client-name-text"
    SETTINGS_USERNAME = "#username-text"
    SETTINGS_LOGOUT_CONTAINER = "#logout-container"
    SETTINGS_VERSION_TEXT = "#version-text"
    SETTINGS_EMAIL_SUPPORT_OPTION = "text=Email Support"
    SETTINGS_CHOOSE_DEPARTMENT_OPTION = "text=Choose Department"
    SETTINGS_LOGOUT_OPTION = "text=Log out"

    # Session grid columns and states
    ADMISSION_DATE_HEADER = "text=Admission Date"
    PATIENT_ID_HEADER = "text=Patient ID"
    FULL_NAME_HEADER = "text=Full Name"
    DEVICE_ID_HEADER = "text=Device ID"
    REFERRING_PHYSICIAN_HEADER = "text=Referring Physician"
    START_TIME_HEADER = "text=Start Time"
    STATUS_HEADER = "text=Status"
    REMAINING_HEADER = "text=Remaining"

    def verify_session_management_page_opened(self):
        try:
            self.pw_page.wait_for_url(f"**/{self.URL_FRAGMENT}", timeout=30000)
            if self.URL_FRAGMENT not in self.pw_page.url:
                return False

            self._wait_any_visible(
                [
                    self.SESSION_MANAGEMENT_HEADER,
                    self.SEARCH_SESSION_INPUT,
                    self.FILTER_BY_STATUS_DROPDOWN,
                    self.SHOW_HIDE_COLUMNS_DROPDOWN,
                    self.PATIENT_ADMISSION_NAV,
                    self.PATIENT_LOOKUP_NAV,
                ],
                timeout=10000,
            )
            return True
        except Exception:
            return False

    def verify_session_grid_opened(self):
        try:
            self._wait_any_visible([self.SEARCH_SESSION_INPUT], timeout=10000)
            self._wait_any_visible([self.FILTER_BY_STATUS_DROPDOWN], timeout=10000)
            self._wait_any_visible([self.SHOW_HIDE_COLUMNS_DROPDOWN], timeout=10000)

            # Verify key table headers are present.
            self._wait_any_visible([self.ADMISSION_DATE_HEADER], timeout=10000)
            self._wait_any_visible([self.PATIENT_ID_HEADER], timeout=10000)
            self._wait_any_visible([self.FULL_NAME_HEADER], timeout=10000)
            self._wait_any_visible([self.DEVICE_ID_HEADER], timeout=10000)
            self._wait_any_visible([self.REFERRING_PHYSICIAN_HEADER], timeout=10000)
            self._wait_any_visible([self.START_TIME_HEADER], timeout=10000)
            self._wait_any_visible([self.STATUS_HEADER], timeout=10000)
            self._wait_any_visible([self.REMAINING_HEADER], timeout=10000)

            return True
        except Exception:
            return False

    def open_patient_admission(self):
        self._click_any_visible([self.PATIENT_ADMISSION_NAV], timeout=10000)
        return PatientAdmissionPage(self.pw_page)

    def open_settings_menu(self):
        self._click_any_visible([self.SETTINGS_BUTTON], timeout=10000)

    def verify_settings_menu_opened(self):
        try:
            self._wait_any_visible([self.SETTINGS_MENU_CONTAINER], timeout=10000)
            self._wait_any_visible([self.SETTINGS_CLIENT_NAME], timeout=10000)
            self._wait_any_visible([self.SETTINGS_USERNAME], timeout=10000)
            self._wait_any_visible([self.SETTINGS_LOGOUT_CONTAINER], timeout=10000)
            self._wait_any_visible([self.SETTINGS_EMAIL_SUPPORT_OPTION], timeout=10000)
            self._wait_any_visible([self.SETTINGS_CHOOSE_DEPARTMENT_OPTION], timeout=10000)
            self._wait_any_visible([self.SETTINGS_LOGOUT_OPTION], timeout=10000)
            return True
        except Exception:
            return False

    def verify_settings_user_email_visible(self, user_email: str):
        try:
            self.pw_page.get_by_text(user_email, exact=False).first.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def verify_settings_client_name_equals(self, expected_client_name: str):
        try:
            client_name = (self.pw_page.locator(self.SETTINGS_CLIENT_NAME).first.text_content() or "").strip()
            return client_name == expected_client_name
        except Exception:
            return False

    def verify_email_support_visible(self):
        try:
            self.pw_page.locator(self.SETTINGS_EMAIL_SUPPORT_OPTION).first.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def verify_choose_department_visible(self):
        try:
            self.pw_page.locator(self.SETTINGS_CHOOSE_DEPARTMENT_OPTION).first.wait_for(
                state="visible", timeout=10000
            )
            return True
        except Exception:
            return False

    def click_logout(self):
        self._click_any_visible([self.SETTINGS_LOGOUT_OPTION], timeout=10000)

    def _wait_any_visible(self, selectors, timeout=6000):
        if isinstance(selectors, str):
            selectors = [selectors]

        for selector in selectors:
            try:
                self.pw_page.locator(selector).first.wait_for(state="visible", timeout=timeout)
                return
            except Exception:
                continue

        raise AssertionError(f"None of selectors became visible: {selectors}")

    def _click_any_visible(self, selectors, timeout=6000):
        if isinstance(selectors, str):
            selectors = [selectors]

        for selector in selectors:
            try:
                locator = self.pw_page.locator(selector).first
                locator.wait_for(state="visible", timeout=timeout)
                locator.click()
                return
            except Exception:
                continue

        raise AssertionError(f"Could not click any selector from: {selectors}")
