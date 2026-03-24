import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


SESSION_URL_FRAGMENT = "session-management"
ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pini.mari@bio-beat.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm123456!")


class TestAdministratorRole(TestBaseOnline):

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_administrator_metric_user_admit_new_patient_sanity(self):
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."

        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

        session_page = SessionManagementPage(page.pw_page)
        assert session_page.verify_session_management_page_opened(), (
            "Session management page did not load after administrator login."
        )
        assert session_page.verify_session_grid_opened(), (
            "Session grid controls or columns are not visible on session management page."
        )

        assert SESSION_URL_FRAGMENT in page.pw_page.url, (
            f"Expected redirect to session management, got '{page.pw_page.url}'"
        )

        session_page.open_patient_admission()
        assert session_page.verify_patient_admission_form_opened(), (
            "Patient admission form did not open with required fields and confirm action."
        )
