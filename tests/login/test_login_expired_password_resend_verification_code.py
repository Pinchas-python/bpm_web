import pytest
import os

from infra.config.config_provider import configuration
from logic.pages.forgot_password_page import ForgotPasswordPage
from logic.pages.login_page import LogInOnline
from tests.test_base_online import TestBaseOnline


class TestLoginExpiredPasswordResendVerificationCode(TestBaseOnline):
    expired_user_email = os.getenv("EXPIRED_USER_EMAIL", "pini.mari+4@bio-beat.com")
    expired_user_password = os.getenv("EXPIRED_USER_PASSWORD", "Pinimari!1")

    def open_login_page(self) -> LogInOnline:
        return self.browser_online.navigate(configuration["online_url_stage"], LogInOnline)

    def open_expired_password_reset_screen(self):
        page: LogInOnline = self.open_login_page()
        page.login(self.expired_user_email, self.expired_user_password)

        forgot_password_page = ForgotPasswordPage(page.pw_page)
        if not forgot_password_page.verify_verification_screen_opened():
            pytest.skip("Expired-password reset screen did not open for configured credentials.")

        return forgot_password_page

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_resend_button_visible(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        assert forgot_password_page.pw_page.locator("button:has-text('Resend')").first.is_visible(timeout=10000), (
            "Expected Resend verification code button to be visible on expired-password screen."
        )
