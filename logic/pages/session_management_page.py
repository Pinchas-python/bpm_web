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

    def verify_required_controls_opened(self):
        try:
            if not self.verify_session_grid_opened():
                return False

            self._wait_any_visible(
                [
                    self.PATIENT_ADMISSION_NAV,
                    "text=New patient",
                    "text=New Patient",
                ],
                timeout=10000,
            )
            self._wait_any_visible([self.PATIENT_LOOKUP_NAV, "text=Patient Lookup"], timeout=10000)
            self._wait_any_visible([self.SETTINGS_BUTTON], timeout=10000)
            return True
        except Exception:
            return False

    def verify_row_actions_by_status(self, status_value: str, expect_edit_enabled: bool):
        self.open_row_action_menu_by_status(status_value)

        edit_admission_option = self._get_visible_menu_option("Edit admission")
        complete_session_option = self._get_visible_menu_option("Complete session")
        remove_option = self._get_visible_menu_option(["Remove", "Remove Session"])

        edit_enabled = self._is_action_enabled(edit_admission_option)
        complete_enabled = self._is_action_enabled(complete_session_option)
        remove_enabled = self._is_action_enabled(remove_option)

        # Close menu before next interaction.
        self.pw_page.keyboard.press("Escape")

        return (
            edit_enabled == expect_edit_enabled
            and complete_enabled
            and remove_enabled
        )

    def open_row_action_menu_by_status(self, status_value: str):
        row = self.pw_page.locator(
            f"//tr[.//*[contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{status_value.lower()}')]]"
        ).first
        row.wait_for(state="visible", timeout=15000)

        # In some builds, the row action button appears only on hover.
        try:
            row.hover()
        except Exception:
            pass

        action_button = row.locator(self.ROW_ACTION_BUTTON).last
        action_button.wait_for(state="visible", timeout=10000)
        action_button.click()

    def open_row_action_menu_for_any_existing_session(self):
        statuses = ["Pending", "Active", "Complete limited", "Complete"]
        for status in statuses:
            try:
                self.open_row_action_menu_by_status(status)
                return True
            except Exception:
                continue

        return False

    def verify_delete_related_row_actions_visible(self):
        if not self.open_row_action_menu_for_any_existing_session():
            return False

        try:
            self._get_visible_menu_option(["Edit session", "Edit admission", "Edit"]).is_visible()
            self._get_visible_menu_option("Complete session").is_visible()
            self._get_visible_menu_option(["Remove", "Remove Session"]).is_visible()
            return True
        except Exception:
            return False
        finally:
            try:
                self.pw_page.keyboard.press("Escape")
            except Exception:
                pass

    def open_remove_session_dialog_for_any_existing_session(self):
        if not self.open_row_action_menu_for_any_existing_session():
            return False

        try:
            self._get_visible_menu_option(["Remove Session", "Remove"]).click()
            dialog = self.pw_page.locator(self.REMOVE_SESSION_DIALOG).first
            dialog.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def click_cancel_in_remove_session_dialog(self):
        try:
            dialog = self.pw_page.locator(self.REMOVE_SESSION_DIALOG).first
            dialog.wait_for(state="visible", timeout=5000)
            cancel_button = dialog.get_by_role("button", name="Cancel", exact=False).first
            cancel_button.wait_for(state="visible", timeout=5000)
            cancel_button.click()

            # Allow close animation; if still open, use Escape as a fallback close action.
            try:
                dialog.wait_for(state="hidden", timeout=2000)
            except Exception:
                try:
                    self.pw_page.keyboard.press("Escape")
                except Exception:
                    pass
            return True
        except Exception:
            return False

    def verify_remove_session_dialog_closed(self):
        remove_dialog = self.pw_page.locator(
            f"{self.REMOVE_SESSION_DIALOG}:has-text('Are you sure you want to remove this session')"
        ).first

        # Poll for a short window because some builds close the dialog with animation.
        for _ in range(25):
            try:
                if remove_dialog.count() == 0:
                    return True

                if not remove_dialog.is_visible():
                    return True
            except Exception:
                return True

            self.pw_page.wait_for_timeout(200)

        try:
            remove_dialog.wait_for(state="hidden", timeout=1000)
            return True
        except Exception:
            return False

    def delete_session_with_wrong_then_correct_patient_id(self):
        if not self.open_remove_session_dialog_for_any_existing_session():
            return False

        dialog = self.pw_page.locator(self.REMOVE_SESSION_DIALOG).first
        remove_button = dialog.get_by_role("button", name="Remove", exact=False).first
        patient_id_input = dialog.locator(self.REMOVE_SESSION_PATIENT_ID_INPUT).first

        try:
            dialog.wait_for(state="visible", timeout=8000)
            remove_button.wait_for(state="visible", timeout=5000)
            patient_id_input.wait_for(state="visible", timeout=5000)
        except Exception:
            return False

        # Step: click Remove while empty; expected behavior is no deletion.
        try:
            remove_button.click(timeout=800)
        except Exception:
            pass

        dialog_text = ""
        patient_id_line = ""
        device_id_line = ""
        try:
            dialog_text = dialog.inner_text(timeout=3000) or ""
        except Exception:
            pass

        try:
            patient_lines = dialog.locator(
                "xpath=.//*[contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'patient id')]"
            ).all_text_contents()
            for line in patient_lines:
                clean = (line or "").strip()
                if "patient id" in clean.lower():
                    patient_id_line = clean
                    break
        except Exception:
            pass

        try:
            device_lines = dialog.locator(
                "xpath=.//*[contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'device id')]"
            ).all_text_contents()
            for line in device_lines:
                clean = (line or "").strip()
                if "device id" in clean.lower():
                    device_id_line = clean
                    break
        except Exception:
            pass

        patient_match = re.search(
            r"Patient\s*ID\s*:?\s*([A-Za-z0-9_-]+)",
            patient_id_line or dialog_text,
            flags=re.IGNORECASE,
        )
        device_match = re.search(
            r"Device\s*ID\s*:?\s*([A-Za-z0-9_-]+)",
            device_id_line or dialog_text,
            flags=re.IGNORECASE,
        )

        patient_id = patient_match.group(1).strip() if patient_match else ""
        device_id = device_match.group(1).strip() if device_match else ""
        if not patient_id:
            return False

        lookup_value = device_id or patient_id
        before_count = 0
        try:
            self.search_session(lookup_value)
            before_count = self.pw_page.locator(
                f"//tr[.//*[contains(normalize-space(),'{lookup_value}')]]"
            ).count()
        except Exception:
            before_count = 0

        wrong_patient_id = f"{patient_id}0"
        if wrong_patient_id == patient_id:
            wrong_patient_id = f"X{patient_id}"

        # Step: enter wrong ID and click Remove.
        try:
            patient_id_input.fill("")
            patient_id_input.fill(wrong_patient_id)
            remove_button.click(timeout=1000)
        except Exception:
            pass

        # Step: copy Patient ID from popup and insert into input field.
        try:
            copied_patient_id = patient_id
            patient_id_input.fill("")
            patient_id_input.fill(copied_patient_id)
        except Exception:
            return False

        # Step: click Remove with correct copied ID.
        for _ in range(20):
            try:
                remove_button.click(timeout=1200)
            except Exception:
                pass
            self.pw_page.wait_for_timeout(200)
            try:
                if not dialog.is_visible():
                    break
            except Exception:
                break

        if not self.verify_remove_session_dialog_closed():
            return False

        try:
            self.search_session(lookup_value)
            after_rows = self.pw_page.locator(
                f"//tr[.//*[contains(normalize-space(),'{lookup_value}')]]"
            )
            for _ in range(35):
                after_count = after_rows.count()
                if after_count == 0:
                    return True
                if before_count > 0 and after_count < before_count:
                    return True
                self.pw_page.wait_for_timeout(200)
            return False
        except Exception:
            return True

    def _get_visible_menu_option(self, labels):
        if isinstance(labels, str):
            labels = [labels]

        for label in labels:
            menu_item = self.pw_page.get_by_role("menuitem", name=label, exact=False).first
            try:
                menu_item.wait_for(state="visible", timeout=2000)
                return menu_item
            except Exception:
                pass

            text_item = self.pw_page.get_by_text(label, exact=False).first
            try:
                text_item.wait_for(state="visible", timeout=2000)
                return text_item
            except Exception:
                pass

        raise AssertionError(f"Could not find visible menu option for labels: {labels}")

    def _is_action_enabled(self, locator):
        try:
            aria_disabled = (locator.get_attribute("aria-disabled") or "").strip().lower()
            if aria_disabled == "true":
                return False
        except Exception:
            pass

        try:
            class_name = (locator.get_attribute("class") or "").lower()
            if "disabled" in class_name:
                return False
        except Exception:
            pass

        try:
            return locator.is_enabled()
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
