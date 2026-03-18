"""
Login tests for Android app - mSalePro
"""
import pytest
from pages.login_page import LoginPage
from config import TEST_CREDENTIALS
from appium.webdriver.common.appiumby import AppiumBy


class TestLogin:
    """Test cases for login functionality"""
    
    def test_login_with_valid_credentials(self, driver):
        """
        Test Case: TC001 - Login with valid credentials
        Expected: Login successfully and navigate to home/main screen
        """
        login_page = LoginPage(driver)
        login_page.login(
            TEST_CREDENTIALS["valid_username"],
            TEST_CREDENTIALS["valid_password"]
        )
        
        # Wait for home screen to appear (adjust timeout as needed)
        driver.implicitly_wait(10)
        
        # TODO: Update with actual home screen element
        # Common patterns:
        # - Menu button
        # - Dashboard element  
        # - User profile icon
        # Example assertion (update with your actual home screen element):
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        # wait = WebDriverWait(driver, 10)
        # home_element = wait.until(EC.presence_of_element_located(
        #     (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Home")')
        # ))
        # assert home_element.is_displayed()
    
    def test_login_with_invalid_credentials(self, driver):
        """
        Test Case: TC002 - Login with invalid credentials
        Expected: Error message displayed, user stays on login screen
        """
        login_page = LoginPage(driver)
        login_page.login(
            TEST_CREDENTIALS["invalid_username"],
            TEST_CREDENTIALS["invalid_password"]
        )
        
        # Check for error message
        # Common error messages: "Invalid credentials", "Sai tên đăng nhập/mật khẩu"
        error_msg = login_page.get_error_message()
        
        # TODO: Update assertion based on actual error message
        # assert error_msg is not None
        # assert any(text in error_msg.lower() for text in ["invalid", "sai", "error", "incorrect"])
    
    def test_login_with_empty_username(self, driver):
        """
        Test Case: TC003 - Login with empty username
        Expected: Validation error for username field
        """
        login_page = LoginPage(driver)
        login_page.enter_password(TEST_CREDENTIALS["valid_password"])
        login_page.click_login_button()
        
        # TODO: Add assertion to verify validation error
        # Common validation messages: "Username is required", "Vui lòng nhập tên đăng nhập"
    
    def test_login_with_empty_password(self, driver):
        """
        Test Case: TC004 - Login with empty password
        Expected: Validation error for password field
        """
        login_page = LoginPage(driver)
        login_page.enter_username(TEST_CREDENTIALS["valid_username"])
        login_page.click_login_button()
        
        # TODO: Add assertion to verify validation error
        # Common validation messages: "Password is required", "Vui lòng nhập mật khẩu"
    
    def test_forgot_password_link(self, driver):
        """
        Test Case: TC005 - Click forgot password link
        Expected: Navigate to password recovery screen
        """
        login_page = LoginPage(driver)
        login_page.click_forgot_password()
        
        # TODO: Add assertion to verify password recovery screen
        # assert driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
        #                            'new UiSelector().text("Quên mật khẩu")').is_displayed()
