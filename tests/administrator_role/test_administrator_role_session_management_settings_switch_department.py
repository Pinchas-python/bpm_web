import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pinimari1@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm1234567!")


class TestAdministratorRoleSessionManagementSettingsSwitchDepartment(TestBaseOnline):
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
    def test_administrator_session_management_settings_switch_between_departments(self):
        session_page = self._login_to_session_management()
        assert session_page.verify_required_controls_opened(), "Session management screen did not load."

        session_page.open_settings_menu()
        assert session_page.verify_settings_menu_opened(), (
            "Settings menu did not open with required options."
        )
        assert session_page.verify_choose_department_visible(), (
            "Expected 'Choose Department' option in settings menu."
        )
        assert session_page.switch_to_other_department_from_settings(), (
            "Could not switch to another department from settings menu."
        )
