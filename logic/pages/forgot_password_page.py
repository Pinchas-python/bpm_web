from infra.page_base import PageBase


class ForgotPasswordPage(PageBase):
    EMAIL_INPUT = "input[type='email'], input[name='email'], input[placeholder='Email *']"
    BACK_TO_LOGIN = "//button[text()='Back to Login']"
    REQUEST_CODE = "//button[text()='Request Code']"
    VERIFICATION_CODE_INPUT = (
        "input[name*='Verification Code *'], input[placeholder*='Verification'], input[placeholder*='code']"
    )
    NEW_PASSWORD_INPUT = "input[placeholder='New Password']"
    CONFIRM_PASSWORD_INPUT = "input[placeholder='Confirm New Password']"
    CHANGE_PASSWORD_BUTTON = "//button[text()='Reset Password']"

    def verify_forgot_password_page_opened(self):
        try:
            self.pw_page.locator(self.EMAIL_INPUT).first.wait_for(state="visible", timeout=10000)
            self.pw_page.locator(self.BACK_TO_LOGIN).first.wait_for(state="visible", timeout=10000)
            self.pw_page.locator(self.REQUEST_CODE).first.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def enter_email(self, email: str):
        self.pw_page.locator(self.EMAIL_INPUT).first.fill(email)

    def click_request_code(self):
        self.pw_page.locator(self.REQUEST_CODE).first.click()

    def click_back_to_login(self):
        self.pw_page.locator(self.BACK_TO_LOGIN).first.click()

    def request_code(self, email: str):
        self.enter_email(email)
        self.click_request_code()

    def verify_verification_screen_opened(self):
        try:
            self.pw_page.locator(self.VERIFICATION_CODE_INPUT).first.wait_for(state="visible", timeout=15000)
            self.pw_page.locator(self.NEW_PASSWORD_INPUT).first.wait_for(state="visible", timeout=15000)
            self.pw_page.locator(self.CONFIRM_PASSWORD_INPUT).first.wait_for(state="visible", timeout=15000)
            self.pw_page.locator(self.CHANGE_PASSWORD_BUTTON).first.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False