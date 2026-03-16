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

