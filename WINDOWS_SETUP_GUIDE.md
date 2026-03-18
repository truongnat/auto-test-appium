# 📘 HƯỚNG DẪN TEST TỰ ĐỘNG TRÊN WINDOWS
### Dành cho Tester mSalePro Android - Không cần biết code

---

## 📋 MỤC LỤC

1. [Cài Đặt Phần Mềm](#cài-đặt-phần-mềm)
2. [Cài Đặt Môi Trường Test](#cài-đặt-môi-trường-test)
3. [Kết Nối Điện Thoại](#kết-nối-điện-thoại)
4. [Chạy Test Đầu Tiên](#chạy-test-đầu-tiên)
5. [Xử Lý Lỗi Thường Gặp](#xử-lý-lỗi-thường-gặp)

---

## 🛠️ CÀI ĐẶT PHẦN MỀM

### Bước 1: Cài đặt Python

1. **Tải Python:**
   - Truy cập: https://www.python.org/downloads/
   - Tải phiên bản **Python 3.11.x** (mới nhất)

2. **Cài đặt:**
   - Chạy file installer vừa tải
   - ⚠️ **QUAN TRỌNG:** Tick chọn ✅ **"Add Python to PATH"** ở màn hình đầu tiên
   - Chọn **"Install Now"**
   
3. **Kiểm tra:**
   - Mở Command Prompt (nhấn `Win + R`, gõ `cmd`, nhấn Enter)
   - Gõ lệnh:
   ```cmd
   python --version
   ```
   - Nếu hiện `Python 3.11.x` là thành công ✅

---

### Bước 2: Cài đặt Android SDK Platform Tools

1. **Tải Platform Tools:**
   - Truy cập: https://developer.android.com/studio/releases/platform-tools
   - Tải file **platform-tools-latest-windows.zip**

2. **Giải nén:**
   - Giải nén vào `C:\platform-tools` (tạo folder mới nếu cần)

3. **Thêm vào PATH:**
   - Nhấn `Win + R`, gõ `sysdm.cpl`, nhấn Enter
   - Tab **Advanced** → **Environment Variables**
   - Trong **System variables**, tìm và chọn **Path** → **Edit**
   - **New** → Thêm: `C:\platform-tools`
   - **OK** → **OK** → **OK**

4. **Kiểm tra:**
   - Mở Command Prompt mới
   - Gõ lệnh:
   ```cmd
   adb version
   ```
   - Nếu hiện thông tin version là thành công ✅

---

### Bước 3: Cài đặt Git (tùy chọn - để clone project)

1. **Tải Git:**
   - Truy cập: https://git-scm.com/download/win
   - Tải và cài đặt bản mới nhất

2. **Kiểm tra:**
   ```cmd
   git --version
   ```

---

## 📥 CÀI ĐẶT MÔI TRƯỜNG TEST

### Bước 1: Tải project test về máy

**Cách 1 - Clone từ Git (nếu có repo):**
```cmd
cd C:\
git clone <url-cua-project> auto-test-android
```

**Cách 2 - Copy thủ công:**
- Copy toàn bộ folder project vào `C:\auto-test-android`

### Bước 2: Cài đặt Python dependencies

```cmd
cd C:\auto-test-android
pip install -r requirements.txt
```

Nếu thành công sẽ hiện:
```
Successfully installed Appium-Python-Client-... selenium-...
```

### Bước 3: Cài đặt Appium Server (nếu cần test với Appium)

```cmd
# Cài Node.js trước (nếu chưa có)
# Tải từ: https://nodejs.org/ (chọn bản LTS)

# Cài Appium
npm install -g appium

# Cài driver cho Android
appium driver install uiautomator2
```

---

## 📱 KẾT NỐI ĐIỆN THOẠI

### Bước 1: Bật USB Debugging trên điện thoại

1. **Vào Settings (Cài đặt)**
2. **About Phone (Giới thiệu về điện thoại)**
3. Tìm **Build Number (Số hiệu bản dựng)**
4. **Nhấn 7 lần** vào Build Number đến khi hiện "You are now a developer"
5. Quay lại **Settings** → **Developer Options (Tùy chọn nhà phát triển)**
6. Bật **USB Debugging (Gỡ lỗi USB)** ✅

### Bước 2: Kết nối với máy tính

1. **Cắm cáp USB** vào máy tính
2. Trên điện thoại hiện popup **"Allow USB debugging?"**
3. Chọn **OK** hoặc **Always allow from this computer**

### Bước 3: Kiểm tra kết nối

```cmd
adb devices
```

**Kết quả thành công:**
```
List of devices attached
10AF571XYU0067D    device
```

**Nếu không thấy thiết bị:**
- Thử cắm cổng USB khác
- Chọn chế độ "File Transfer" hoặc "MTP" trên điện thoại
- Restart ADB:
  ```cmd
  adb kill-server
  adb start-server
  adb devices
  ```

---

## ▶️ CHẠY TEST ĐẦU TIÊN

### Test Login mSalePro

**Bước 1:** Kiểm tra kết nối
```cmd
adb devices
```

**Bước 2:** Chạy test
```cmd
cd C:\auto-test-android
python simple_login_test.py
```

**Bước 3:** Xem kết quả

**✅ Thành công:**
```
============================================================
✅ TEST PASSED - Login flow completed successfully
============================================================
```

**❌ Thất bại:**
```
❌ TEST FAILED - Login flow did not complete
```

### Xem ảnh kết quả

File `login_result.png` sẽ được lưu trong folder `C:\auto-test-android`

Mở bằng Windows Photos hoặc bất kỳ viewer nào.

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: "python is not recognized"

**Nguyên nhân:** Python chưa được thêm vào PATH

**Cách sửa:**
1. Mở Settings → System → About → Advanced system settings
2. Environment Variables → Path → Edit
3. Thêm: `C:\Users\<ten-cua-ban>\AppData\Local\Programs\Python\Python311\`
4. Thêm: `C:\Users\<ten-cua-ban>\AppData\Local\Programs\Python\Python311\Scripts\`
5. OK và mở Command Prompt mới

### Lỗi 2: "adb is not recognized"

**Nguyên nhân:** ADB chưa được thêm vào PATH

**Cách sửa:**
1. Mở Settings → System → About → Advanced system settings
2. Environment Variables → Path → Edit
3. Thêm: `C:\platform-tools`
4. OK và mở Command Prompt mới

### Lỗi 3: "no devices found"

**Cách sửa:**
```cmd
adb kill-server
adb start-server
adb devices
```

Nếu vẫn không thấy:
- Rút cáp USB, cắm lại
- Thử cổng USB khác (nên dùng cổng USB phía sau máy tính)
- Kiểm tra cáp USB (dùng cáp tốt, có truyền dữ liệu)
- Trên điện thoại: chọn chế độ "File Transfer"

### Lỗi 4: "unauthorized" khi adb devices

**Cách sửa:**
1. Rút cáp, cắm lại
2. Trên điện thoại hiện popup "Allow USB debugging?"
3. Chọn **OK**
4. Chạy lại `adb devices`

### Lỗi 5: Test chạy nhưng không nhập được text

**Nguyên nhân:** Bàn phím ảo không hỗ trợ ADB input

**Cách sửa:**
1. Vào Settings → Language & Input → Current Keyboard
2. Chọn **GBoard** hoặc **Android Keyboard (AOSP)**
3. Chạy lại test

### Lỗi 6: "app not installed" hoặc "activity not found"

**Cách sửa:**
```cmd
# Kiểm tra app đã cài chưa
adb shell pm list packages | findstr mobifone

# Nếu chưa có, cài app
adb install C:\path\to\msalepro.apk

# Xóa data app và chạy lại
adb shell pm clear com.mobifone.msaleplus
```

### Lỗi 7: "socket hang up" hoặc "connection refused"

**Cách sửa:**
```cmd
# Restart ADB
adb kill-server
adb start-server

# Restart điện thoại
# Chạy lại test
python simple_login_test.py
```

---

## 📂 CẤU TRÚC THƯ MỤC

```
C:\auto-test-android\
├── 📘 NO_CODE_TESTER_GUIDE.md   ← Đọc nếu cần chi tiết hơn
├── 📗 README.md                  ← Hướng dẫn nhanh
├── ⚙️ config.py                  ← Cấu hình test
├── 🧪 simple_login_test.py       ← Test login
├── 🔍 quick_inspect.py           ← Inspect UI nhanh
└── 📸 login_result.png           ← Ảnh kết quả
```

---

## ⚙️ CẤU HÌNH TEST

### Thay đổi username/password

Mở file `config.py` bằng Notepad hoặc VS Code:

```python
TEST_CREDENTIALS = {
    "valid_username": "duyen_test@cntt",  # ← Sửa username
    "valid_password": "1123",              # ← Sửa password
}
```

Lưu file và chạy lại test.

---

## 📞 CẦN TRỢ GIÚP?

Khi báo lỗi, vui lòng cung cấp:

1. ✅ **Nội dung lỗi** (copy nguyên văn từ Command Prompt)
2. ✅ **Ảnh chụp màn hình lỗi** (dùng Snipping Tool: `Win + Shift + S`)
3. ✅ **Kết quả `adb devices`**
4. ✅ **Phiên bản Android** (Settings → About Phone → Android Version)
5. ✅ **Tên điện thoại** (Settings → About Phone → Device Name)

---

## 🎯 CÁC LỆNH CƠ BẢN

| Lệnh | Mục đích |
|------|----------|
| `adb devices` | Xem thiết bị đã kết nối chưa |
| `adb kill-server` | Restart ADB server |
| `python simple_login_test.py` | Chạy test login |
| `python quick_inspect.py` | Xem UI elements trong app |

---

## 📝 CHECKLIST TRƯỚC KHI CHẠY TEST

- [ ] Python đã cài và thêm vào PATH
- [ ] ADB đã cài và thêm vào PATH
- [ ] USB Debugging đã bật trên điện thoại
- [ ] Cáp USB được kết nối tốt
- [ ] App mSalePro đã cài trên điện thoại
- [ ] `adb devices` hiện thiết bị là "device"
- [ ] Tài khoản test đã được tạo và active

---

**Biên soạn:** Auto Test Team  
**Cập nhật:** Tháng 3/2025  
**Platform:** Windows 10/11
