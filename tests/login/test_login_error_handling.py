import pytest

from tests.login.login_base import LoginBase


class TestLoginErrorHandling(LoginBase):

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_invalid_credentials_shows_error(self):
        page = self.open_login_page()
        page.login("wrong.user@bio-beat.com", "Pm123456!")
        page.pw_page.wait_for_timeout(2000)

        assert page.verify_login_page_opened(), "Expected to remain on login form after failed authentication."
        assert "/login" in page.pw_page.url, f"Expected to remain on login page, got '{page.pw_page.url}'"
        assert page.pw_page.url != self.expected_url, "Invalid credentials must not navigate to the session page."

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_empty_email_and_password(self):
        page = self.open_login_page()
        page.login("", "")

        assert page.verify_error_message("email is required")
        assert page.verify_email_marked_red()

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_empty_password(self):
        page = self.open_login_page()
        page.login("pini.mari@bio-beat.com", "")
        assert page.verify_error_message("Password is required")
        assert page.verify_password_marked_red()

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_empty_email(self):
        page = self.open_login_page()
        page.login("", "123456")

        assert page.verify_error_message("email is required")
        assert page.verify_email_marked_red()

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_invalid_email_format(self):
        page = self.open_login_page()
        page.login("user@,user.com", "123456")

        assert page.verify_error_message("Incorrect email or password")

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_wrong_email(self):
        page = self.open_login_page()
        page.login("wrong@bio-beat.com", "ValidPassword123")

        assert page.verify_error_message("Incorrect email or password")

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_deleted_user(self):
        page = self.open_login_page()
        page.login("deleted.user@bio-beat.com", "ValidPassword123")

        assert page.verify_error_message("Incorrect email or password")

    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_short_password(self):
        page = self.open_login_page()
        page.login("pini.mari@bio-beat.com", "12")

        assert page.verify_error_message("Incorrect email or password")
