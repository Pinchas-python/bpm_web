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


class TestAdministratorRoleScreenFunctionality(TestBaseOnline):

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
		return session_page, patient_admission_page

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_screen_opens_with_required_controls(self):
		_, admission = self._login_and_open_patient_admission()
		assert admission.verify_opened(), "Patient admission screen is missing one or more required controls."

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_close_popup_cancel_keeps_form_open(self):
		_, admission = self._login_and_open_patient_admission()

		admission.pw_page.locator(admission.CLOSE_BUTTON).first.click()

		cancel_button = admission.pw_page.get_by_role("button", name="Cancel", exact=False).first
		cancel_button.wait_for(state="visible", timeout=10000)
		cancel_button.click()

		assert admission.verify_opened(), "Admission form should remain open after Cancel on exit popup."

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_close_popup_leave_returns_to_session_management(self):
		session_page, admission = self._login_and_open_patient_admission()

		admission.pw_page.locator(admission.CLOSE_BUTTON).first.click()

		leave_button = admission.pw_page.get_by_role("button", name="Leave", exact=False).first
		leave_button.wait_for(state="visible", timeout=10000)
		leave_button.click()

		admission.pw_page.wait_for_load_state("domcontentloaded", timeout=15000)
		assert SESSION_URL_FRAGMENT in admission.pw_page.url or session_page.verify_session_management_page_opened(), (
			f"Expected to return to session management after Leave, got '{admission.pw_page.url}'"
		)
