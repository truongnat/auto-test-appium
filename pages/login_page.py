"""
Page Object for Login screen
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    Page Object for Login screen
    Define locators and actions for the login page
    
    App: mSalePro (com.mobifone.msaleplus)
    """
    
    # Locators using Android UI Automator (app doesn't have resource-ids)
    # Username field: EditText with placeholder "Tên đăng nhập"
    USERNAME_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").text("Tên đăng nhập")'
    )
    
    # Password field: EditText with placeholder "Mật khẩu"
    PASSWORD_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").text("Mật khẩu")'
    )
    
    # Login button: Find the TextView with text "Đăng nhập" (inside the Button)
    LOGIN_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Đăng nhập")'
    )
    
    # Alternative: Use XPath (slower but works)
    # USERNAME_INPUT = (AppiumBy.XPATH, '//android.widget.EditText[@text="Tên đăng nhập"]')
    # PASSWORD_INPUT = (AppiumBy.XPATH, '//android.widget.EditText[@text="Mật khẩu"]')
    # LOGIN_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@text="Đăng nhập"]')
    
    # Forgot password link: TextView with text "Quên mật khẩu?"
    FORGOT_PASSWORD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Quên mật khẩu?")'
    )
    
    # Fingerprint login
    FINGERPRINT_LOGIN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Đăng nhập bằng vân tay")'
    )
    
    # Error message locator (generic TextView)
    ERROR_MESSAGE = (AppiumBy.CLASS_NAME, "android.widget.TextView")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def enter_username(self, username):
        """Enter username into the username field"""
        element = self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        element.clear()
        element.send_keys(username)
        return self
    
    def enter_password(self, password):
        """Enter password into the password field"""
        element = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        element.clear()
        element.send_keys(password)
        return self
    
    def click_login_button(self):
        """Click the login button"""
        element = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        element.click()
        return self
    
    def get_error_message(self):
        """Get error message if login fails"""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
            return element.text
        except:
            return None
    
    def login(self, username, password):
        """
        Complete login action
        Returns self for method chaining
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def click_forgot_password(self):
        """Click forgot password link"""
        element = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD))
        element.click()
        return self
