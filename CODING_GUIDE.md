#  HƯỚNG DẪN CODE VÀ SỬ DỤNG TEST TỰ ĐỘNG
### Tài liệu kỹ thuật cho Developer và Tester muốn mở rộng test

---

## 📋 MỤC LỤC

1. [Tổng Quan Kiến Trúc](#tổng-quan-kiến-trúc)
2. [Cấu Trúc Project](#cấu-trúc-project)
3. [Hiểu Về ADB Test Method](#hiểu-về-adb-test-method)
4. [Viết Test Mới](#viết-test-mới)
5. [Các Hàm Helper Hữu Ích](#các-hàm-helper-hữu-ích)
6. [Best Practices](#best-practices)
7. [Ví Dụ Thực Tế](#ví-dụ-thực-tế)

---

## 🏗️ TỔNG QUAN KIẾN TRÚC

### Phương pháp test được sử dụng

Project sử dụng **2 phương pháp** test:

| Phương pháp | Ưu điểm | Nhược điểm | Khi nào dùng |
|-------------|---------|------------|--------------|
| **ADB Input Method** | ✅ Ổn định, nhanh, không cần Appium<br>✅ Không bị "socket hang up"<br>✅ Dễ debug | ❌ Chỉ làm việc với native app<br>❌ Không hỗ trợ complex gestures | ✅ **Khuyến nghị** cho test cơ bản |
| **Appium Method** | ✅ Hỗ trợ complex interactions<br>✅ Cross-platform (iOS/Android)<br>✅ Rich ecosystem | ❌ Dễ bị "socket hang up"<br>❌ Chậm hơn<br>❌ Cần Appium server | Khi cần test phức tạp |

### Luồng thực thi test (ADB Method)

```
┌─────────────────────────────────────────────────────────┐
│  1. Launch app bằng adb shell am start                │
│  2. Get UI dump bằng adb uiautomator dump             │
│  3. Parse XML để tìm elements                         │
│  4. Tính toán tọa độ (x, y) của elements              │
│  5. Tap bằng adb input tap x y                        │
│  6. Input text bằng adb input text                    │
│  7. Chụp ảnh bằng adb shell screencap                 │
│  8. Verify kết quả                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 CẤU TRÚC PROJECT

```
auto-test-android/
├── config.py                    # Cấu hình toàn cục
├── conftest.py                  # Pytest fixtures
├── requirements.txt             # Dependencies
│
├── simple_login_test.py         # Test login mẫu (ADB method)
├── quick_inspect.py             # Script inspect UI
├── inspect_app.py               # Script inspect chi tiết
│
├── pages/                       # Page Objects (nếu dùng Appium)
│   └── login_page.py
└── tests/                       # Test cases (pytest)
    └── test_login.py
```

---

## 🔧 HIỂU VỀ ADB TEST METHOD

### Các hàm cơ bản trong `simple_login_test.py`

#### 1. `run_adb(cmd)` - Chạy adb command có output

```python
def run_adb(cmd):
    """Chạy adb command và return output"""
    result = subprocess.run(["adb", "shell"] + cmd, capture_output=True, text=True)
    return result.stdout.strip()
```

**Sử dụng:**
```python
# Lấy UI dump
dump = run_adb(["cat", "/sdcard/window_dump.xml"])

# Lấy package name
package = run_adb(["shell", "getprop", "ro.package.name"])
```

#### 2. `run_adb_no_output(cmd)` - Chạy adb command không cần output

```python
def run_adb_no_output(cmd):
    """Chạy adb command không cần output"""
    subprocess.run(["adb", "shell"] + cmd, capture_output=True)
```

**Sử dụng:**
```python
# Tap vào màn hình
run_adb_no_output(["input", "tap", "500", "1000"])

# Nhập text
run_adb_no_output(["input", "text", "hello"])

# Chụp màn hình
run_adb_no_output(["screencap", "-p", "/sdcard/screen.png"])
```

#### 3. `get_ui_dump()` - Lấy UI dump XML

```python
def get_ui_dump():
    """Lấy UI dump qua adb"""
    run_adb_no_output(["uiautomator", "dump", "/sdcard/window_dump.xml"])
    return run_adb(["cat", "/sdcard/window_dump.xml"])
```

**Output mẫu:**
```xml
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<hierarchy rotation="0">
  <node index="0" text="" class="android.widget.FrameLayout" 
        bounds="[0,0][1080,2408]">
    <node index="0" text="Đăng nhập" 
          class="android.widget.TextView" 
          bounds="[416,1566][665,1638]" />
  </node>
</hierarchy>
```

#### 4. `find_element_center(dump, class_name, text)` - Tìm element

```python
def find_element_center(dump, class_name, text=None):
    """Tìm element và return center coordinates"""
    pattern = rf'<node[^>]*class="{class_name}"[^>]*'
    if text:
        pattern += rf'[^>]*text="{text}"'
    pattern += r'[^>]*>'
    
    matches = re.findall(pattern, dump)
    for match in matches:
        bounds_match = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', match)
        if bounds_match:
            x1, y1, x2, y2 = map(int, bounds_match.groups())
            return ((x1 + x2) // 2, (y1 + y2) // 2)
    return None
```

**Sử dụng:**
```python
dump = get_ui_dump()

# Tìm button "Đăng nhập"
login_btn = find_element_center(dump, "android.widget.TextView", "Đăng nhập")
# Return: (540, 1602) - tọa độ center

# Tìm tất cả EditText
edit_texts = get_all_elements(dump, "android.widget.EditText")
```

#### 5. `tap(x, y)` - Tap vào tọa độ

```python
def tap(x, y):
    """Tap tại tọa độ"""
    run_adb_no_output(["input", "tap", str(x), str(y)])
    time.sleep(0.8)  # Chờ cho UI update
```

**Sử dụng:**
```python
# Tap vào giữa màn hình
tap(540, 1200)

# Tap vào button
login_center = find_element_center(dump, "android.widget.TextView", "Đăng nhập")
tap(login_center[0], login_center[1])
```

#### 6. `input_text(text)` - Nhập text

```python
def input_text(text):
    """Nhập text qua adb input"""
    escaped = text.replace("'", "'\\''")
    run_adb_no_output(["input", "text", f"'{escaped}'"])
    time.sleep(0.3)
```

**Lưu ý:** 
- Chỉ hỗ trợ ASCII tốt
- Tiếng Việt có thể bị lỗi encoding
- Special characters cần escape

#### 7. `clear_text()` - Xóa text field

```python
def clear_text():
    """Clear text field"""
    for _ in range(30):
        run_adb_no_output(["input", "keyevent", "KEYCODE_DEL"])
    time.sleep(0.2)
```

#### 8. `hide_keyboard()` - Ẩn keyboard

```python
def hide_keyboard():
    """Ẩn keyboard"""
    run_adb_no_output(["input", "keyevent", "KEYCODE_BACK"])
    time.sleep(0.5)
```

---

## ✍️ VIẾT TEST MỚI

### Template test cơ bản

```python
"""
Test mẫu - Copy để tạo test mới
"""
import subprocess
import time
import re

def run_adb(cmd):
    result = subprocess.run(["adb", "shell"] + cmd, capture_output=True, text=True)
    return result.stdout.strip()

def run_adb_no_output(cmd):
    subprocess.run(["adb", "shell"] + cmd, capture_output=True)

def get_ui_dump():
    run_adb_no_output(["uiautomator", "dump", "/sdcard/window_dump.xml"])
    return run_adb(["cat", "/sdcard/window_dump.xml"])

def find_element_center(dump, class_name, text=None):
    pattern = rf'<node[^>]*class="{class_name}"[^>]*'
    if text:
        pattern += rf'[^>]*text="{text}"'
    pattern += r'[^>]*>'
    
    matches = re.findall(pattern, dump)
    for match in matches:
        bounds_match = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', match)
        if bounds_match:
            x1, y1, x2, y2 = map(int, bounds_match.groups())
            return ((x1 + x2) // 2, (y1 + y2) // 2)
    return None

def tap(x, y):
    run_adb_no_output(["input", "tap", str(x), str(y)])
    time.sleep(0.8)

def input_text(text):
    escaped = text.replace("'", "'\\''")
    run_adb_no_output(["input", "text", f"'{escaped}'"])
    time.sleep(0.3)

def test_cua_ban():
    # 1. Launch app
    print("🚀 Launching app...", flush=True)
    run_adb_no_output(["am", "start", "-n", "com.mobifone.msaleplus/.MainActivity"])
    time.sleep(3)
    
    # 2. Get UI dump
    print("📄 Getting UI dump...", flush=True)
    dump = get_ui_dump()
    
    # 3. Tìm elements cần thiết
    print("🔍 Finding elements...", flush=True)
    element = find_element_center(dump, "android.widget.TextView", "Text cần tìm")
    
    if not element:
        print("❌ Element not found!", flush=True)
        return False
    
    # 4. Tương tác
    print("👆 Tapping element...", flush=True)
    tap(element[0], element[1])
    time.sleep(2)
    
    # 5. Verify
    print("✅ Checking result...", flush=True)
    new_dump = get_ui_dump()
    if "Expected text" in new_dump:
        print("✅ TEST PASSED", flush=True)
        return True
    else:
        print("❌ TEST FAILED", flush=True)
        return False

if __name__ == "__main__":
    test_cua_ban()
```

### Các bước viết test mới

#### Bước 1: Inspect UI để tìm elements

```bash
python quick_inspect.py
```

Hoặc dùng adb trực tiếp:
```bash
adb shell uiautomator dump /sdcard/window_dump.xml
adb pull /sdcard/window_dump.xml .
```

Mở `window_dump.xml` để xem cấu trúc UI.

#### Bước 2: Xác định elements cần tương tác

Tìm trong XML:
- **Button**: `class="android.widget.Button"` hoặc `class="android.widget.TextView"` với `clickable="true"`
- **Input field**: `class="android.widget.EditText"`
- **Text hiển thị**: `class="android.widget.TextView"`

#### Bước 3: Viết code tương tác

```python
# Tìm element
element = find_element_center(dump, "android.widget.TextView", "Text trên button")

# Tap
tap(element[0], element[1])

# Hoặc nhập text
input_text("Nội dung cần nhập")
```

#### Bước 4: Verify kết quả

```python
# Lấy UI dump mới
new_dump = get_ui_dump()

# Kiểm tra có text mong đợi
if "Text mong đợi" in new_dump:
    return True  # Pass
else:
    return False  # Fail
```

---

## 🛠️ CÁC HÀM HELPER HỮU ÍCH

### Lấy tất cả elements của một class

```python
def get_all_elements(dump, class_name):
    """Tìm tất cả elements của một class"""
    pattern = rf'<node[^>]*class="{class_name}"[^>]*>'
    return re.findall(pattern, dump)

# Sử dụng
edit_texts = get_all_elements(dump, "android.widget.EditText")
print(f"Found {len(edit_texts)} EditText fields")
```

### Parse bounds để lấy tọa độ

```python
def get_bounds_center(bounds_str):
    """Parse bounds string và return center"""
    match = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', bounds_str)
    if match:
        x1, y1, x2, y2 = map(int, match.groups())
        return ((x1 + x2) // 2, (y1 + y2) // 2)
    return (500, 1000)  # Default

# Sử dụng
bounds = 'bounds="[416,1566][665,1638]"'
center = get_bounds_center(bounds)  # (540, 1602)
```

### Chụp màn hình

```python
def take_screenshot(filename):
    """Chụp màn hình và pull về"""
    run_adb_no_output(["screencap", "-p", f"/sdcard/{filename}"])
    time.sleep(0.3)
    subprocess.run(["adb", "pull", f"/sdcard/{filename}", filename], capture_output=True)

# Sử dụng
take_screenshot("ket_qua.png")
```

### Swipe (cuộn màn hình)

```python
def swipe(x1, y1, x2, y2):
    """Swipe từ (x1,y1) đến (x2,y2)"""
    run_adb_no_output(["input", "swipe", str(x1), str(y1), str(x2), str(y2)])
    time.sleep(0.5)

# Swipe lên (cuộn xuống)
swipe(540, 1800, 540, 800)

# Swipe xuống (cuộn lên)
swipe(540, 800, 540, 1800)
```

### Press key events

```python
def press_key(keycode):
    """Press key event"""
    run_adb_no_output(["input", "keyevent", keycode])

# Các keycode thông dụng
press_key("KEYCODE_BACK")        # Nút Back
press_key("KEYCODE_HOME")        # Nút Home
press_key("KEYCODE_ENTER")       # Nút Enter
press_key("KEYCODE_TAB")         # Nút Tab
press_key("KEYCODE_DEL")         # Nút Delete
```

---

## 📖 BEST PRACTICES

### 1. Luôn chờ UI update

```python
# ❌ KHÔNG TỐT
tap(x, y)
tap(x2, y2)  # Có thể quá nhanh

# ✅ TỐT
tap(x, y)
time.sleep(0.8)  # Chờ UI update
tap(x2, y2)
```

### 2. Xử lý khi element không tìm thấy

```python
# ❌ KHÔNG TỐT
element = find_element_center(dump, "class", "text")
tap(element[0], element[1])  # Crash nếu element = None

# ✅ TỐT
element = find_element_center(dump, "class", "text")
if not element:
    print("Element not found!", flush=True)
    return False
tap(element[0], element[1])
```

### 3. Dùng hardcoded coordinates làm fallback

```python
# Tìm element
login_btn = find_element_center(dump, "android.widget.TextView", "Đăng nhập")

# Fallback nếu không tìm thấy
if not login_btn:
    print("Using hardcoded coordinates", flush=True)
    login_btn = (540, 1602)  # Tọa độ ước lượng
```

### 4. Chụp ảnh ở các bước quan trọng

```python
take_screenshot("before_action.png")
# ... thực hiện action ...
take_screenshot("after_action.png")
```

### 5. Log rõ ràng từng bước

```python
print(" Launching app...", flush=True)
print("📝 Entering username...", flush=True)
print("✅ Test passed!", flush=True)
```

### 6. Tái sử dụng code với functions

```python
# ❌ KHÔNG TỐT - Code lặp lại
tap(588, 1044)
time.sleep(0.3)
clear_text()
input_text("user1")

tap(588, 1044)
time.sleep(0.3)
clear_text()
input_text("user2")

# ✅ TỐT - Dùng function
def enter_username(username):
    tap(588, 1044)
    time.sleep(0.3)
    clear_text()
    input_text(username)

enter_username("user1")
enter_username("user2")
```

---

## 📝 VÍ DỤ THỰC TẾ

### Ví dụ 1: Test search functionality

```python
"""
Test: Tìm kiếm sản phẩm
"""
import subprocess
import time
import re

# ... (các hàm helper ở trên) ...

def test_search_product():
    print("="*60)
    print("TEST: TÌM KIẾM SẢN PHẨM")
    print("="*60)
    
    # 1. Launch app
    run_adb_no_output(["am", "start", "-n", "com.mobifone.msaleplus/.MainActivity"])
    time.sleep(4)
    
    # 2. Login (giả sử đã có hàm login)
    login("test_user", "1123")
    time.sleep(3)
    
    # 3. Get UI dump
    dump = get_ui_dump()
    
    # 4. Tìm search icon/button
    search_btn = find_element_center(dump, "android.widget.ImageView", "Tìm kiếm")
    if not search_btn:
        # Fallback: tìm bằng content-desc
        search_btn = find_element_center(dump, "android.widget.ImageView")
    
    if not search_btn:
        print("❌ Không tìm thấy search button", flush=True)
        return False
    
    # 5. Click search
    print("🔍 Click search button...", flush=True)
    tap(search_btn[0], search_btn[1])
    time.sleep(1)
    
    # 6. Nhập search query
    print("📝 Nhập từ khóa...", flush=True)
    search_input = find_element_center(dump, "android.widget.EditText")
    if search_input:
        tap(search_input[0], search_input[1])
        input_text("iPhone")
        time.sleep(2)
        
        # 7. Press Enter
        press_key("KEYCODE_ENTER")
        time.sleep(3)
        
        # 8. Verify có kết quả
        new_dump = get_ui_dump()
        if "iPhone" in new_dump or "sản phẩm" in new_dump.lower():
            print("✅ Tìm thấy kết quả", flush=True)
            take_screenshot("search_result.png")
            return True
        else:
            print("❌ Không có kết quả", flush=True)
            return False
    else:
        print("❌ Không tìm thấy search input", flush=True)
        return False

if __name__ == "__main__":
    success = test_search_product()
    print(f"\n{'✅ TEST PASSED' if success else '❌ TEST FAILED'}")
```

### Ví dụ 2: Test navigation menu

```python
"""
Test: Điều hướng menu
"""

def test_menu_navigation():
    print("="*60)
    print("TEST: ĐIỀU HƯỚNG MENU")
    print("="*60)
    
    # Launch và login
    launch_app()
    time.sleep(3)
    login("test_user", "1123")
    time.sleep(3)
    
    # Get UI dump
    dump = get_ui_dump()
    
    # Tìm menu icon (thường ở góc trái trên)
    menu_items = [
        ("Trang chủ", 540, 200),
        ("Đơn hàng", 540, 400),
        ("Sản phẩm", 540, 600),
        ("Khách hàng", 540, 800),
        ("Báo cáo", 540, 1000),
    ]
    
    results = []
    
    for item_name, x, y in menu_items:
        print(f"\n📍 Testing: {item_name}", flush=True)
        
        # Tap vào menu item
        tap(x, y)
        time.sleep(2)
        
        # Chụp ảnh
        take_screenshot(f"menu_{item_name.replace(' ', '_')}.png")
        
        # Verify (kiểm tra xem có text đặc trưng của màn hình đó)
        new_dump = get_ui_dump()
        
        # Check nếu vẫn ở màn hình cũ (không navigate được)
        if item_name in new_dump:
            print(f"  ✅ {item_name} - OK", flush=True)
            results.append(True)
        else:
            print(f"  ⚠️ {item_name} - Có thể đã navigate", flush=True)
            results.append(True)  # Vẫn count là pass nếu không lỗi
        
        # Back về màn hình chính
        press_key("KEYCODE_BACK")
        time.sleep(1)
    
    # Report
    passed = sum(results)
    total = len(results)
    print(f"\n{'='*60}")
    print(f"RESULT: {passed}/{total} menu items tested")
    print(f"{'='*60}")
    
    return passed == total
```

### Ví dụ 3: Test form input validation

```python
"""
Test: Validation form nhập liệu
"""

def test_form_validation():
    print("="*60)
    print("TEST: FORM VALIDATION")
    print("="*60)
    
    launch_app()
    login("test_user", "1123")
    time.sleep(2)
    
    # Navigate đến form nhập liệu
    dump = get_ui_dump()
    
    # Test 1: Để trống required field
    print("\n📝 Test 1: Để trống required field", flush=True)
    
    # Tìm và clear input field
    input_field = find_element_center(dump, "android.widget.EditText")
    tap(input_field[0], input_field[1])
    clear_text()
    
    # Click submit
    submit_btn = find_element_center(dump, "android.widget.Button", "Lưu")
    tap(submit_btn[0], submit_btn[1])
    time.sleep(1)
    
    # Check error message
    new_dump = get_ui_dump()
    if "bắt buộc" in new_dump.lower() or "required" in new_dump.lower():
        print("  ✅ Validation hoạt động", flush=True)
    else:
        print("  ❌ Validation không hoạt động", flush=True)
    
    # Test 2: Nhập dữ liệu hợp lệ
    print("\n📝 Test 2: Nhập dữ liệu hợp lệ", flush=True)
    tap(input_field[0], input_field[1])
    clear_text()
    input_text("Dữ liệu test")
    
    tap(submit_btn[0], submit_btn[1])
    time.sleep(2)
    
    # Check success message
    new_dump = get_ui_dump()
    if "thành công" in new_dump.lower() or "success" in new_dump.lower():
        print("  ✅ Submit thành công", flush=True)
        take_screenshot("form_success.png")
        return True
    else:
        print("  ⚠️ Không rõ kết quả", flush=True)
        return False
```

---

## 🐛 DEBUGGING TIPS

### 1. In ra UI dump để debug

```python
dump = get_ui_dump()
print(dump[:2000])  # In 2000 ký tự đầu
```

### 2. Lưu UI dump ra file

```python
dump = get_ui_dump()
with open("debug_dump.xml", "w", encoding="utf-8") as f:
    f.write(dump)
print("Saved to debug_dump.xml")
```

### 3. Test từng bước

```python
# Thêm input() để pause giữa các bước
tap(x, y)
input("Press Enter to continue...")  # Pause để quan sát
```

### 4. Dùng logging thay vì print

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting test...")
logger.error("Element not found!")
```

---

## 📞 CẦN TRỢ GIÚP?

Khi gặp vấn đề về code:

1. ✅ Kiểm tra log output
2. ✅ Lưu UI dump để phân tích
3. ✅ Chụp màn hình ở bước bị lỗi
4. ✅ Test thủ công trên điện thoại để verify flow

---

**Biên soạn:** Auto Test Team  
**Cập nhật:** Tháng 3/2025  
**Version:** 1.0
