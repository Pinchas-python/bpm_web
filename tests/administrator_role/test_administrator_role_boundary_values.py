import os
import time
import pytest

from infra.config.config_provider import configuration
from logic.pages.login_page import LogInOnline
from logic.pages.patient_admission_page import PatientAdmissionPage
from logic.pages.session_management_page import SessionManagementPage
from tests.test_base_online import TestBaseOnline


ADMIN_EMAIL = os.getenv("ADMIN_METRIC_EMAIL", "pinimari1@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_METRIC_PASSWORD", "Pm1234567!")


class TestAdministratorRoleBoundaryValues(TestBaseOnline):

	def _login_and_open_patient_admission(self):
		page: LogInOnline = self.browser_online.navigate(configuration["online_url_stage"], LogInOnline)
		assert page.verify_login_page_opened(), "Login page did not load for administrator scenario."

		page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

		session_page = SessionManagementPage(page.pw_page)
		assert session_page.verify_session_management_page_opened(), (
			"Session management page did not load after administrator login."
		)
		assert session_page.verify_session_grid_opened(), (
			"Session grid controls or columns are not visible on session management page."
		)

		patient_admission_page: PatientAdmissionPage = session_page.open_patient_admission()
		assert patient_admission_page.verify_opened(), (
			"Patient admission form did not open with required fields and confirm action. "
			f"Details: {patient_admission_page.get_last_open_failure()}"
		)
		return patient_admission_page

	def _unique_numeric(self, length: int):
		seed = str(int(time.time() * 1000))
		return seed[-length:].zfill(length)

	def _fill_required_valid_values(self, admission: PatientAdmissionPage, patient_id: str, device_id: str):
		admission.fill_patient_id(patient_id)
		admission.fill_device_id(device_id)
		admission.select_gender_male()
		admission.select_weight_unit_kg()
		admission.select_height_unit_cm()
		admission.fill_weight("80")
		admission.fill_height_cm("178")
		admission.select_first_referring_physician()

	def _assert_confirmation_popup_opens(self, admission: PatientAdmissionPage):
		admission.click_confirm()
		popup_header = admission.pw_page.get_by_text(
			"Please confirm the patient ID to complete the admission process", exact=False
		).first
		popup_header.wait_for(state="visible", timeout=10000)

		cancel_button = admission.pw_page.get_by_role("button", name="Cancel", exact=False).first
		cancel_button.click()

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_patient_id_30_characters_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = "A" * 30
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		self._assert_confirmation_popup_opens(admission)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_device_id_8_digits_with_000_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = "12000034"

		self._fill_required_valid_values(admission, patient_id, device_id)
		self._assert_confirmation_popup_opens(admission)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_first_name_1_character_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		admission.fill_first_name("A")
		self._assert_confirmation_popup_opens(admission)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_first_name_30_characters_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		admission.fill_first_name("A" * 30)
		self._assert_confirmation_popup_opens(admission)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_last_name_1_character_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		admission.fill_last_name("L")
		self._assert_confirmation_popup_opens(admission)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_last_name_30_characters_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		admission.fill_last_name("L" * 30)
		self._assert_confirmation_popup_opens(admission)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_dob_year_1904_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		admission.pw_page.locator(admission.DOB_INPUT).first.fill("01/01/1904")
		admission.click_confirm()
		assert admission.verify_error_message("Patient age is out of range"), (
			"Expected DOB year 1904 to show 'Patient age is out of range' validation."
		)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_weight_250_kg_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		admission.pw_page.get_by_role("radio", name="kg", exact=False).first.check()
		admission.fill_weight("250")
		self._assert_confirmation_popup_opens(admission)

	@pytest.mark.usefixtures("before_after_test")
	def test_patient_admission_height_242_cm_boundary(self):
		admission = self._login_and_open_patient_admission()
		patient_id = self._unique_numeric(8)
		device_id = self._unique_numeric(8)

		self._fill_required_valid_values(admission, patient_id, device_id)
		admission.pw_page.get_by_role("radio", name="cm", exact=False).first.check()
		admission.fill_height_cm("242")
		self._assert_confirmation_popup_opens(admission)
