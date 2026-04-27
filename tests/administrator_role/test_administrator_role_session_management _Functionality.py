import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pinimari1@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm1234567!")


class TestAdministratorRoleSessionManagementFunctionality(TestBaseOnline):
	def _login_to_session_management(self) -> SessionManagementPage:
		page: LogInOnline = self.browser_online.navigate(configuration["online_url_stage"], LogInOnline)
		assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."

		page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

		session_page = SessionManagementPage(page.pw_page)
		assert session_page.verify_session_management_page_opened(), (
			"Session management page did not load after administrator login."
		)
		return session_page

	@pytest.mark.usefixtures("before_after_test")
	def test_open_session_management_screen_with_required_controls(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), (
			"Session table and required columns/controls were not fully visible."
		)

	@pytest.mark.usefixtures("before_after_test")
	@pytest.mark.parametrize(
		"status_value, expect_edit_enabled",
		[
			("Complete limited", False),
			("Complete", False),
			("Active", False),
			("Pending", True),
		],
	)
	def test_row_actions_by_patient_status(self, status_value: str, expect_edit_enabled: bool):
		session_page = self._login_to_session_management()
		assert session_page.verify_row_actions_by_status(status_value, expect_edit_enabled), (
			f"Unexpected row action state for status '{status_value}'."
		)
