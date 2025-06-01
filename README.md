# Hệ Thống Quản Lý Trang Trại (Farm Management System)


Ứng dụng quản lý trang trại toàn diện với các chức năng quản lý cây trồng, vật nuôi, hoạt động, tài chính và kho hàng, tích hợp cảnh báo thời tiết thông minh.

## 📌 Tính năng chính

### 🌱 Quản lý cây trồng
- Theo dõi thông tin cây trồng (tên, loại, ngày trồng, diện tích)
- Quản lý trạng thái (đang phát triển, thu hoạch, bệnh)
- Cảnh báo chăm sóc dựa trên thời tiết

### 🐄 Quản lý vật nuôi
- Theo dõi thông tin vật nuôi (tên, loại, số lượng)
- Quản lý tình trạng sức khỏe (khỏe mạnh, bệnh, đang điều trị)
- Cảnh báo chăm sóc theo điều kiện thời tiết

### 📅 Quản lý hoạt động
- Lập kế hoạch hoạt động trang trại
- Theo dõi tiến độ và trạng thái hoạt động
- Phân công người phụ trách

### 💰 Quản lý tài chính
- Theo dõi thu chi
- Phân loại giao dịch (bán sản phẩm, mua giống, lương nhân viên...)
- Báo cáo tổng số dư và thống kê tài chính

### 📦 Quản lý kho hàng
- Quản lý vật tư (tên, số lượng, đơn giá)
- Theo dõi nhập/xuất kho
- Quản lý nhà cung cấp

### ⛅ Thời tiết
- Hiển thị thông tin thời tiết theo địa điểm
- Cảnh báo thời tiết ảnh hưởng đến trang trại
- Gợi ý biện pháp chăm sóc

### 🔐 Hệ thống phân quyền
- 2 cấp độ người dùng: Admin và User thường
- Chức năng đăng nhập, đổi mật khẩu
- Phân quyền truy cập chức năng

## 🛠 Yêu cầu hệ thống

- **Hệ điều hành**: Windows 10/11, macOS, Linux
- **Python**: Phiên bản 3.8+
- **Thư viện yêu cầu**: Xem trong file `requirements.txt`
- **Phần cứng tối thiểu**:
  - RAM: 2GB
  - Ổ cứng trống: 100MB
  - Kết nối Internet (cho chức năng thời tiết)

## 🔧 Cài đặt

### Cài đặt từ mã nguồn

1. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/farm-management-system.git
   cd farm-management-system

2. **Cài đặt thư viện vần thiết**:
   pip install -r requirements.txt

3. **Cấu hình API KEY thời tiết**:
   WEATHER_API_KEY=your_openweather_api_key_here
4. **Chạy chương trình**:
   python main.py

   
  