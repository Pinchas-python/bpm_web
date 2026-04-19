import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pinimari1@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm1234567!")


class TestAdministratorRoleSessionManagementDeleteSessionFunctionality(TestBaseOnline):
	def _login_to_session_management(self) -> SessionManagementPage:
		page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
		assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."

		page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

		session_page = SessionManagementPage(page.pw_page)
		assert session_page.verify_session_management_page_opened(), (
			"Session management page did not load after administrator login."
		)
		return session_page

	@pytest.mark.usefixtures("before_after_test")
	def test_open_session_management_screen_for_delete_session(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), (
			"Session table and required columns/controls were not fully visible."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_three_dots_menu_shows_delete_related_actions(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_delete_related_row_actions_visible(), (
			"Expected edit, complete session, and remove options to be visible in row action menu."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_click_remove_session_then_click_cancel_closes_window(self):
		session_page = self._login_to_session_management()
		assert session_page.open_remove_session_dialog_for_any_existing_session(), (
			"Could not open remove session confirmation window from row action menu."
		)
		assert session_page.click_cancel_in_remove_session_dialog(), (
			"Could not click Cancel in remove session confirmation window."
		)
		assert session_page.verify_remove_session_dialog_closed(), (
			"The remove session confirmation window should close after clicking Cancel."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_delete_session_with_wrong_then_correct_patient_id(self):
		session_page = self._login_to_session_management()
		assert session_page.delete_session_with_wrong_then_correct_patient_id(), (
			"Delete session flow failed: expected Remove to stay disabled for empty/wrong ID, "
			"become enabled for correct Patient ID, and remove the session from the table."
		)
