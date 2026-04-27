import os
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pinimari1@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm1234567!")


class TestAdministratorRoleSessionManagementFilteringAndSorting(TestBaseOnline):
	SORTABLE_COLUMNS = [
		"Admission Date",
		"Patient ID",
		"Referring Physician",
		"Full Name",
		"Device ID",
		"Start Time",
		"Status",
		"Remaining",
	]

	def _login_to_session_management(self) -> SessionManagementPage:
		page: LogInOnline = self.browser_online.navigate(configuration["online_url_stage"], LogInOnline)
		assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."

		page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

		session_page = SessionManagementPage(page.pw_page)
		assert session_page.verify_session_management_page_opened(), (
			"Session management page did not load after administrator login."
		)
		return session_page

	@pytest.mark.usefixtures("before_after_test")
	def test_open_session_management_tab(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), (
			"Session management tab did not open with required controls and table columns."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_admission_date_column_sorted_ascending_on_first_click(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), (
			"Session management tab did not open with required controls and table columns."
		)
		assert session_page.verify_session_column_sorted_ascending("Admission Date"), (
			"Expected table to be sorted ascending by Admission Date after first click."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_admission_date_column_sorted_descending_on_second_click(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), (
			"Session management tab did not open with required controls and table columns."
		)
		assert session_page.verify_session_column_sorted_descending("Admission Date"), (
			"Expected table to be sorted descending by Admission Date after second click."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_all_session_table_columns_sorted_ascending_then_descending(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), (
			"Session management tab did not open with required controls and table columns."
		)
		assert session_page.verify_session_columns_sorted_ascending_then_descending(self.SORTABLE_COLUMNS), (
			"Expected all session table columns to sort ascending on first click and descending on second click."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_search_by_existing_device_id(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		device_id = session_page.get_first_session_row_field_value("Device ID")
		assert device_id, "Could not read an existing Device ID from session table."
		assert session_page.verify_search_filters_results(device_id), (
			"Expected table search to filter by entered Device ID."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_search_by_existing_patient_id_with_case_and_numbers(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		patient_id = session_page.get_first_session_row_field_value("Patient ID")
		assert patient_id, "Could not read an existing Patient ID from session table."

		variant = "".join(ch.swapcase() if ch.isalpha() else ch for ch in patient_id)
		if not variant:
			variant = patient_id

		assert session_page.verify_search_filters_results(variant), (
			"Expected table search to filter by entered Patient ID with mixed case/numbers."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_search_by_full_first_and_last_name(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		full_name = session_page.get_first_session_row_field_value("Full Name")
		assert full_name, "Could not read an existing Full Name from session table."

		name_parts = [part for part in full_name.split() if part.strip()]
		queries = [full_name]
		if len(name_parts) >= 1:
			queries.append(name_parts[0])
		if len(name_parts) >= 2:
			queries.append(name_parts[-1])

		for query in queries:
			assert session_page.verify_search_filters_results(query), (
				f"Expected table search to filter by entered name query '{query}'."
			)

	@pytest.mark.usefixtures("before_after_test")
	def test_filter_by_status_dropdown_shows_expected_options(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		expected_options = ["Pending", "Active", "Complete & Complete Limited"]
		assert session_page.verify_filter_by_status_options_visible(expected_options), (
			"Expected Pending, Active and Complete & Complete Limited options in Filter by status dropdown."
		)

	@pytest.mark.usefixtures("before_after_test")
	@pytest.mark.parametrize("status_value", ["Pending", "Active", "Complete and limited"])
	def test_filter_by_each_status_option(self, status_value: str):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		assert session_page.apply_filter_by_status(status_value), (
			f"Could not apply Filter by status option '{status_value}'."
		)
		assert session_page.verify_only_rows_with_status_visible(status_value), (
			f"Expected only patients with status '{status_value}' after filtering."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_show_hide_columns_dropdown_without_device_id_option(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		assert session_page.verify_show_hide_columns_dropdown_without_device_id(), (
			"Expected Show/Hide Columns dropdown list without Device ID option."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_show_hide_columns_select_session_initiator_and_verify_columns(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		dropdown_options = session_page.get_show_hide_columns_options()
		assert len(dropdown_options) >= 1, (
			"Expected Show/Hide Columns dropdown to open with selectable options."
		)
		assert any("session initiator" in option.lower() for option in dropdown_options), (
			"Expected 'Session Initiator' option in Show/Hide Columns dropdown."
		)

		assert session_page.select_session_initiator_column_and_verify_added(), (
			"Could not select 'Session Initiator' in Show/Hide Columns dropdown."
		)
		assert session_page.verify_session_initiator_column_added(), (
			"Expected Session Initiator column header to be visible in the table after selection."
		)
		assert session_page.verify_expected_visible_columns(["Session Initiator", "Patient ID"]), (
			"Expected Session Initiator and Patient ID columns to be displayed in the table."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_show_hide_columns_uncheck_status_hides_status_column(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		assert session_page.open_show_hide_columns_dropdown(), (
			"Could not open Show/Hide Columns dropdown."
		)
		assert session_page.mark_columns_in_show_hide_dropdown(["Status"]), (
			"Could not uncheck 'Status' in Show/Hide Columns dropdown."
		)
		assert not session_page.verify_session_column_visible_by_name("Status"), (
			"Expected 'Status' column not to be displayed in the table after unchecking it."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_pagination_options_work_for_visible_patients(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		assert session_page.verify_pagination_options_work(), (
			"Expected pagination options to be visible and usable for current patient list."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_search_field_tooltip_text(self):
		session_page = self._login_to_session_management()
		assert session_page.verify_required_controls_opened(), "Session management screen did not load."

		expected_tooltip = "Search by Patient ID, Name, Device ID, or Session Initiator"
		assert session_page.verify_search_field_tooltip_text(expected_tooltip), (
			"Expected tooltip text for search field was not displayed."
		)
