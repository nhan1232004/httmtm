# KẾ HOẠCH THỰC HIỆN ĐỀ TÀI: BIG DATA TRONG THƯƠNG MẠI ĐIỆN TỬ

## 1\. Lựa chọn bài toán cụ thể

Big Data rất rộng, để làm một ứng dụng thực tiễn, nhóm nên thu hẹp lại thành một trong các bài toán sau:

- **Bài toán 1 (Khuyên chọn):** Hệ thống gợi ý sản phẩm (Recommendation System) - Gợi ý dựa trên lịch sử mua hàng, đánh giá hoặc sản phẩm tương tự.
- **Bài toán 2:** Phân loại và phân tích tệp khách hàng (Customer Segmentation) - Dùng thuật toán gom cụm (K-Means) để chia nhóm khách hàng (VIP, dễ rời bỏ, mua nhiều...) dựa trên mô hình RFM (Recency, Frequency, Monetary).
- **Bài toán 3:** Phân tích cảm xúc người dùng (Sentiment Analysis) - Phân tích Big Data từ các luồng review/comment để đánh giá chất lượng sản phẩm.

_(Kế hoạch dưới đây sẽ viết theo hướng_ **_Bài toán 1: Hệ thống gợi ý sản phẩm_**_)_

## 2\. GIAI ĐOẠN GIỮA KỲ (Nghiên cứu & Demo cơ bản)

### 2.1. Báo cáo lý thuyết (Word/PDF Report)

Cần bao quát các nội dung sau:

- **Mở đầu:** Giới thiệu tổng quan về TMĐT và tầm quan trọng của dữ liệu lớn (Big Data).
- **Cơ sở lý thuyết về Big Data:** Định nghĩa (5V: Volume, Velocity, Variety, Veracity, Value), các công nghệ cốt lõi (Hadoop, Spark, NoSQL).
- **Ứng dụng Big Data trong TMĐT:** Nêu các ví dụ thực tế (Amazon, Shopee, Tiki đang dùng Big Data để làm gì?).
- **Đi sâu vào bài toán cốt lõi:** Trình bày lý thuyết về Hệ thống gợi ý (Collaborative Filtering, Content-based Filtering).
- **Thiết kế Demo:** Giới thiệu bộ dữ liệu (Dataset) sử dụng (ví dụ: Amazon Reviews dataset từ Kaggle) và luồng xử lý dữ liệu.

### 2.2. Slide Thuyết trình (PPT)

- Cô đọng nội dung từ Report. Sử dụng nhiều biểu đồ, hình ảnh trực quan.
- Trình bày tối đa 15-20 slide, tập trung vào **"Big Data giải quyết nỗi đau (pain-point) gì cho doanh nghiệp TMĐT?"**.
- Dành 3-5 phút cuối để chạy Demo.

### 2.3. Demo Code (Giữa kỳ)

Ở giữa kỳ, giảng viên thường không yêu cầu một web app hoàn chỉnh. Demo ở mức "Proof of Concept" (Chứng minh tính khả thi).

- **Công cụ:** Python (Jupyter Notebook / Google Colab).
- **Thực hiện:** \* Tải một bộ dữ liệu TMĐT thật từ Kaggle (khoảng vài trăm ngàn đến vài triệu dòng để thể hiện yếu tố "Big").
  - Viết script dùng Pandas để làm sạch dữ liệu.
  - Viết thuật toán (ví dụ: Tính độ tương đồng Cosine Similarity) để đưa ra danh sách sản phẩm gợi ý khi nhập vào 1 mã khách hàng hoặc mã sản phẩm.
  - In kết quả ra màn hình console hoặc dạng bảng biểu đồ.

## 3\. GIAI ĐOẠN CUỐI KỲ (Hoàn thiện & Xây dựng Ứng dụng Thực tiễn)

### 3.1. Nâng cấp Báo cáo (Report Cuối kỳ)

- Hoàn thiện lý thuyết từ góp ý của Giữa kỳ.
- Bổ sung phần **Kiến trúc hệ thống (System Architecture)**: Vẽ sơ đồ hệ thống thực tế (Client -> Server -> Database -> Data Processing Engine).
- Bổ sung phần **Đánh giá thuật toán**: Dùng các thang đo như RMSE, Precision, Recall để chứng minh độ chính xác của ứng dụng.

### 3.2. Ứng dụng thực tiễn (Final Project/App)

Nâng cấp từ đoạn code Python khô khan ở giữa kỳ thành một **ứng dụng Web thực tế**.

- **Giao diện người dùng (Front-end):** \* Sử dụng HTML/CSS/JS (hoặc ReactJS).
  - Tạo giao diện một trang chủ mua sắm đơn giản (Homepage).
  - Có khu vực "Dành riêng cho bạn" (Recommended for You) hiển thị sản phẩm dựa trên Big Data.
- **Hệ thống xử lý (Back-end & Data):**
  - Sử dụng Python (FastAPI hoặc Flask) làm API.
  - Khi người dùng click vào một sản phẩm A, Front-end gọi API gửi dữ liệu về Back-end.
  - Back-end chạy mô hình Big Data đã train sẵn, trả về danh sách 5 sản phẩm liên quan nhất.
- **Yếu tố "Big Data" (Nâng cao để lấy điểm A):** \* Thay vì dùng Pandas thông thường, hãy thử dùng **PySpark** để xử lý tập dữ liệu hàng triệu dòng (thể hiện khả năng xử lý song song).
  - Lưu trữ dữ liệu bằng MongoDB thay vì file CSV.

## 4\. GỢI Ý BỘ DỮ LIỆU (DATASETS) TỪ KAGGLE

- **Olist Brazilian E-commerce Dataset:** Rất đầy đủ về đơn hàng, khách hàng, sản phẩm, review. (Thích hợp làm Customer Segmentation).
- **Amazon Product Reviews:** Cực lớn, rất tốt để làm Recommendation System hoặc Sentiment Analysis.
- **H&M Personalized Fashion Recommendations:** Dữ liệu mua sắm quần áo có hình ảnh.