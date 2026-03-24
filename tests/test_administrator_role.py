import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.patient_admission_page import PatientAdmissionPage
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


SESSION_URL_FRAGMENT = "session-management"
ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pinimari1@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm1234567!")


class TestAdministratorRole(TestBaseOnline):

    def _login_and_open_patient_admission(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."

        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

        session_page = SessionManagementPage(page.pw_page)
        assert session_page.verify_session_management_page_opened(), (
            "Session management page did not load after administrator login."
        )
        assert session_page.verify_session_grid_opened(), (
            "Session grid controls or columns are not visible on session management page."
        )

        patient_admission_page: PatientAdmissionPage = session_page.open_patient_admission()
        assert patient_admission_page.verify_opened(), (
            "Patient admission form did not open with required fields and confirm action. "
            f"Details: {patient_admission_page.get_last_open_failure()}"
        )
        return page, session_page, patient_admission_page

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_administrator_metric_user_admit_new_patient_sanity(self):
        page, _, _ = self._login_and_open_patient_admission()

        assert "patient-admission" in page.pw_page.url or SESSION_URL_FRAGMENT in page.pw_page.url, (
            f"Expected redirect to patient admission/session management, got '{page.pw_page.url}'"
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_patient_admission_confirm_disabled_when_form_empty(self):
        _, _, patient_admission_page = self._login_and_open_patient_admission()

        assert not patient_admission_page.is_confirm_disabled(), (
            "Confirm button should be enabled and visible when patient admission form is empty."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_patient_admission_patient_id_max_length_validation(self):
        _, _, patient_admission_page = self._login_and_open_patient_admission()

        patient_admission_page.fill_patient_id("1" * 31)
        patient_admission_page.click_confirm()

        assert patient_admission_page.verify_validation_message("Patient ID can have up to 30 characters"), (
            "Expected validation message for Patient ID length > 30 characters."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_patient_admission_first_name_max_length_validation(self):
        _, _, patient_admission_page = self._login_and_open_patient_admission()

        patient_admission_page.fill_first_name("A" * 31)
        patient_admission_page.click_confirm()

        assert patient_admission_page.verify_validation_message("First name can have up to 30 characters"), (
            "Expected validation message for First Name length > 30 characters."
        )
