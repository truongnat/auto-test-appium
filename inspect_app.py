"""
Script để inspect app và tìm locators
Chạy script này để xem page source và tìm elements
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
from config import APPIUM_SERVER, ANDROID_CONFIG

def inspect_app():
    # Initialize driver
    options = UiAutomator2Options()
    for key, value in ANDROID_CONFIG.items():
        setattr(options, key, value)
    
    print("Connecting to Appium server...")
    driver = webdriver.Remote(APPIUM_SERVER, options=options)
    
    try:
        # Wait for app to load
        time.sleep(5)
        
        # Ensure we're in the correct app
        print(f"Current app package: {driver.current_package}")
        print(f"Current app activity: {driver.current_activity}")
        
        print("\n" + "="*60)
        print("APP PAGE SOURCE (XML)")
        print("="*60)
        page_source = driver.page_source
        print(page_source[:5000])  # Print first 5000 chars
        if len(page_source) > 5000:
            print(f"\n... (total {len(page_source)} characters)")
        
        # Save full page source to file
        with open('page_source.xml', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"\n✓ Full page source saved to: page_source.xml")
        
        # Find all interactive elements
        from appium.webdriver.common.appiumby import AppiumBy
        
        print("\n" + "="*60)
        print("INTERACTIVE ELEMENTS")
        print("="*60)
        
        # Find EditTexts (input fields)
        print("\n📝 EditText (Input Fields):")
        try:
            elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            for i, el in enumerate(elements, 1):
                res_id = el.get_attribute('resource-id') or 'N/A'
                content_desc = el.get_attribute('content-desc') or 'N/A'
                text = el.text or el.get_attribute('text') or 'N/A'
                print(f"  {i}. ID: {res_id}")
                print(f"     Content-Desc: {content_desc}")
                print(f"     Text: {text}")
                print()
        except Exception as e:
            print(f"  No EditText found: {e}")
        if not elements:
            print("  (none found)")
        
        # Find Buttons
        print("\n🔘 Buttons (android.widget.Button):")
        elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
        for i, el in enumerate(elements, 1):
            res_id = el.get_attribute('resource-id') or 'N/A'
            content_desc = el.get_attribute('content-desc') or 'N/A'
            text = el.text or el.get_attribute('text') or 'N/A'
            print(f"  {i}. ID: {res_id}")
            print(f"     Content-Desc: {content_desc}")
            print(f"     Text: {text}")
            print()
        
        # Find TextViews (labels, messages)
        print("\n📄 TextViews (Labels/Messages):")
        elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        for i, el in enumerate(elements, 1):
            res_id = el.get_attribute('resource-id') or 'N/A'
            content_desc = el.get_attribute('content-desc') or 'N/A'
            text = el.text or el.get_attribute('text') or 'N/A'
            print(f"  {i}. ID: {res_id}")
            print(f"     Content-Desc: {content_desc}")
            print(f"     Text: {text}")
            print()
        
        # Find clickable elements
        print("\n🖱️ Clickable Elements:")
        elements = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 
                                        'new UiSelector().clickable(true)')
        for i, el in enumerate(elements[:10], 1):  # Limit to 10
            res_id = el.get_attribute('resource-id') or 'N/A'
            class_name = el.get_attribute('className')
            text = el.text or el.get_attribute('text') or 'N/A'
            print(f"  {i}. {class_name} - ID: {res_id} - Text: {text}")
        
        print("\n" + "="*60)
        print("HOW TO USE LOCATORS")
        print("="*60)
        print("""
Example for LoginPage locators:

from appium.webdriver.common.appiumby import AppiumBy

class LoginPage:
    # If you found resource-id:
    USERNAME_INPUT = (AppiumBy.ID, "com.mobifone.msaleplus:id/et_username")
    PASSWORD_INPUT = (AppiumBy.ID, "com.mobifone.msaleplus:id/et_password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.mobifone.msaleplus:id/btn_login")
    
    # If you found content-desc (accessibility-id):
    USERNAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "username")
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "login")
    
    # If no ID, use UiAutomator:
    USERNAME_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 
                      'new UiSelector().resourceId("com.mobifone.msaleplus:id/et_username")')
        """)
        
    finally:
        print("\nClosing session in 5 seconds...")
        time.sleep(5)
        driver.quit()
        print("Done!")

if __name__ == "__main__":
    print("="*60)
    print("APPIUM INSPECTOR SCRIPT")
    print("="*60)
    print("\nMake sure Appium server is running: appium")
    print("Make sure device is connected: adb devices\n")
    
    try:
        inspect_app()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Appium server is running (run: appium)")
        print("2. Make sure device is connected (run: adb devices)")
        print("3. Check app package name in config.py")
