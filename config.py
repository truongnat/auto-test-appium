"""
Appium configuration for Android testing
"""

APPIUM_SERVER = "http://localhost:4723"

ANDROID_CONFIG = {
    "platformName": "Android",
    "platformVersion": "",  # Will be auto-detected
    "deviceName": "",  # Will be auto-detected
    "appPackage": "com.mobifone.msaleplus",
    "appActivity": ".MainActivity",
    "appWaitActivity": ".MainActivity,.*LoginActivity,.*SplashActivity",  # Wait for any of these
    "automationName": "UiAutomator2",
    "noReset": True,  # Don't reset app state between sessions
    "fullReset": False,
    "autoGrantPermissions": True,
    "newCommandTimeout": 300,
    "skipUnlock": True,  # Skip screen unlock for stability
    "disableWindowAnimation": True,  # Faster, more stable tests
    "adbExecTimeout": 60000,  # Increase ADB timeout
    "uiautomator2ServerInstallTimeout": 20000,
    "ignoreUnimportantViews": True,  # Improve performance
    "allowInvisibleElements": True,  # Allow finding invisible elements
}

# Test credentials - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
TEST_CREDENTIALS = {
    "valid_username": "duyen_test@cntt",  # Replace with actual username
    "valid_password": "1123",  # Replace with actual password
    "invalid_username": "wrong_user",
    "invalid_password": "wrong_password",
}
