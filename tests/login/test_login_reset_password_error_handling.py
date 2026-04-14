import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from tests.test_base_online import TestBaseOnline


class TestLoginResetPasswordErrorHandling(TestBaseOnline):

    def open_login_page(self) -> LogInOnline:
        return self.browser_online.navigate(configuration["online_url"], LogInOnline)

    @pytest.mark.usefixtures("before_after_test")
    def test_reset_password_request_code_with_empty_email_shows_error(self):
        page = self.open_login_page()
        forgot_password_page = page.open_forgot_password()

        forgot_password_page.request_code("")

        assert forgot_password_page.verify_email_error_message("Email is required"), (
            "Expected 'Email is required' when Request Code is clicked with empty email."
        )
        assert forgot_password_page.verify_email_marked_red(), (
            "Expected email field to be visually marked as invalid."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_reset_password_request_code_with_invalid_email_shows_error(self):
        page = self.open_login_page()
        forgot_password_page = page.open_forgot_password()

        forgot_password_page.request_code("user")

        assert forgot_password_page.verify_email_error_message("Please enter a valid email address"), (
            "Expected invalid-email validation message when Request Code is clicked with malformed email."
        )
        assert forgot_password_page.verify_email_marked_red(), (
            "Expected email field to be visually marked as invalid."
        )
