# 🤖 Android Automation Test - mSalePro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Appium](https://img.shields.io/badge/Appium-2.x-green.svg)](https://appium.io)
[![Platform](https://img.shields.io/badge/Platform-Android-lightgrey.svg)](https://android.com)

---

## 📖 DÀNH CHO AI?

| Đối tượng | Hướng dẫn phù hợp |
|-----------|-------------------|
| 👶 **Người mới bắt đầu** (không code) | Đọc [NO_CODE_TESTER_GUIDE.md](NO_CODE_TESTER_GUIDE.md) |
| 🪟 **Người dùng Windows** | Đọc [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) |
| 👨💻 **Tester có kinh nghiệm** | Đọc phần Quick Start bên dưới |
| 🧑‍💻 **Developer muốn code test** | Đọc [CODING_GUIDE.md](CODING_GUIDE.md) |
| 🔍 **Inspect UI elements** | Đọc [INSPECTOR_GUIDE.md](INSPECTOR_GUIDE.md) |

---

## ⚡ QUICK START (5 phút)

### 1. Cài đặt (chỉ lần đầu)

```bash
# Cài dependencies
pip install -r requirements.txt

# Cài Appium server (nếu chưa có)
npm install -g appium
appium driver install uiautomator2
```

### 2. Kết nối điện thoại

```bash
# Bật USB Debugging trên điện thoại
# Cắm cáp USB và kiểm tra
adb devices
```

### 3. Chạy test login

```bash
python simple_login_test.py
```

### 4. Xem kết quả

- ✅ **Pass**: Hiện message thành công + file `login_result.png`
- ❌ **Fail**: Hiện message lỗi + screenshot

---

## 📁 CẤU TRÚC PROJECT

```
auto-test-android/
├── 📘 NO_CODE_TESTER_GUIDE.md   ← Người mới BẮT ĐẦU TỪ ĐÂY
├── 📗 README.md                  ← File này (tổng quan)
├── 📙 INSPECTOR_GUIDE.md         ← Hướng dẫn inspect UI elements
│
├── ⚙️ config.py                  ← Cấu hình (app package, credentials)
├── ⚙️ conftest.py                ← Pytest fixtures
├── 📦 requirements.txt           ← Python dependencies
│
├── 🧪 simple_login_test.py       ← Test login (ADB method - ổn định nhất)
├── 🔍 quick_inspect.py           ← Script inspect nhanh UI
├── 🔍 inspect_app.py             ← Script inspect chi tiết
│
├── 📂 pages/                     ← Page Objects (nếu có)
└──  tests/                     ← Test cases (pytest)
```

---

## 🎯 CÁC TEST CÓ SẴN

| Test File | Mô tả | Khi nào dùng |
|-----------|-------|--------------|
| `simple_login_test.py` | Test login flow | ✅ Dùng hàng ngày |
| `quick_inspect.py` | Xem UI elements | Khi cần tìm locator |
| `inspect_app.py` | Inspect chi tiết app | Khi cần debug sâu |

---

## ⚙️ CẤU HÌNH

### Thay đổi app package/activity

Sửa trong `config.py`:

```python
ANDROID_CONFIG = {
    "appPackage": "com.mobifone.msaleplus",  # ← Package app của bạn
    "appActivity": ".MainActivity",           # ← Activity khởi động
    ...
}
```

### Thay đổi credentials

Sửa trong `config.py`:

```python
TEST_CREDENTIALS = {
    "valid_username": "duyen_test@cntt",  # ← Username test
    "valid_password": "1123",              # ← Password test
    ...
}
```

---

## 🧪 CHẠY TEST

### Chạy test login (khuyến nghị)

```bash
python simple_login_test.py
```

### Chạy test với pytest

```bash
# Tất cả tests trong folder tests/
pytest tests/ -v

# Test cụ thể
pytest tests/test_login.py::test_valid_login -v

# Với screenshot report
pytest tests/ -v --html=report.html
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: "adb: command not found"

```bash
# Cài Android SDK Platform Tools
# https://developer.android.com/studio/releases/platform-tools

# macOS
brew install --cask android-platform-tools

# Windows: Tải và thêm vào PATH
# Xem chi tiết: WINDOWS_SETUP_GUIDE.md
```

### Lỗi: "no devices found"

```bash
# 1. Kiểm tra cáp USB
# 2. Bật USB Debugging trên điện thoại
# 3. Restart ADB
adb kill-server
adb start-server
adb devices
```

### Lỗi: "socket hang up"

```bash
# Test sử dụng ADB method (không cần Appium)
python simple_login_test.py

# Nếu vẫn lỗi, restart điện thoại và chạy lại
```

### Lỗi: "app not installed"

```bash
# Cài app mSalePro
adb install msalepro.apk

# Hoặc check package name trong config.py
```

---

## 📚 TÀI LIỆU

| Tài liệu | Nội dung |
|----------|----------|
| [NO_CODE_TESTER_GUIDE.md](NO_CODE_TESTER_GUIDE.md) | **Hướng dẫn chi tiết cho người không code** |
| [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) | **Hướng dẫn cài đặt trên Windows** |
| [CODING_GUIDE.md](CODING_GUIDE.md) | **Hướng dẫn code và mở rộng test** |
| [INSPECTOR_GUIDE.md](INSPECTOR_GUIDE.md) | Dùng Appium Inspector tìm UI locators |
| [requirements.txt](requirements.txt) | Danh sách Python packages cần cài |

---

## 🔧 CÁC LỆNH ADB HỮU ÍCH

```bash
# Xem thiết bị
adb devices

# Chụp màn hình
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png .

# Quay video (max 3 phút)
adb shell screenrecord /sdcard/demo.mp4
adb pull /sdcard/demo.mp4 .

# Cài/gỡ app
adb install app.apk
adb uninstall com.mobifone.msaleplus

# Xóa data app
adb shell pm clear com.mobifone.msaleplus

# Xem log
adb logcat | grep mSalePro

# Restart app
adb shell am start -n com.mobifone.msaleplus/.MainActivity
```

---

## 📞 CẦN TRỢ GIÚP?

Khi báo lỗi, vui lòng cung cấp:

1. ✅ Nội dung lỗi (copy nguyên văn)
2. ✅ Ảnh chụp màn hình lỗi
3. ✅ Kết quả `adb devices`
4. ✅ Phiên bản Android (`adb shell getprop ro.build.version.release`)

---

## 🚀 NEXT STEPS

- [ ] Đọc [NO_CODE_TESTER_GUIDE.md](NO_CODE_TESTER_GUIDE.md) nếu bạn mới bắt đầu
- [ ] Chạy thử `simple_login_test.py`
- [ ] Tìm hiểu cách inspect UI với `quick_inspect.py`
- [ ] Thêm test cases mới cho các màn hình khác

---

**Biên soạn:** Auto Test Team  
**Cập nhật:** Tháng 3/2025  
**Version:** 2.0
# auto-test-appium
