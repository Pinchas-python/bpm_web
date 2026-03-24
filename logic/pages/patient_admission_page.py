from infra.page_base import PageBase
import re


class PatientAdmissionPage(PageBase):
    # Main admission fields
    PATIENT_ID_INPUT = (
        "input[name*='patient_id'], input[name*='patientId'], input[placeholder*='Patient ID']"
    )
    DEVICE_ID_INPUT = (
        "input[name*='device_id'], input[name*='deviceId'], input[placeholder*='Device ID']"
    )
    FIRST_NAME_INPUT = (
        "input[name*='firstName'], input[placeholder*='First Name']"
    )
    LAST_NAME_INPUT = (
        "input[name*='lastName'], input[placeholder*='Last Name']"
    )
    FIRST_NAME_LABEL = "First Name"
    LAST_NAME_LABEL = "Last Name"

    # Form controls/options
    GENDER_AT_BIRTH_LABEL = "Gender at birth"
    MALE_OPTION_LABEL = "Male"
    FEMALE_OPTION_LABEL = "Female"
    DOB_INPUT = "input[placeholder*='Date of Birth'], input[name*='dob'], input[name*='birth']"
    WEIGHT_INPUT = "input[placeholder*='Weight'], input[name*='weight']"
    HEIGHT_INPUT = "input[placeholder*='Height'], input[name*='height']"
    REFERRING_PHYSICIAN_DROPDOWN = (
        "input[name*='referring_physician'], input[name*='referringPhysician'], "
        "[role='combobox']:has-text('Referring Physician'), select[name*='physician']"
    )
    ADDITIONAL_NOTES_TEXTAREA = "textarea[name*='notes'], textarea[placeholder*='notes']"
    REPORT_COMPLETION_EMAIL_TOGGLE = "input[type='checkbox'][name*='email'], [role='switch']"

    # Actions
    CONFIRM_BUTTON = (
        "//button[normalize-space()='Confirm']"
    )
    CLOSE_BUTTON = "button[aria-label*='close' i], button:has-text('X'), button:has-text('×')"

    # Validation containers
    ERROR_CONTAINER = "[class*='error'], [role='alert'], [aria-live='assertive']"

    def __init__(self, page):
        super().__init__(page)
        self._last_open_failure = ""

    def verify_opened(self):
        checks = [
            ("Patient ID input", self.PATIENT_ID_INPUT, "locator"),
            ("Device ID input", self.DEVICE_ID_INPUT, "locator"),
            ("First Name field", self.FIRST_NAME_LABEL, "text"),
            ("Last Name field", self.LAST_NAME_LABEL, "text"),
            ("Gender at birth label", self.GENDER_AT_BIRTH_LABEL, "text"),
            ("Male radio", self.MALE_OPTION_LABEL, "radio"),
            ("Female radio", self.FEMALE_OPTION_LABEL, "radio"),
            ("Date of Birth field", self.DOB_INPUT, "locator"),
            ("Weight field", self.WEIGHT_INPUT, "locator"),
            ("Height field", self.HEIGHT_INPUT, "locator"),
            ("Referring Physician", self.REFERRING_PHYSICIAN_DROPDOWN, "locator"),
            ("Additional notes", self.ADDITIONAL_NOTES_TEXTAREA, "locator"),
            ("Report completion email toggle", self.REPORT_COMPLETION_EMAIL_TOGGLE, "locator"),
            ("Confirm button", self.CONFIRM_BUTTON, "locator"),
        ]

        for label, selector, kind in checks:
            try:
                if kind == "locator":
                    self._wait_visible(selector, 10000)
                elif kind == "text":
                    self.pw_page.get_by_text(selector, exact=False).first.wait_for(state="visible", timeout=10000)
                elif kind == "radio":
                    self.pw_page.get_by_role("radio", name=selector, exact=False).first.wait_for(
                        state="visible", timeout=10000
                    )
            except Exception as exc:
                self._last_open_failure = f"Missing {label}; kind={kind}; selector={selector}; error={exc}"
                return False

        self._last_open_failure = ""

        # Some builds render a close icon without stable text/aria attributes.
        # Do not fail the whole form verification on this optional UI control.
        try:
            self._wait_visible(self.CLOSE_BUTTON, 2000)
        except Exception:
            pass

        return True

    def get_last_open_failure(self):
        return self._last_open_failure or "No admission open failure details recorded."

    def fill_patient_id(self, value: str):
        try:
            self.pw_page.get_by_label("Patient ID", exact=False).first.fill(value)
            return
        except Exception:
            pass
        self.pw_page.locator(self.PATIENT_ID_INPUT).first.fill(value)

    def fill_first_name(self, value: str):
        try:
            self.pw_page.get_by_label(self.FIRST_NAME_LABEL, exact=False).first.fill(value)
            return
        except Exception:
            pass
        self.pw_page.locator(self.FIRST_NAME_INPUT).first.fill(value)

    def click_confirm(self):
        self.pw_page.locator(self.CONFIRM_BUTTON).first.click()

    def is_confirm_disabled(self):
        locator = self.pw_page.locator(self.CONFIRM_BUTTON).first
        locator.wait_for(state="visible", timeout=10000)

        try:
            if locator.is_disabled():
                return True
        except Exception:
            pass

        try:
            if (locator.get_attribute("aria-disabled") or "").lower() == "true":
                return True
        except Exception:
            pass

        try:
            class_name = (locator.get_attribute("class") or "").lower()
            if "disabled" in class_name:
                return True
        except Exception:
            pass

        return False

    def verify_validation_message(self, expected_message: str):
        expected = self._normalize(expected_message)
        if not expected:
            return False

        try:
            locator = self.pw_page.get_by_text(expected_message, exact=False).first
            if locator.is_visible(timeout=3000):
                actual = self._normalize(locator.text_content() or "")
                if actual == expected:
                    return True
        except Exception:
            pass

        for selector in [self.ERROR_CONTAINER, "text=/up to 30 characters/i"]:
            try:
                candidate = self.pw_page.locator(selector).first
                if candidate.is_visible(timeout=1000):
                    actual = self._normalize(candidate.text_content() or "")
                    if actual == expected:
                        return True
            except Exception:
                continue

        return False

    def _wait_visible(self, selector: str, timeout: int):
        self.pw_page.locator(selector).first.wait_for(state="visible", timeout=timeout)

    def _normalize(self, value: str):
        text = (value or "").strip().lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return " ".join(text.split())
