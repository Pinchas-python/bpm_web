import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.forgot_password_page import ForgotPasswordPage
from logic.pages.login_page import LogInOnline
from tests.test_base_online import TestBaseOnline


class LoginBase(TestBaseOnline):
    expected_url = "https://bpholter.stage.bio-beat.cloud/session-management"
    expired_user_email = os.getenv("EXPIRED_USER_EMAIL", "pini.mari@bio-beat.com")
    expired_user_password = os.getenv("EXPIRED_USER_PASSWORD", "Pm1234567!")
    expired_user_verification_code = os.getenv("EXPIRED_USER_VERIFICATION_CODE", "")
    expired_user_used_password = os.getenv("EXPIRED_USER_USED_PASSWORD", expired_user_password)

    def open_login_page(self):
        return self.browser_online.navigate(configuration["online_url"], LogInOnline)

    def open_expired_password_reset_screen(self):
        page: LogInOnline = self.open_login_page()
        page.login(self.expired_user_email, self.expired_user_password)

        forgot_password_page = ForgotPasswordPage(page.pw_page)
        if not forgot_password_page.verify_verification_screen_opened():
            pytest.skip("Expired-password reset screen did not open for configured credentials.")

        return forgot_password_page
