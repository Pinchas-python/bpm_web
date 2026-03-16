from infra.page_base import PageBase
from playwright.sync_api import  expect



class LogInOnline(PageBase):

    USERNAME_INPUT = "input[placeholder='Email']"
    LOGIN_BUTTON = "button[type='submit']"
    SUCCESS_MESSAGE = ".success-message, [class*='success']"
    LOGOUT_BUTTON = "button:has-text('Logout'), button:has-text('Sign out')"
    FORGOT_PASSWORD_LINK = "button:has-text('Forgot your password?')"
    USERNAME_LABEL = "label:has-text('Username')"
    PASSWORD_LABEL = "label:has-text('Password')"
    EMAIL_INPUT = "input[type='email'], input[name='email'], input[placeholder='Email']"
    PASSWORD_INPUT = "input[type='password'], input[name='password'], input[placeholder='Password']"
    FORGOT_PASSWORD = "button:has-text('Forgot your password?')"

    def __init__(self, page):
        super().__init__(page)
    
    
    
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