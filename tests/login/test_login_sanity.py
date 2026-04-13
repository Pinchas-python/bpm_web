import pytest

from tests.login.login_base import LoginBase


class TestLoginSanity(LoginBase):

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_open_login_page(self):
        page = self.open_login_page()
        assert page.verify_login_page_opened(), (
            "The login page should show Email and Password fields and the "
            "'Forgot your password?' and 'Log in' buttons."
        )

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_login_with_valid_credentials_sanity(self):
        page = self.open_login_page()
        page.login("pinimari1@gmail.com", "Pm1234567!")
        page.pw_page.wait_for_url(self.expected_url, timeout=15000)
        assert page.pw_page.url == self.expected_url, (
            f"Expected URL '{self.expected_url}', but got '{page.pw_page.url}'"
        )
