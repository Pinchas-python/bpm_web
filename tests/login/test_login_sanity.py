import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


class TestLoginSanity(TestBaseOnline):
    expected_url = "https://bpholter.stage.bio-beat.cloud/session-management"
    expected_client_name = "pinitesting"
    metric_user_email = "pinimari1@gmail.com"
    metric_user_password = "Pm1234567!"

    def open_login_page(self) -> LogInOnline:
        page: LogInOnline = self.browser_online.navigate(configuration["online_url_stage"], LogInOnline)
        return page

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_open_login_page(self):
        page: LogInOnline = self.open_login_page()
        assert page.verify_login_page_opened(), (
            "The login page should show Email and Password fields and the "
            "'Forgot your password?' and 'Log in' buttons."
        )

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_valid_credentials_sanity(self):
        page: LogInOnline = self.open_login_page()
        page.login(self.metric_user_email, self.metric_user_password)
        page.pw_page.wait_for_url(self.expected_url, timeout=15000)
        assert page.pw_page.url == self.expected_url, (
            f"Expected URL '{self.expected_url}', but got '{page.pw_page.url}'"
        )

        session_page = SessionManagementPage(page.pw_page)
        assert session_page.verify_session_management_page_opened(), (
            "Session management page did not open after successful login."
        )
        assert session_page.verify_session_grid_opened(), (
            "Session grid controls/headers are not visible after successful login."
        )

        assert page.pw_page.locator(session_page.SESSION_MANAGEMENT_HEADER).first.is_visible(timeout=10000)
        assert page.pw_page.locator(session_page.PATIENT_ADMISSION_NAV).first.is_visible(timeout=10000)
        assert page.pw_page.locator(session_page.PATIENT_LOOKUP_NAV).first.is_visible(timeout=10000)

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_login_and_check_settings_menu_opens_sanity(self):
        page: LogInOnline = self.open_login_page()
        page.login(self.metric_user_email, self.metric_user_password)

        session_page = SessionManagementPage(page.pw_page)
        assert session_page.verify_session_management_page_opened(), (
            "Session management page did not open after successful login."
        )
        session_page.open_settings_menu()
        assert session_page.verify_settings_menu_opened(), (
            "Expected Email Support, Choose Department, and Log out options in settings menu."
        )
        assert session_page.verify_email_support_visible(), (
            "Expected 'Email Support' text to be displayed in settings menu."
        )
        assert session_page.verify_choose_department_visible(), (
            "Expected 'Choose Department' text to be displayed in settings menu."
        )
        assert session_page.verify_settings_client_name_equals(self.expected_client_name), (
            f"Expected client name '{self.expected_client_name}' in settings menu."
        )
        assert session_page.verify_settings_user_email_visible(self.metric_user_email), (
            "Expected logged-in user email at top of settings menu."
        )

        # Logout returns to login page.
        session_page.click_logout()
        assert page.verify_login_page_opened(), "Expected login page after clicking 'Log out'."