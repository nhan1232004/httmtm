# Hướng Dẫn Cài Đặt và Chạy Dự Án

## 1. Thiết lập Môi Trường
- Cài đặt Node.js và npm từ trang chính thức của Node.js.
- Clone dự án từ GitHub về máy:
  ```bash
  git clone https://github.com/nhan1232004/httmtm.git
  cd httmtm
  ```

## 2. Cấu Hình MongoDB
- Cài đặt MongoDB từ trang chính thức.
- Khởi động MongoDB:
  ```bash
  mongod
  ```
- Tạo database và collection cần thiết sử dụng MongoDB shell hoặc một công cụ GUI như MongoDB Compass.

## 3. Chạy Máy Chủ Backend
- Trong thư mục dự án, cài đặt các thư viện cần thiết:
  ```bash
  npm install
  ```
- Chạy máy chủ backend:
  ```bash
  npm start
  ```

## 4. Chạy Ứng Dụng Frontend
- Chuyển đến thư mục frontend nếu có:
  ```bash
  cd frontend
  ```
- Cài đặt các thư viện cần thiết cho frontend:
  ```bash
  npm install
  ```
- Chạy ứng dụng frontend:
  ```bash
  npm start
  ```

## 5. Kiểm Tra Toàn Bộ Hệ Thống
- Truy cập ứng dụng từ trình duyệt: `http://localhost:3000`
- Kiểm tra các chức năng cơ bản của ứng dụng để đảm bảo mọi thứ hoạt động bình thường.