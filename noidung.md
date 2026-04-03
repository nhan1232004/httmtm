# BÁO CÁO GIỮA KỲ: ỨNG DỤNG BIG DATA TRONG HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ

**(Nghiên cứu và Xây dựng Hệ thống Gợi ý Sản phẩm)**

## CHƯƠNG 1: TỔNG QUAN VỀ BUSINESS INTELLIGENCE VÀ BIG DATA

### 1.1. Từ Business Intelligence (BI) đến Big Data

Theo quá trình phát triển (Chương 1 của bài giảng), Business Intelligence (BI) ban đầu được định nghĩa là khả năng nắm bắt các mối quan hệ của các sự kiện để hướng tới mục tiêu mong muốn (Luhn, 1958). Trọng tâm của BI truyền thống là Data Warehouse (Kho dữ liệu) và các công cụ OLAP, Báo cáo (Reporting).

Tuy nhiên, trong kỷ nguyên số, với sự bùng nổ của các hệ thống Thương mại điện tử (TMĐT), dữ liệu không chỉ nằm ở dạng cấu trúc (bảng biểu giao dịch) mà còn ở dạng phi cấu trúc (lịch sử click chuột, văn bản đánh giá, hình ảnh). Điều này dẫn đến sự dịch chuyển và mở rộng từ BI sang **Big Data (Dữ liệu lớn)**.

Big Data trong TMĐT được đặc trưng bởi mô hình 5V:

- **Volume (Dung lượng):** Khối lượng dữ liệu khổng lồ từ hàng triệu giao dịch và hành vi người dùng mỗi ngày.
- **Velocity (Tốc độ):** Dữ liệu sinh ra liên tục theo thời gian thực (real-time stream).
- **Variety (Đa dạng):** Đa dạng nguồn dữ liệu (Cơ sở dữ liệu, Log file, Mạng xã hội, Text/Review).
- **Veracity (Tính xác thực):** Độ nhiễu của dữ liệu lớn, cần được làm sạch (Data Provisioning).
- **Value (Giá trị):** Khai phá dữ liệu để mang lại doanh thu (ví dụ: gợi ý đúng sản phẩm cho đúng người).

### 1.2. Mục tiêu của việc ứng dụng Big Data trong TMĐT

Hệ thống TMĐT sử dụng Big Data để giải quyết các mục tiêu phân tích (Analytical Goals) từ mô tả (Descriptive) đến dự đoán (Predictive):

- Hiểu rõ hành vi khách hàng (Customer Perspective).
- Tối ưu hóa quy trình vận hành và chuỗi cung ứng (Production/Operational Perspective).
- Tăng tỷ lệ chuyển đổi (Conversion Rate) và giá trị vòng đời khách hàng (Customer Lifetime Value).

## CHƯƠNG 2: QUY TRÌNH XỬ LÝ VÀ PHÂN TÍCH DỮ LIỆU TMĐT

_(Dựa trên nền tảng Data Provisioning & Visualization - Chương 3 & 4)_

### 2.1. Cung cấp và tích hợp dữ liệu (Data Provisioning)

Dữ liệu TMĐT hiếm khi sẵn sàng để phân tích ngay. Quá trình chuyển đổi từ **Dữ liệu giao dịch (Transactional Data - OLTP)** sang **Dữ liệu phân tích (Analytical Data - OLAP)** đòi hỏi quá trình ETL (Extract, Transform, Load):

- **Data Extraction:** Trích xuất dữ liệu từ nhiều nguồn (Database bán hàng của Magento/Shopify, Log truy cập web, API mạng xã hội).
- **Schema & Data Integration:** Tích hợp dữ liệu để giải quyết xung đột (ví dụ: cùng một khách hàng nhưng lưu tên khác nhau ở hệ thống CRM và hệ thống Website).

### 2.2. Mô tả và Trực quan hóa dữ liệu (Data Description & Visualization)

Trước khi chạy các thuật toán AI/Machine Learning, dữ liệu cần được mô tả để hiểu rõ phân phối. Trong TMĐT, việc trực quan hóa (Visualization) thường tập trung vào:

- **Góc nhìn khách hàng (Customer perspective):** Trực quan hóa dữ liệu chéo (Cross-sectional) như nhân khẩu học, hoặc dữ liệu theo thời gian (Temporal) như lịch sử mua hàng.
- **Reporting:** Tạo các Dashboard báo cáo tổng quan về doanh thu, tỷ lệ bỏ giỏ hàng (Cart abandonment rate).

## CHƯƠNG 3: CÁC KỸ THUẬT DATA MINING YẾU LƯỢC TRONG TMĐT

_(Dựa trên nền tảng Data Mining - Chương 5, 6, 8)_

Hệ thống TMĐT áp dụng mạnh mẽ các kỹ thuật khai phá dữ liệu (Data Mining) để tạo ra giá trị:

### 3.1. Phân tích dữ liệu chéo (Cross-Sectional Data Mining)

- **Học có giám sát (Supervised Learning - Phân lớp/Hồi quy):** Dùng để dự đoán một khách hàng có khả năng rời bỏ hệ thống hay không (Churn Prediction), hoặc dự đoán sức mua trong tương lai.
- **Học không giám sát (Unsupervised Learning - Phân cụm/Clustering):** Sử dụng các thuật toán như K-Means để gom nhóm khách hàng (Customer Segmentation) dựa trên mô hình RFM (Recency - Thời gian mua gần nhất, Frequency - Tần suất mua, Monetary - Giá trị mua). Từ đó, hệ thống có chiến dịch Marketing riêng cho nhóm "Khách hàng VIP" hoặc "Khách hàng sắp rời bỏ".

### 3.2. Phân tích dữ liệu chuỗi thời gian (Temporal Data Mining)

- **Khai phá luật kết hợp (Association Analysis / Market Basket Analysis):** Đây là kỹ thuật kinh điển trong TMĐT (ví dụ: thuật toán Apriori). Mục tiêu là tìm ra các tập phổ biến (Frequent itemsets) dựa trên quy tắc _"Khách hàng mua sản phẩm A thường sẽ mua thêm sản phẩm B"_.
- **Sequence Mining:** Phân tích chuỗi hành động của người dùng (ví dụ: Xem trang chủ -> Tìm kiếm "điện thoại" -> Xem chi tiết iPhone -> Thêm vào giỏ -> Thanh toán) để tìm ra "nút thắt cổ chai" khiến khách hàng thoát trang.

### 3.3. Phân tích đa khía cạnh (Multiple Perspectives & Text Mining)

- **Text Mining (Khai phá văn bản):** Xử lý khối lượng lớn các bình luận, đánh giá (Reviews) của khách hàng để làm **Sentiment Analysis (Phân tích cảm xúc)**. Hệ thống sẽ tự động phân loại review là Tích cực (Positive), Tiêu cực (Negative) hoặc Trung tính (Neutral).
- **Social Network Analysis:** Phân tích mạng xã hội để xác định các cá nhân có sức ảnh hưởng (Influencers) tác động đến việc mua hàng của mạng lưới bạn bè.

## CHƯƠNG 4: BÀI TOÁN TRỌNG TÂM - HỆ THỐNG GỢI Ý SẢN PHẨM (RECOMMENDATION SYSTEM)

_(Đây là nội dung chính mà nhóm sẽ làm Demo và Ứng dụng)_

### 4.1. Giới thiệu Hệ thống Gợi ý

Hệ thống gợi ý là một trong những ứng dụng thành công và mang lại lợi nhuận cao nhất của Big Data trong TMĐT (Ví dụ: 35% doanh thu của Amazon đến từ các luồng gợi ý). Nó giải quyết "nỗi đau" (pain-point) của khách hàng là sự quá tải thông tin (Information Overload), giúp họ tìm thấy sản phẩm mong muốn nhanh nhất.

### 4.2. Các phương pháp Gợi ý cốt lõi

Dựa trên các kỹ thuật Data Mining đã nghiên cứu, Hệ thống gợi ý được chia làm các hướng chính:

- **Lọc cộng tác (Collaborative Filtering):** \* _Nguyên lý:_ Dựa trên hành vi của một cộng đồng người dùng để gợi ý cho một người dùng cụ thể. Giả định rằng nếu User A và User B có chung sở thích trong quá khứ, họ sẽ có chung sở thích trong tương lai.
  - _Kỹ thuật:_ Sử dụng Ma trận Người dùng - Sản phẩm (User-Item Matrix) và tính toán khoảng cách/độ tương đồng (Ví dụ: Cosine Similarity, Pearson Correlation).
- **Lọc dựa trên nội dung (Content-Based Filtering):**
  - _Nguyên lý:_ Gợi ý các sản phẩm tương tự với những sản phẩm mà người dùng đã thích/mua trước đây, dựa trên thuộc tính của sản phẩm (danh mục, mô tả, giá cả).
  - _Kỹ thuật:_ Phân tích Vector đặc trưng của sản phẩm (thường kết hợp với Text Mining để trích xuất đặc trưng từ mô tả sản phẩm).
- **Hệ thống lai (Hybrid Recommender System):** Kết hợp cả hai phương pháp trên để khắc phục nhược điểm (như vấn đề "Cold-start" - Khởi động lạnh khi hệ thống chưa có dữ liệu về người dùng mới).

### 4.3. Đề xuất Hướng tiếp cận cho Ứng dụng Cuối kỳ của Nhóm

- **Dữ liệu:** Sử dụng bộ dữ liệu đánh giá sản phẩm (Product Reviews Dataset) từ Kaggle, thể hiện cả đặc tính Cross-sectional (ai mua gì) và Temporal (mua lúc nào).
- **Luồng xử lý:** Data Provisioning (Làm sạch Data bằng Pandas/PySpark) -> Data Mining (Xây dựng ma trận tương đồng Cosine Similarity) -> Xuất kết quả (Top N sản phẩm gợi ý).
- **Đánh giá:** Sử dụng các thang đo như RMSE (Root Mean Square Error) hoặc Precision/Recall để đo lường độ chính xác của thuật toán gợi ý so với dữ liệu thực tế.

**\[HẾT PHẦN BÁO CÁO LÝ THUYẾT\]**