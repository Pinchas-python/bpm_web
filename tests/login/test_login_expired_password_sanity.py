import pytest
import os

from infra.config.config_provider import configuration
from logic.pages.forgot_password_page import ForgotPasswordPage
from logic.pages.login_page import LogInOnline
from tests.test_base_online import TestBaseOnline


class TestLoginExpiredPasswordSanity(TestBaseOnline):
    expired_user_email = os.getenv("EXPIRED_USER_EMAIL")
    expired_user_password = os.getenv("EXPIRED_USER_PASSWORD")

    def open_login_page(self) -> LogInOnline:
        return self.browser_online.navigate(configuration["online_url"], LogInOnline)

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_expired_password_opens_reset_password_screen(self):
        page = self.open_login_page()
        page.login(self.expired_user_email, self.expired_user_password)

        assert page.pw_page.get_by_text("Your password has expired", exact=False).first.is_visible(timeout=15000), (
            "Expected 'Your password has expired' message after login with expired credentials."
        )

        forgot_password_page = ForgotPasswordPage(page.pw_page)
        assert forgot_password_page.verify_verification_screen_opened(), (
            "Expected verification code/new password/confirm password/reset password controls to be visible."
        )
        assert page.pw_page.locator("button:has-text('Resend')").first.is_visible(timeout=10000), (
            "Expected Resend verification code button to be visible on expired-password screen."
        )
        assert page.pw_page.locator(forgot_password_page.BACK_TO_LOGIN).first.is_visible(timeout=10000), (
            "Expected Back to Login button to be visible on expired-password screen."
        )
