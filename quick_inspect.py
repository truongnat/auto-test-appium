"""
Simple script để inspect app - tìm login elements
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
from config import APPIUM_SERVER, ANDROID_CONFIG

def inspect_login_screen():
    options = UiAutomator2Options()
    for key, value in ANDROID_CONFIG.items():
        setattr(options, key, value)
    
    print("📱 Connecting to Appium...")
    driver = webdriver.Remote(APPIUM_SERVER, options=options)
    driver.implicitly_wait(5)
    
    try:
        time.sleep(3)
        print(f"✓ Connected to: {driver.current_package}/{driver.current_activity}")
        
        # Get page source
        print("\n📄 Getting page source...")
        page_source = driver.page_source
        with open('login_page_source.xml', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"✓ Saved to: login_page_source.xml")
        
        # Find elements by class
        from appium.webdriver.common.appiumby import AppiumBy
        
        print("\n" + "="*60)
        print("LOGIN SCREEN ELEMENTS")
        print("="*60)
        
        # All EditTexts
        print("\n📝 EditText fields:")
        for i, el in enumerate(driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText"), 1):
            rid = el.get_attribute('resource-id')
            desc = el.get_attribute('content-desc')
            txt = el.get_attribute('text')
            print(f"  {i}. resource-id: {rid}")
            print(f"     content-desc: {desc}")
            print(f"     text: {txt}")
        
        # All Buttons
        print("\n🔘 Buttons:")
        for i, el in enumerate(driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button"), 1):
            rid = el.get_attribute('resource-id')
            desc = el.get_attribute('content-desc')
            txt = el.get_attribute('text')
            print(f"  {i}. resource-id: {rid}")
            print(f"     content-desc: {desc}")
            print(f"     text: {txt}")
        
        # All TextViews
        print("\n📄 TextViews:")
        for i, el in enumerate(driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"), 1):
            rid = el.get_attribute('resource-id')
            desc = el.get_attribute('content-desc')
            txt = el.get_attribute('text')
            if txt and txt.strip():
                print(f"  {i}. [{txt}]")
                print(f"     resource-id: {rid}")
        
        # Clickable elements
        print("\n🖱️ Clickable elements:")
        clickable = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 
                                         'new UiSelector().clickable(true)')
        for i, el in enumerate(clickable[:15], 1):
            cls = el.get_attribute('className')
            rid = el.get_attribute('resource-id')
            txt = el.get_attribute('text')
            print(f"  {i}. {cls.split('.')[-1]} - {rid}")
            if txt:
                print(f"     text: {txt}")
        
        print("\n" + "="*60)
        print("SUGGESTED LOCATORS for LoginPage:")
        print("="*60)
        print("""
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage:
    # Replace with actual IDs from above
    USERNAME_INPUT = (AppiumBy.ID, "com.mobifone.msaleplus:id/YOUR_USERNAME_ID")
    PASSWORD_INPUT = (AppiumBy.ID, "com.mobifone.msaleplus:id/YOUR_PASSWORD_ID")
    LOGIN_BUTTON = (AppiumBy.ID, "com.mobifone.msaleplus:id/YOUR_LOGIN_BUTTON_ID")
""")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("\nClosing in 3 seconds...")
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    inspect_login_screen()
