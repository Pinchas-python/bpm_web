from infra.page_base import PageBase



class LogInOnline(PageBase):

    USERNAME_INPUTS = [
        "input[placeholder='Email']",
        "input[placeholder*='Email']",
        "input[type='email']",
        "input[name='email']",
        "input[id*='email' i]",
    ]
    PASSWORD_INPUTS = [
        "input[placeholder='Password']",
        "input[placeholder*='Password']",
        "input[type='password']",
        "input[name='password']",
        "input[id*='password' i]",
    ]
    LOGIN_BUTTONS = [
        "button[type='submit']",
        "button:has-text('Sign in')",
        "button:has-text('Login')",
        "button:has-text('Log in')",
    ]
    ERROR_MESSAGE = "[role='alert'], .amplify-alert, .error, [class*='error'], [class*='alert']"
    SUCCESS_MESSAGE = ".success-message, [class*='success']"
    LOGOUT_BUTTON = "button:has-text('Logout'), button:has-text('Sign out')"
    FORGOT_PASSWORD_LINK = "button:has-text('Forgot your password?')"
    USERNAME_LABEL = "label:has-text('Username')"
    PASSWORD_LABEL = "label:has-text('Password')"


    def __init__(self, page):
        super().__init__(page)

    def _first_visible_selector(self, selectors, timeout_ms=5000):
        for selector in selectors:
            try:
                self.pw_page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
                return selector
            except Exception:
                continue
        return None

    def wait_for_login_form(self):
        selector = self._first_visible_selector(self.USERNAME_INPUTS, timeout_ms=20000)
        if not selector:
            raise TimeoutError(f"Login form not visible. Current URL: {self.pw_page.url}")
    
    def navigate_to_login(self, base_url: str):
        """Navigate to login page"""
        try:
            self.navigate_to(base_url)
            # Wait for page to be ready
            self.pw_page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            print(f"Navigation warning: {e}")
            # Try to continue anyway
            pass
    
    def enter_username(self, username: str):
        """Enter username in the username field"""
        self.pw_page.wait_for_load_state("domcontentloaded")
        selector = self._first_visible_selector(self.USERNAME_INPUTS)
        if not selector:
            raise TimeoutError(f"Username input not found. Current URL: {self.pw_page.url}")
        self.pw_page.fill(selector, username)
    
    def enter_password(self, password: str):
        """Enter password in the password field"""
        selector = self._first_visible_selector(self.PASSWORD_INPUTS)
        if not selector:
            raise TimeoutError(f"Password input not found. Current URL: {self.pw_page.url}")
        self.pw_page.fill(selector, password)

    def login(self, username: str, password: str):
        """Complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def click_login_button(self):
        """Click the login button"""
        selector = self._first_visible_selector(self.LOGIN_BUTTONS)
        if not selector:
            raise TimeoutError(f"Login button not found. Current URL: {self.pw_page.url}")
        self.pw_page.click(selector)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        self.wait_for_selector(self.ERROR_MESSAGE, timeout=5000)
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is visible"""
        try:
            # Wait for error to appear with multiple selectors
            self.pw_page.wait_for_selector(
                ".Mui-error, [role='alert'], .error, [class*='error']",
                timeout=3000,
                state="visible"
            )
            return True
        except:
            # If timeout, check if any error elements exist
            try:
                error_elements = self.pw_page.locator(".Mui-error, [role='alert'], .error, [class*='error']")
                return error_elements.count() > 0
            except:
                return False
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in (logout button is visible)"""
        try:
            return self.is_visible(self.LOGOUT_BUTTON)
        except:
            return False