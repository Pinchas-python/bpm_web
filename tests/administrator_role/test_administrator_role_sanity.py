import os
import pytest
from typing import Tuple

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.patient_admission_page import PatientAdmissionPage
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


SESSION_URL_FRAGMENT = "session-management"
ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pinimari1@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm1234567!")


class TestAdministratorRoleSanity(TestBaseOnline):

	def _open_login_page(self) -> LogInOnline:
		page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
		assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."
		return page

	def _login_to_session_management(self, page: LogInOnline) -> SessionManagementPage:
		page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

		session_page = SessionManagementPage(page.pw_page)
		assert session_page.verify_session_management_page_opened(), (
			"Session management page did not load after administrator login."
		)
		assert session_page.verify_session_grid_opened(), (
			"Session grid controls or columns are not visible on session management page."
		)
		return session_page

	def _open_patient_admission(
		self, session_page: SessionManagementPage
	) -> PatientAdmissionPage:
		patient_admission_page: PatientAdmissionPage = session_page.open_patient_admission()
		assert patient_admission_page.verify_opened(), (
			"Patient admission form did not open with required fields and confirm action. "
			f"Details: {patient_admission_page.get_last_open_failure()}"
		)
		return patient_admission_page

	def _login_and_open_patient_admission(
		self,
	) -> Tuple[LogInOnline, SessionManagementPage, PatientAdmissionPage]:
		page = self._open_login_page()
		session_page = self._login_to_session_management(page)
		patient_admission_page = self._open_patient_admission(session_page)
		return page, session_page, patient_admission_page

	@pytest.mark.smoke
	@pytest.mark.usefixtures("before_after_test")
	def test_administrator_metric_user_admit_new_patient_sanity(self):
		page, _, _ = self._login_and_open_patient_admission()

		assert "patient-admission" in page.pw_page.url or SESSION_URL_FRAGMENT in page.pw_page.url, (
			f"Expected redirect to patient admission/session management, got '{page.pw_page.url}'"
		)
