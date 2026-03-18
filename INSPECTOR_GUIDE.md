# Hướng dẫn sử dụng Appium Inspector

## Cách 1: Dùng Appium Inspector GUI (Khuyến nghị)

### Bước 1: Mở Appium Inspector

Sau khi cài đặt xong, chạy lệnh:
```bash
appium-inspector
```

Hoặc tìm "Appium Inspector" trong Applications.

### Bước 2: Cấu hình Desired Capabilities

Trong Appium Inspector, nhập các thông tin sau:

| Key | Value |
|-----|-------|
| platformName | Android |
| appPackage | com.mobifone.msaleplus |
| appActivity | .MainActivity |
| automationName | UiAutomator2 |
| deviceName | Android Device |
| noReset | true |
| autoGrantPermissions | true |

**Server URL:** `http://127.0.0.1:4723`

### Bước 3: Start Session

1. Click **Start Session**
2. Appium Inspector sẽ kết nối và hiển thị giao diện app của bạn

### Bước 4: Tìm Locators

1. **Di chuột** vào element bạn muốn tìm (ví dụ: username field)
2. **Thông tin element** sẽ hiện ở bên phải:
   - `resource-id`: ID của element (tốt nhất)
   - `content-desc`: Accessibility ID
   - `class`: Class type (android.widget.EditText, etc.)
   - `text`: Text hiển thị

3. **Chọn locator strategy**:

#### Priority 1: Accessibility ID (Tốt nhất)
```python
(AppiumBy.ACCESSIBILITY_ID, "username")
```
Dùng khi element có `content-desc`

#### Priority 2: Android ID
```python
(AppiumBy.ID, "com.mobifone.msaleplus:id/et_username")
```
Dùng khi element có `resource-id`

#### Priority 3: Android UiAutomator
```python
(AppiumBy.ANDROID_UIAUTOMATOR, 
 'new UiSelector().resourceId("com.mobifone.msaleplus:id/et_username")')
```

#### Priority 4: XPath (Cuối cùng)
```python
(AppiumBy.XPATH, "//android.widget.EditText[@text='Username']")
```

### Bước 5: Copy Locator

Click vào element → Copy locator → Paste vào `pages/login_page.py`

---

## Cách 2: Dùng ADB để tìm Resource ID

### Tìm resource-id của elements

```bash
# Bật chế độ hiển thị UI
adb shell settings put global show_touches on

# Xem layout hierarchy
adb shell uiautomator dump
adb pull /sdcard/window_dump.xml

# Hoặc dùng lệnh này để xem chi tiết
adb shell uiautomator events
```

### Mở file window_dump.xml
File XML sẽ chứa toàn bộ UI hierarchy với resource-id của từng element.

---

## Ví dụ thực tế cho mSalePlus

### 1. Start Appium Server
```bash
appium
```

### 2. Chạy script test đơn giản để inspect

Tạo file `inspect_app.py`:
```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Device",
    "appPackage": "com.mobifone.msaleplus",
    "appActivity": ".MainActivity",
    "noReset": True,
    "autoGrantPermissions": True,
}

options = UiAutomator2Options()
for k, v in caps.items():
    setattr(options, k, v)

driver = webdriver.Remote("http://localhost:4723", options=options)

# In ra toàn bộ page source
print(driver.page_source)

# Tìm tất cả EditText elements
from appium.webdriver.common.appiumby import AppiumBy
elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
print(f"\nFound {len(elements)} EditText elements:")
for i, el in enumerate(elements):
    print(f"{i+1}. ID: {el.get_attribute('resource-id')}")
    print(f"   Text: {el.text}")
    print(f"   Content-Desc: {el.get_attribute('content-desc')}")

time.sleep(30)  # Giữ session trong 30s để inspect
driver.quit()
```

Chạy:
```bash
python inspect_app.py
```

---

## Mẹo tìm Locators

### 1. Ưu tiên theo thứ tự:
1. **Accessibility ID** (`content-desc`) - Nhanh và ổn định nhất
2. **Android ID** (`resource-id`) - Tốt, ổn định
3. **Android UiAutomator** - Linh hoạt
4. **XPath** - Chậm, dễ gãy

### 2. Pattern thường gặp:

| Element Type | Locator Pattern |
|-------------|-----------------|
| EditText (input) | `com.package:id/et_username` |
| Button | `com.package:id/btn_login` |
| TextView | `com.package:id/tv_error` |
| ImageView | `com.package:id/iv_logo` |

### 3. Dùng text để tìm (nếu không có ID):
```python
(AppiumBy.ANDROID_UIAUTOMATOR, 
 'new UiSelector().text("Login")')
```

### 4. Dùng class name + index:
```python
# Tìm EditText đầu tiên
elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
username_field = elements[0]
password_field = elements[1]
```

---

## Sau khi tìm được locators

Cập nhật vào `pages/login_page.py`:

```python
class LoginPage:
    # Thay thế bằng locators thực tế
    USERNAME_INPUT = (AppiumBy.ID, "com.mobifone.msaleplus:id/et_username")
    PASSWORD_INPUT = (AppiumBy.ID, "com.mobifone.msaleplus:id/et_password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.mobifone.msaleplus:id/btn_login")
    ERROR_MESSAGE = (AppiumBy.ID, "com.mobifone.msaleplus:id/tv_error")
```

---

## Troubleshooting

### Appium Inspector không kết nối được
1. Kiểm tra Appium server đang chạy: `appium`
2. Kiểm tra device kết nối: `adb devices`
3. Restart Appium server

### Không tìm thấy element
1. Chờ element load: dùng `WebDriverWait`
2. Kiểm tra lại app package/activity
3. Scroll để tìm element (nếu ở ngoài viewport)

### Element bị che khuất
```python
# Scroll tới element
driver.execute_script("arguments[0].scrollIntoView()", element)
```
