import pytest
import os

from infra.config.config_provider import configuration
from logic.pages.forgot_password_page import ForgotPasswordPage
from logic.pages.login_page import LogInOnline
from tests.test_base_online import TestBaseOnline


class TestLoginExpiredPasswordErrorHandling(TestBaseOnline):
    expired_user_email = os.getenv("EXPIRED_USER_EMAIL")
    expired_user_password = os.getenv("EXPIRED_USER_PASSWORD")
    expired_user_verification_code = os.getenv("EXPIRED_USER_VERIFICATION_CODE", "")
    expired_user_used_password = os.getenv("EXPIRED_USER_USED_PASSWORD", expired_user_password)

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
    def test_expired_password_change_with_last_used_password_shows_error(self):
        if not self.expired_user_verification_code:
            pytest.skip("Set EXPIRED_USER_VERIFICATION_CODE for this test.")

        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.change_password(
            self.expired_user_verification_code,
            self.expired_user_used_password,
            self.expired_user_used_password,
        )

        assert forgot_password_page.verify_reset_password_error_message("Password has previously been used"), (
            "Expected error: 'Password has previously been used'."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_invalid_password_shows_error(self):
        if not self.expired_user_verification_code:
            pytest.skip("Set EXPIRED_USER_VERIFICATION_CODE for this test.")

        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.change_password(self.expired_user_verification_code, "abc", "abc")

        assert forgot_password_page.verify_reset_password_error_message(
            "Password must have at least 8 characters, and contain upper case, lower case, numeric, and special characters"
        ), "Expected password complexity error for invalid password."

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_invalid_confirm_password_shows_error(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.change_password("123456", "Valid@123", "Invalid@123")

        assert forgot_password_page.verify_reset_password_error_message("Passwords do not match"), (
            "Expected mismatch error when confirm password does not match."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_all_fields_empty_shows_verification_code_required(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.click_change_password()

        assert forgot_password_page.verify_reset_password_error_message("Verification code is required"), (
            "Expected 'Verification code is required' when all fields are empty."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_empty_code_shows_code_cannot_be_empty(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.change_password("", "Valid@123", "Valid@123")

        assert forgot_password_page.verify_reset_password_error_message("Verification code cannot be empty"), (
            "Expected 'Verification code cannot be empty' when verification code field is blank."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_empty_password_shows_password_cannot_be_empty(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.change_password("123456", "", "")

        assert forgot_password_page.verify_reset_password_error_message("Password cannot be empty"), (
            "Expected 'Password cannot be empty' when password field is blank."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_empty_confirm_shows_confirm_required(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.change_password("123456", "Valid@123", "")

        assert forgot_password_page.verify_reset_password_error_message("Please confirm password to continue"), (
            "Expected confirm-password required message when confirm field is blank."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_wrong_code_shows_invalid_code_error(self):
        forgot_password_page = self.open_expired_password_reset_screen()
        forgot_password_page.change_password("000000", "Valid@123", "Valid@123")

        assert forgot_password_page.verify_reset_password_error_message(
            "Invalid verification code provided, please try again"
        ), "Expected invalid verification code error for wrong verification code."
