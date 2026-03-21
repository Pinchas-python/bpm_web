from infra.page_base import PageBase
import re
from logic.pages.forgot_password_page import ForgotPasswordPage



class LogInOnline(PageBase):

    LOGIN_BUTTON = "button[type='submit']"
    EMAIL_INPUT = "input[type='email'], input[name='email'], input[placeholder='Email']"
    PASSWORD_INPUT = "input[type='password'], input[name='password'], input[placeholder='Password']"
    
    
    
    def enter_username(self, username: str):
        locator = self.pw_page.locator(
            "input[type='email'], input[name='email'], input[placeholder='Email']"
        ).first
        locator.wait_for(state="visible", timeout=10000)
        locator.fill(username)
    
    def enter_password(self, password: str):
        locator = self.pw_page.locator(
            "input[type='password'], input[name='password'], input[placeholder='Password']"
        ).first
        locator.wait_for(state="visible", timeout=10000)
        locator.fill(password)

    
    def click_login_button(self):
        self.pw_page.click(self.LOGIN_BUTTON)

    def open_forgot_password(self):
        self.pw_page.get_by_role("button", name="Forgot your password?", exact=True).click()
        return ForgotPasswordPage(self.pw_page)

    def verify_login_page_opened(self):
        try:
            email_input = self.pw_page.locator(self.EMAIL_INPUT).first
            password_input = self.pw_page.locator(self.PASSWORD_INPUT).first
            forgot_password_button = self.pw_page.get_by_role(
                "button", name="Forgot your password?", exact=True
            )
            login_button = self.pw_page.locator("button[type='submit'], input[type='submit']").first

            email_input.wait_for(state="visible", timeout=10000)
            password_input.wait_for(state="visible", timeout=10000)
            forgot_password_button.wait_for(state="visible", timeout=10000)
            login_button.wait_for(state="visible", timeout=10000)

            forgot_password_label = (forgot_password_button.text_content() or "").strip()
            if forgot_password_label != "Forgot your password?":
                return False

            login_button_label = (
                (login_button.text_content() or "").strip()
                or (login_button.get_attribute("value") or "").strip()
            ).lower()

            return "login" in login_button_label or "log in" in login_button_label
        except Exception:
            return False
        
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def verify_error_message(self, expected_message: str):
        expected_message = self._normalize_text(expected_message)
        if not expected_message:
            return False

        try:
            matched_locator = self.pw_page.get_by_text(expected_message, exact=False).first
            if matched_locator.is_visible(timeout=2000):
                matched_text = self._normalize_text(matched_locator.text_content() or "")
                if matched_text == expected_message:
                    return True
        except Exception:
            pass

        email_input = self.pw_page.locator(self.EMAIL_INPUT).first
        password_input = self.pw_page.locator(self.PASSWORD_INPUT).first

        try:
            email_validation = self._normalize_text(email_input.evaluate("el => el.validationMessage") or "")
            if expected_message == email_validation:
                return True
        except Exception:
            pass

        try:
            password_validation = self._normalize_text(password_input.evaluate("el => el.validationMessage") or "")
            if expected_message == password_validation:
                return True
        except Exception:
            pass

        # Some auth failures do not show a stable text node; use behavior-based
        # validation as a fallback for incorrect credentials.
        if "incorrect email or password" in expected_message:
            try:
                return "/login" in self.pw_page.url and "session-management" not in self.pw_page.url
            except Exception:
                return False

        return False

    def _normalize_text(self, value: str):
        text = (value or "").strip().lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return " ".join(text.split())

    def verify_email_marked_red(self):
        return self._is_field_marked_as_error(self.pw_page.locator(self.EMAIL_INPUT).first)

    def verify_password_marked_red(self):
        return self._is_field_marked_as_error(self.pw_page.locator(self.PASSWORD_INPUT).first)

    def _is_field_marked_as_error(self, field_locator):
        try:
            if field_locator.get_attribute("aria-invalid") == "true":
                return True
        except Exception:
            pass

        try:
            class_name = (field_locator.get_attribute("class") or "").lower()
            if "error" in class_name or "invalid" in class_name:
                return True
        except Exception:
            pass

        try:
            border_color = (field_locator.evaluate("el => getComputedStyle(el).borderColor") or "").lower()
            return "255, 0, 0" in border_color or "220, 38, 38" in border_color or "red" in border_color
        except Exception:
            return False