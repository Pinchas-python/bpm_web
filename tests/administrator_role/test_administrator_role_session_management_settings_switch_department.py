import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD")


class TestAdministratorRoleSessionManagementSettingsSwitchDepartment(TestBaseOnline):
    def _login_to_session_management(self) -> SessionManagementPage:
        page: LogInOnline = self.browser_online.navigate(configuration["online_url"], LogInOnline)
        assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."

        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

        session_page = SessionManagementPage(page.pw_page)
        assert session_page.verify_session_management_page_opened(), (
            "Session management page did not load after administrator login."
        )
        return session_page

    @pytest.mark.usefixtures("before_after_test")
    def test_administrator_session_management_settings_switch_between_departments(self):
        session_page = self._login_to_session_management()
        assert session_page.verify_required_controls_opened(), "Session management screen did not load."

        session_page.open_settings_menu()
        assert session_page.verify_settings_menu_opened(), (
            "Settings menu did not open with required options."
        )
        assert session_page.verify_choose_department_visible(), (
            "Expected 'Choose Department' option in settings menu."
        )
        assert session_page.switch_to_other_department_from_settings(), (
            "Could not switch to another department from settings menu."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_login_opens_session_management_with_all_required_controls(self):
        session_page = self._login_to_session_management()
        assert session_page.verify_required_controls_opened(), (
            "Session management screen is missing one or more required controls after login."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_settings_menu_opens_with_client_name_email_choose_department_and_logout(self):
        session_page = self._login_to_session_management()
        session_page.open_settings_menu()
        assert session_page.verify_settings_menu_opened(), (
            "Settings menu did not open with client name, email, 'Choose Department' and 'Log out'."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_choose_department_shows_dropdown_with_available_departments(self):
        session_page = self._login_to_session_management()
        session_page.open_settings_menu()
        assert session_page.verify_choose_department_visible(), (
            "Expected 'Choose Department' option in settings menu."
        )
        assert session_page._open_choose_department_selector(), (
            "Department selector dropdown did not open after clicking 'Choose Department'."
        )
        departments = session_page._get_department_options()
        assert len(departments) >= 1, (
            "Expected at least one department to be listed in the dropdown."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_selecting_department_opens_session_management_for_that_department(self):
        session_page = self._login_to_session_management()
        assert session_page.switch_to_other_department_from_settings(), (
            "Could not switch to a different department from the settings menu."
        )
        assert session_page.verify_session_management_page_opened(), (
            "Session management screen did not open for the newly selected department."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_search_session_from_previous_department_shows_no_results(self):
        session_page = self._login_to_session_management()

        # Remember the first session visible before switching.
        first_session = session_page.get_first_session_row_field_value("Patient ID")

        assert session_page.switch_to_other_department_from_settings(), (
            "Could not switch to a different department."
        )
        assert session_page.verify_session_management_page_opened(), (
            "Session management page did not reload after switching department."
        )

        if first_session:
            session_page.search_session(first_session)
            assert session_page.verify_table_shows_no_results(), (
                f"Expected no results when searching for '{first_session}' from the previous department."
            )

    @pytest.mark.usefixtures("before_after_test")
    def test_patient_lookup_screen_opens_with_required_controls_and_columns(self):
        session_page = self._login_to_session_management()
        session_page.open_patient_lookup()
        assert session_page.verify_patient_lookup_opened(), (
            "Patient lookup screen did not open with the expected title, search field and 'New Patient' button."
        )
        assert session_page.verify_patient_lookup_table_columns_visible(), (
            "Patient lookup table is missing one or more expected columns "
            "(Patient ID, First name, Last name, Last session, Department)."
        )

    @pytest.mark.usefixtures("before_after_test")
    def test_search_patient_from_previous_department_in_lookup_shows_no_results(self):
        session_page = self._login_to_session_management()

        first_patient = session_page.get_first_session_row_field_value("Patient ID")

        assert session_page.switch_to_other_department_from_settings(), (
            "Could not switch to a different department."
        )
        assert session_page.verify_session_management_page_opened(), (
            "Session management page did not reload after switching department."
        )

        session_page.open_patient_lookup()
        assert session_page.verify_patient_lookup_opened(), (
            "Patient lookup screen did not open after switching department."
        )

        if first_patient:
            session_page.search_patient_lookup(first_patient)
            assert session_page.verify_table_shows_no_results(), (
                f"Expected no results in Patient Lookup when searching for '{first_patient}' "
                "from the previous department."
            )

    @pytest.mark.usefixtures("before_after_test")
    def test_choosing_different_department_displays_its_sessions(self):
        session_page = self._login_to_session_management()
        assert session_page.switch_to_other_department_from_settings(), (
            "Could not switch to a different department."
        )
        assert session_page.verify_session_management_page_opened(), (
            "Session management screen did not open after switching to a different department."
        )
        assert session_page.verify_session_grid_opened(), (
            "Session grid did not load correctly for the newly selected department."
        )
