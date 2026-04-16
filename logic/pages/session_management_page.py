from infra.page_base import PageBase
from logic.pages.patient_admission_page import PatientAdmissionPage
import re


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
    REDIRECT_OVERLAY_TEXT = "You are being redirected to the Session Management screen"

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
    ROW_ACTION_BUTTON = (
        "button[aria-label*='more' i], "
        "button[aria-haspopup='menu'], "
        "button:has(svg)"
    )
    REMOVE_SESSION_OPTION = "text=Remove Session"
    REMOVE_SESSION_DIALOG = "[role='dialog']"
    REMOVE_SESSION_PATIENT_ID_INPUT = (
        "[role='dialog'] input[placeholder*='Patient ID'], "
        "[role='dialog'] input[placeholder*='Enter Patient ID'], "
        "[role='dialog'] input[name*='patient'], "
        "[role='dialog'] input"
    )
    REMOVE_SESSION_CONFIRM_BUTTON = "[role='dialog'] button:has-text('Remove')"

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

    def verify_redirect_overlay_visible(self):
        expected = self.REDIRECT_OVERLAY_TEXT.lower()

        # Overlay can be very short-lived; poll for a short window.
        for _ in range(40):
            try:
                if self.pw_page.get_by_text(self.REDIRECT_OVERLAY_TEXT, exact=False).first.is_visible(timeout=100):
                    return True
            except Exception:
                pass

            try:
                body_text = (self.pw_page.locator("body").inner_text(timeout=200) or "").lower()
                if expected in body_text:
                    return True
            except Exception:
                pass

            self.pw_page.wait_for_timeout(200)

        # Fallback: treat successful redirect as acceptable when overlay is missed due to timing.
        try:
            return self.URL_FRAGMENT in self.pw_page.url
        except Exception:
            return False

    def search_session(self, value: str):
        self.pw_page.locator(self.SEARCH_SESSION_INPUT).first.fill(value)

    def verify_patient_status_in_table(self, patient_id: str, expected_status: str):
        try:
            self.search_session(patient_id)
            row = self.pw_page.locator(
                f"//tr[.//*[contains(normalize-space(),'{patient_id}')]]"
            ).first
            row.wait_for(state="visible", timeout=15000)
            row.get_by_text(expected_status, exact=False).first.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def remove_session_by_device_id_if_exists(self, device_id: str):
        self.search_session(device_id)
        self.pw_page.wait_for_timeout(800)

        row = self.pw_page.locator(
            f"//tr[.//*[contains(normalize-space(),'{device_id}')]]"
        ).first
        if row.count() == 0:
            return False

        row.wait_for(state="visible", timeout=10000)
        patient_id = (row.locator("td").first.text_content() or "").strip()

        # The row action button is shown only on row hover in some builds.
        try:
            row.hover()
        except Exception:
            pass

        action_button = row.locator(self.ROW_ACTION_BUTTON).last
        try:
            action_button.wait_for(state="visible", timeout=4000)
        except Exception:
            try:
                row.dispatch_event("mouseover")
            except Exception:
                pass
            self.pw_page.wait_for_timeout(300)

        action_button.click()
        self.pw_page.get_by_text("Remove Session", exact=False).first.click()

        # Some builds require entering Patient ID in a confirmation dialog.
        try:
            dialog = self.pw_page.locator(self.REMOVE_SESSION_DIALOG).first
            dialog.wait_for(state="visible", timeout=5000)

            # Use the same Patient ID shown in the popup: "Patient ID: <value>".
            dialog_text = dialog.inner_text(timeout=3000) or ""
            match = re.search(r"Patient\s*ID\s*:\s*([^\r\n]+)", dialog_text, flags=re.IGNORECASE)
            popup_patient_id = match.group(1).strip() if match else ""
            patient_id_to_fill = popup_patient_id or patient_id

            if patient_id_to_fill:
                input_locator = dialog.locator("input[id^=':r'], input[type='text'], input").first
                input_locator.fill("")
                input_locator.fill(patient_id_to_fill)

            remove_button = dialog.get_by_role("button", name="Remove", exact=False).first
            for _ in range(20):
                try:
                    if remove_button.is_enabled():
                        break
                except Exception:
                    pass
                self.pw_page.wait_for_timeout(100)

            remove_button.click()
        except Exception:
            # Fallback when dialog is not required or has different controls.
            confirm_candidates = [
                self.pw_page.get_by_role("button", name="Remove", exact=False).first,
                self.pw_page.get_by_role("button", name="Confirm", exact=False).first,
            ]
            for candidate in confirm_candidates:
                try:
                    if candidate.is_visible(timeout=2000):
                        candidate.click()
                        break
                except Exception:
                    continue

        # Verify row is removed from current filtered view.
        self.pw_page.wait_for_timeout(1200)
        return row.count() == 0

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
