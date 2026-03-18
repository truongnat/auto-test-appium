# 📘 HƯỚNG DẪN TEST TỰ ĐỘNG CHO NGƯỜI KHÔNG CODE
### Dành cho Tester mSalePro Android

---

## 📋 MỤC LỤC

1. [Giới Thiệu](#giới-thiệu)
2. [Cài Đặt Môi Trường](#cài-đặt-môi-trường)
3. [Chạy Test Đầu Tiên](#chạy-test-đầu-tiên)
4. [Hiểu Về Test Script](#hiểu-về-test-script)
5. [Sửa Test Theo Yêu Cầu](#sửa-test-theo-yêu-cầu)
6. [Xử Lý Lỗi Thường Gặp](#xử-lý-lỗi-thường-gặp)
7. [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

## 🎯 GIỚI THIỆU

### Bạn là ai?
- ✅ Tester/QC không chuyên code
- ✅ Biết sử dụng máy tính cơ bản
- ✅ Muốn tự động hóa test mà không cần học lập trình sâu

### Bộ test này giúp gì cho bạn?
- 📱 Test tự động app Android mSalePro
- 🔐 Test login, các màn hình chính
- 📸 Tự động chụp ảnh kết quả
- ✅ Báo cáo pass/fail rõ ràng

### Công nghệ sử dụng (bạn KHÔNG CẦN hiểu sâu)
- **ADB**: Công cụ giao tiếp với điện thoại Android
- **Python**: Ngôn ngữ lập trình (chỉ cần biết chạy script)
- **Appium**: Framework test mobile (dùng khi cần nâng cao)

---

## 🛠️ CÀI ĐẶT MÔI TRƯỜNG

### Bước 1: Cài đặt Python

**Windows:**
1. Tải Python từ https://www.python.org/downloads/
2. Chọn phiên bản Python 3.10 trở lên
3. Khi cài, tick chọn ✅ **"Add Python to PATH"**
4. Nhấn Install Now

**macOS:**
```bash
# Kiểm tra Python đã có chưa
python3 --version

# Nếu chưa có, cài bằng Homebrew
brew install python@3.11
```

### Bước 2: Cài đặt Android SDK Platform Tools

**Windows:**
1. Tải từ: https://developer.android.com/studio/releases/platform-tools
2. Giải nén vào `C:\platform-tools`
3. Thêm vào PATH:
   - Chuột phải This PC → Properties → Advanced System Settings
   - Environment Variables → Path → Edit → New
   - Thêm `C:\platform-tools`

**macOS:**
```bash
brew install --cask android-platform-tools
```

### Bước 3: Kết nối điện thoại/tablet

1. **Bật USB Debugging trên thiết bị:**
   - Vào Settings → About Phone
   - Tap 7 lần vào "Build Number" để enable Developer Options
   - Quay lại Settings → Developer Options
   - Bật **USB Debugging**

2. **Kết nối với máy tính:**
   - Cắm cáp USB
   - Trên điện thoại hiện popup "Allow USB debugging?" → Chọn **OK**

3. **Kiểm tra kết nối:**
```bash
adb devices
```
Nếu thấy thiết bị hiện ra là thành công:
```
List of devices attached
10AF571XYU0067D    device
```

### Bước 4: Cài đặt thư viện test

Mở terminal/command prompt, cd vào thư mục test:
```bash
cd /Users/truongdq/tx/dev/auto-test-android
```

Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

---

## ▶️ CHẠY TEST ĐẦU TIÊN

### Test Login mSalePro

**Bước 1:** Đảm bảo điện thoại đã kết nối
```bash
adb devices
```

**Bước 2:** Chạy test login
```bash
python simple_login_test.py
```

**Bước 3:** Xem kết quả

Kết quả thành công sẽ hiện:
```
============================================================
✅ TEST PASSED - Login flow completed successfully
============================================================
```

Và file ảnh `login_result.png` sẽ được lưu trong thư mục.

---

## 📖 HIỂU VỀ TEST SCRIPT

### File `simple_login_test.py` làm gì?

Script này thực hiện các bước **giống như bạn test thủ công**:

```
1. Mở app mSalePro
2. Nhập username
3. Nhập password  
4. Ẩn bàn phím
5. Click nút Đăng nhập
6. Chụp ảnh màn hình kết quả
7. Báo cáo thành công/thất bại
```

### Các hàm chính (để tham khảo)

| Hàm | Chức năng |
|-----|-----------|
| `tap(x, y)` | Click vào tọa độ (x, y) trên màn hình |
| `input_text("abc")` | Nhập chữ "abc" vào ô đang chọn |
| `clear_text()` | Xóa nội dung ô input |
| `hide_keyboard()` | Ẩn bàn phím ảo |
| `take_screenshot("file.png")` | Chụp màn hình |

---

## ✏️ SỬA TEST THEO YÊU CẦU

### Thay đổi username/password

Mở file `config.py` trong text editor (Notepad, VS Code, Sublime Text):

```python
TEST_CREDENTIALS = {
    "valid_username": "duyen_test@cntt",  # ← Sửa username ở đây
    "valid_password": "1123",              # ← Sửa password ở đây
    "invalid_username": "wrong_user",
    "invalid_password": "wrong_password",
}
```

### Test với tài khoản khác

Chạy test với tham số:
```bash
python simple_login_test.py
```

Hoặc sửa trực tiếp trong `simple_login_test.py`:
```python
success = simple_login_test(
    username="your_username",   # ← Sửa ở đây
    password="your_password"    # ← Sửa ở đây
)
```

### Thêm bước test mới

Liên hệ với dev để được hỗ trợ thêm test case mới.

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: "adb: command not found"

**Nguyên nhân:** Chưa cài ADB hoặc chưa thêm vào PATH

**Cách sửa:**
```bash
# Kiểm tra adb đã cài chưa
which adb         # macOS/Linux
where adb         # Windows

# Nếu chưa có, làm theo Bước 2 phần Cài đặt
```

### Lỗi 2: "no devices found"

**Nguyên nhân:** Điện thoại không kết nối với máy tính

**Cách sửa:**
1. Rút cáp USB ra, cắm lại
2. Trên điện thoại, chọn chế độ "File Transfer" hoặc "MTP"
3. Kiểm tra USB Debugging đã bật chưa
4. Chạy lại: `adb devices`

### Lỗi 3: "app not installed" hoặc "activity not found"

**Nguyên nhân:** App mSalePro chưa cài trên điện thoại

**Cách sửa:**
```bash
# Cài app từ file APK
adb install path/to/msalepro.apk
```

### Lỗi 4: Test chạy nhưng không nhập được text

**Nguyên nhân:** Bàn phím ảo không hỗ trợ input qua ADB

**Cách sửa:**
- Thử đổi bàn phím thành GBoard hoặc bàn phím mặc định của Android
- Restart app và chạy lại test

### Lỗi 5: "socket hang up" hoặc "connection refused"

**Nguyên nhân:** Appium server gặp vấn đề

**Cách sửa:**
```bash
# Restart ADB server
adb kill-server
adb start-server

# Chạy lại test
python simple_login_test.py
```

### Lỗi 6: Test báo thành công nhưng app chưa login

**Nguyên nhân:** Tài khoản test không hợp lệ

**Cách sửa:**
1. Kiểm tra username/password trong `config.py`
2. Thử login thủ công trên điện thoại để verify tài khoản
3. Chạy lại test

---

## 📚 TÀI LIỆU THAM KHẢO

### Tài liệu trong project này

| File | Mục đích |
|------|----------|
| `README.md` | Giới thiệu tổng quan về project |
| `INSPECTOR_GUIDE.md` | Hướng dẫn dùng Appium Inspector |
| `quick_inspect.py` | Script nhanh để xem UI elements |
| `inspect_app.py` | Script inspect chi tiết app |

### Tài liệu bên ngoài

- **ADB Commands**: https://developer.android.com/studio/command-line/adb
- **Python Basics**: https://www.python.org/about/gettingstarted/
- **Appium Documentation**: https://appium.io/docs/

### Các lệnh ADB hữu ích cho tester

```bash
# Xem danh sách thiết bị
adb devices

# Chụp màn hình
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png

# Quay video màn hình (max 3 phút)
adb shell screenrecord /sdcard/demo.mp4
adb pull /sdcard/demo.mp4

# Cài app
adb install app.apk

# Gỡ app
adb uninstall com.mobifone.msaleplus

# Xóa data app
adb shell pm clear com.mobifone.msaleplus

# Xem log app
adb logcat | grep mSalePro

# Restart app
adb shell am start -n com.mobifone.msaleplus/.MainActivity
```

---

## 🆘 CẦN TRỢ GIÚP?

Khi gặp vấn đề, hãy cung cấp các thông tin sau để được hỗ trợ nhanh:

1. ✅ **Lỗi hiển thị gì?** (copy nguyên văn message lỗi)
2. ✅ **Ảnh chụp màn hình lỗi**
3. ✅ **Đã làm những gì trước khi lỗi?**
4. ✅ **Phiên bản Android?** (Settings → About Phone)
5. ✅ **Kết quả `adb devices`**

---

## 📝 CHECKLIST TRƯỚC KHI CHẠY TEST

- [ ] Điện thoại đã bật USB Debugging
- [ ] Cáp USB được kết nối tốt
- [ ] App mSalePro đã cài trên điện thoại
- [ ] Đã chạy `adb devices` và thấy thiết bị
- [ ] Tài khoản test đã được tạo và active
- [ ] Đã đóng các app khác trên điện thoại (để test nhanh hơn)

---

**Biên soạn:** Auto Test Team  
**Cập nhật:** Tháng 3/2025  
**Version:** 1.0
