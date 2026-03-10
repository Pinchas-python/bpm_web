import pytest
from tests.test_base_online import TestBaseOnline
#from tests.Test_Online.test_base_online import TestBaseOnline
from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
import json


class TestLoginOnline(TestBaseOnline):

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_log_in_online_with_lupa(self):
        expected_url = "https://bpholter.stage.bio-beat.cloud/session-management"
        page: LogInOnline = self.browser_online.navigate(configuration['online_url'], LogInOnline)
        page.enter_username("pini.mari@bio-beat.com")
        page.enter_password("Pm123456!")
        page.click_login_button()
        page.pw_page.wait_for_url(expected_url, timeout=15000)

        assert page.pw_page.url == expected_url, (
            f"Expected URL '{expected_url}', but got '{page.pw_page.url}'"
        )