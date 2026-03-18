"""
Pytest configuration and fixtures for Appium Android tests
"""
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import APPIUM_SERVER, ANDROID_CONFIG
import subprocess


def get_device_info():
    """Get connected Android device info via adb"""
    result = subprocess.run(
        ["adb", "shell", "getprop", "ro.build.version.release"],
        capture_output=True,
        text=True
    )
    platform_version = result.stdout.strip()
    
    result = subprocess.run(
        ["adb", "devices", "-l"],
        capture_output=True,
        text=True
    )
    for line in result.stdout.splitlines():
        if "device" in line and "List" not in line:
            device_id = line.split()[0]
            break
    else:
        device_id = "Android Device"
    
    return platform_version, device_id


@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to create and teardown Appium driver
    """
    platform_version, device_name = get_device_info()
    
    # Update config with actual device info
    capabilities = ANDROID_CONFIG.copy()
    capabilities["platformVersion"] = platform_version
    capabilities["deviceName"] = device_name
    
    # Create Appium options
    options = UiAutomator2Options()
    for key, value in capabilities.items():
        setattr(options, key, value)
    
    # Initialize driver
    drv = webdriver.Remote(APPIUM_SERVER, options=options)
    drv.implicitly_wait(10)
    
    yield drv
    
    # Teardown
    drv.quit()
