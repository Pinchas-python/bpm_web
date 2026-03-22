import pytest
from tests.test_base_online import TestBaseOnline
from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
expected_url = "https://bpholter.stage.bio-beat.cloud/session-management"

class TestLoginOnline(TestBaseOnline):

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
        page.login("pini.mari@bio-beat.com","Pm123456!")
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

    

