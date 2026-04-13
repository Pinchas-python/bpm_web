import pytest

from tests.login.login_base import LoginBase


class TestLoginExpiredPasswordResendVerificationCode(LoginBase):

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_resend_button_visible(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        assert forgot_password_page.pw_page.locator("button:has-text('Resend')").first.is_visible(timeout=10000), (
            "Expected Resend verification code button to be visible on expired-password screen."
        )
