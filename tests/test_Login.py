import os
import pytest
from tests.test_base_online import TestBaseOnline
from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.forgot_password_page import ForgotPasswordPage

expected_url = "https://bpholter.stage.bio-beat.cloud/session-management"
EXPIRED_USER_EMAIL = os.getenv("EXPIRED_USER_EMAIL", "pini.mari@bio-beat.com")
EXPIRED_USER_PASSWORD = os.getenv("EXPIRED_USER_PASSWORD", "Pm1234567!")
EXPIRED_USER_VERIFICATION_CODE = os.getenv("EXPIRED_USER_VERIFICATION_CODE", "")
EXPIRED_USER_USED_PASSWORD = os.getenv("EXPIRED_USER_USED_PASSWORD", EXPIRED_USER_PASSWORD)

class TestLoginOnline(TestBaseOnline):

    def _open_expired_password_reset_screen(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login(EXPIRED_USER_EMAIL, EXPIRED_USER_PASSWORD)

        forgot_password_page = ForgotPasswordPage(page.pw_page)
        if not forgot_password_page.verify_verification_screen_opened():
            pytest.skip("Expired-password reset screen did not open for configured credentials.")

        return forgot_password_page

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_open_login_page(self):  
        page: LogInOnline = self.browser_online.navigate(configuration['online_url'], LogInOnline)
        assert page.verify_login_page_opened(), (
            "The login page should show Email and Password fields and the "
            "'Forgot your password?' and 'Log in' buttons."
        )


    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_Login_with_valid_credentials_santy(self):  
        page: LogInOnline = self.browser_online.navigate(configuration['online_url'], LogInOnline)
        page.login("pinimari1@gmail.com","Pm1234567!")
        page.pw_page.wait_for_url(expected_url, timeout=15000)
        assert page.pw_page.url == expected_url, (
            f"Expected URL '{expected_url}', but got '{page.pw_page.url}'"
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_invalid_credentials_shows_error(self):
        page: LogInOnline = self.browser_online.navigate(configuration['online_url'], LogInOnline)
        page.login("wrong.user@bio-beat.com", "Pm123456!")
        page.pw_page.wait_for_timeout(2000)

        assert page.verify_login_page_opened(), "Expected to remain on login form after failed authentication."
        assert "/login" in page.pw_page.url, f"Expected to remain on login page, got '{page.pw_page.url}'"
        assert page.pw_page.url != expected_url, "Invalid credentials must not navigate to the session page."

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_empty_email_and_password(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline )
        page.login("", "")

        assert page.verify_error_message("email is required")
        assert page.verify_email_marked_red()

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_empty_password(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login("pini.mari@bio-beat.com", "")
        assert page.verify_error_message("Password is required")
        assert page.verify_password_marked_red()

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_empty_email(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login("", "123456")

        assert page.verify_error_message("email is required")
        assert page.verify_email_marked_red()

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_invalid_email_format(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login("user@,user.com", "123456")

        assert page.verify_error_message("Incorrect email or password")


    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_wrong_email(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login("wrong@bio-beat.com", "ValidPassword123")

        assert page.verify_error_message("Incorrect email or password")

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_deleted_user(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login("deleted.user@bio-beat.com", "ValidPassword123")

        assert page.verify_error_message("Incorrect email or password")

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_short_password(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login("pini.mari@bio-beat.com", "12")

        assert page.verify_error_message("Incorrect email or password")

    @pytest.mark.usefixtures("before_after_test")
    def test_open_forgot_password_page(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        forgot_password_page = page.open_forgot_password()

        assert forgot_password_page.verify_forgot_password_page_opened(), (
            "Forgot password screen should show Email field, 'Back to login page', and 'Request Code'."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_request_code_opens_verification_screen(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        forgot_password_page = page.open_forgot_password()

        forgot_password_page.request_code("pini.mari@bio-beat.com")

        assert forgot_password_page.verify_verification_screen_opened(), (
            "Verification screen should show verification code, new password, confirm password, "
            "and change password controls after requesting a code."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_reset_password_request_code_with_empty_email_shows_error(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
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
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        forgot_password_page = page.open_forgot_password()

        forgot_password_page.request_code("user")

        assert forgot_password_page.verify_email_error_message("Please enter a valid email address"), (
            "Expected invalid-email validation message when Request Code is clicked with malformed email."
        )
        assert forgot_password_page.verify_email_marked_red(), (
            "Expected email field to be visually marked as invalid."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_expired_password_opens_reset_password_screen(self):
        
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        page.login(EXPIRED_USER_EMAIL, EXPIRED_USER_PASSWORD)

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

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_last_used_password_shows_error(self):
        if not EXPIRED_USER_VERIFICATION_CODE:
            pytest.skip("Set EXPIRED_USER_VERIFICATION_CODE for this test.")

        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.change_password(
            EXPIRED_USER_VERIFICATION_CODE,
            EXPIRED_USER_USED_PASSWORD,
            EXPIRED_USER_USED_PASSWORD,
        )

        assert forgot_password_page.verify_reset_password_error_message("Password has previously been used"), (
            "Expected error: 'Password has previously been used'."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_invalid_password_shows_error(self):
        if not EXPIRED_USER_VERIFICATION_CODE:
            pytest.skip("Set EXPIRED_USER_VERIFICATION_CODE for this test.")

        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.change_password(EXPIRED_USER_VERIFICATION_CODE, "abc", "abc")

        assert forgot_password_page.verify_reset_password_error_message(
            "Password must have at least 8 characters, and contain upper case, lower case, numeric, and special characters"
        ), "Expected password complexity error for invalid password."

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_invalid_confirm_password_shows_error(self):
        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.change_password("123456", "Valid@123", "Invalid@123")

        assert forgot_password_page.verify_reset_password_error_message("Passwords do not match"), (
            "Expected mismatch error when confirm password does not match."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_all_fields_empty_shows_verification_code_required(self):
        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.click_change_password()

        assert forgot_password_page.verify_reset_password_error_message("Verification code is required"), (
            "Expected 'Verification code is required' when all fields are empty."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_empty_code_shows_code_cannot_be_empty(self):
        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.change_password("", "Valid@123", "Valid@123")

        assert forgot_password_page.verify_reset_password_error_message("Verification code cannot be empty"), (
            "Expected 'Verification code cannot be empty' when verification code field is blank."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_empty_password_shows_password_cannot_be_empty(self):
        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.change_password("123456", "", "")

        assert forgot_password_page.verify_reset_password_error_message("Password cannot be empty"), (
            "Expected 'Password cannot be empty' when password field is blank."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_empty_confirm_shows_confirm_required(self):
        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.change_password("123456", "Valid@123", "")

        assert forgot_password_page.verify_reset_password_error_message("Please confirm password to continue"), (
            "Expected confirm-password required message when confirm field is blank."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_expired_password_change_with_wrong_code_shows_invalid_code_error(self):
        forgot_password_page = self._open_expired_password_reset_screen()
        forgot_password_page.change_password("000000", "Valid@123", "Valid@123")

        assert forgot_password_page.verify_reset_password_error_message(
            "Invalid verification code provided, please try again"
        ), "Expected invalid verification code error for wrong verification code."

    

