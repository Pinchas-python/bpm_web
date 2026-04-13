import pytest

from tests.login.login_base import LoginBase


class TestLoginResetPasswordSanity(LoginBase):

    @pytest.mark.usefixtures("before_after_test")
    def test_open_forgot_password_page(self):
        page = self.open_login_page()
        forgot_password_page = page.open_forgot_password()

        assert forgot_password_page.verify_forgot_password_page_opened(), (
            "Forgot password screen should show Email field, 'Back to login page', and 'Request Code'."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_request_code_opens_verification_screen(self):
        page = self.open_login_page()
        forgot_password_page = page.open_forgot_password()

        forgot_password_page.request_code("pini.mari@bio-beat.com")

        assert forgot_password_page.verify_verification_screen_opened(), (
            "Verification screen should show verification code, new password, confirm password, "
            "and change password controls after requesting a code."
        )
