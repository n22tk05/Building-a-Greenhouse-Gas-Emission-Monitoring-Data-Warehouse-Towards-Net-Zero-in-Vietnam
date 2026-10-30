# SLIDE THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN TỐT NGHIỆP

**ĐỀ TÀI:**  
## HỆ THỐNG GIÁM SÁT PHÁT THẢI KHÍ NHÀ KÍNH HƯỚNG TỚI NET-ZERO TẠI VIỆT NAM  
*(VIETNAM GREENHOUSE GAS EMISSION MONITORING DATA WAREHOUSE TOWARDS NET-ZERO)*

---

### Slide 1: Trang Tiêu Đề (Title Slide)
* **Tên đề tài:** Hệ Thống Giám Sát Phát Thải Khí Nhà Kính Hướng Tới Net-Zero Tại Việt Nam
* **Cơ sở dữ liệu:** `NetZero_VN_DWH` trên Microsoft SQL Server 2022
* **Nhóm sinh viên thực hiện (5 thành viên):**
  - Nguyễn Tuấn Khánh (Trưởng nhóm / Data Architect)
  - Võ Quốc Anh (Data Cleansing & QA Engineer)
  - Hà Trần Bảo Trân (ETL Pipeline Engineer)
  - Võ Văn Nhân (Big Data & Performance Engineer)
  - Lê Trần Đoan Trang (BI Developer & Data Analyst)
* **Speaker Notes:** Kính chào quý thầy cô Hội đồng chấm đồ án tốt nghiệp. Hôm nay nhóm chúng em xin phép được trình bày đề tài nghiên cứu và xây dựng hệ thống kho dữ liệu giám sát phát thải khí nhà kính hướng tới mục tiêu Net-Zero 2050 tại Việt Nam.

---

### Slide 2: Bối Cảnh Nghiên Cứu & Tính Cấp Thiết (Problem Statement)
* **Cam kết Quốc tế:** Việt Nam cam kết đạt phát thải ròng bằng 0 (**Net-Zero**) vào năm 2050 tại COP26.
* **Khung Pháp lý:** Nghị định 06/2022/NĐ-CP và Quyết định 13/2024/QĐ-TTg bắt buộc 2.166 cơ sở phải kiểm kê khí nhà kính.
* **Rào cản Dữ liệu Hiện tại:**
  - Dữ liệu bị **phân mảnh** giữa các bộ ngành (Bộ TN&MT, Bộ Công Thương, GSO).
  - Thiếu nhất quán về mức độ chi tiết: Số liệu kinh tế tính theo năm, dữ liệu trạm quan trắc đo theo giờ.
  - Áp lực từ Cơ chế điều chỉnh biên giới carbon (**CBAM**) đe dọa các ngành xuất khẩu chủ lực (thép, xi măng, nhôm).
* **Speaker Notes:** Dữ liệu môi trường và kinh tế tại Việt Nam hiện đang nằm rời rạc trong các file silo. Nếu không có một nền tảng dữ liệu tập trung, các nhà hoạch định chính sách sẽ không thể theo dõi tiến độ cam kết cũng như đánh giá rủi ro kinh tế của các địa phương.

---

### Slide 3: Mục Tiêu & Giải Pháp Đề Xuất (Objectives & Solution)
* **Mục tiêu tổng quát:** Xây dựng một Kho dữ liệu (DWH) tập trung theo chuẩn quốc tế và nền tảng Báo cáo thông minh (BI) hỗ trợ quản lý môi trường - kinh tế xanh 63 tỉnh thành.
* **4 Trụ cột Kỹ thuật Chính:**
  1. Mô hình hóa đa chiều chuẩn **Ralph Kimball (Star Schema)**.
  2. Đường ống ETL tự động hóa trên **SSIS** có bảo vệ chống tính trùng GDP.
  3. Mở rộng Big Data **1.66 triệu dòng** với công nghệ **Clustered Columnstore Index (CCI)**.
  4. Hệ thống Báo cáo Điều hành **Power BI** với bản đồ phân vùng số **TopoJSON 63 tỉnh thành**.
* **Speaker Notes:** Đồ án không chỉ dừng lại ở bài toán trích xuất dữ liệu thông thường, mà tích hợp cả tầng vĩ mô nhiều năm và tầng vi mô dữ liệu lớn Big Data phục vụ phân tích thời gian thực.

---

### Slide 4: Kiến Trúc Hệ Thống 3 Tầng (3-Tier DWH Architecture)
* **Sơ đồ luồng dữ liệu:**
  - **Tầng Nguồn (Raw):** World Bank API, Climate Watch (1970–2023), Tổng cục Thống kê GSO, 189 Trạm quan trắc không khí.
  - **Tầng Đệm (Staging):** Schema `staging` chứa dữ liệu trung gian, bảng kiểm toán `ETL_Audit_Log`.
  - **Tầng Kho Dữ Liệu (dwh):** Schema `dwh` chứa Star Schema, 5 Dimensions, 3 Fact Tables, lập chỉ mục Columnstore Index.
  - **Tầng Ngữ Nghĩa & Ứng Dụng (BI Layer):** 8 SQL Semantic Views, 35 DAX Measures, Power BI Dashboards.
* **Speaker Notes:** Kiến trúc 3 tầng đảm bảo tính độc lập giữa hệ thống nguồn và kho dữ liệu, cho phép nạp bù và truy vết dữ liệu an toàn.

---

### Slide 5: Mô Hình Chiều Chuẩn Ralph Kimball (Star Schema ERD)
* **Bảng Sự Kiện (Fact Tables):**
  - `Fact_National_Emissions` (510 dòng): Phát thải CO2, CH4, Năng lượng tái tạo cấp quốc gia.
  - `Fact_Provincial_Economy` (630 dòng): GRDP, Dân số, Che phủ rừng, Carbon ước lượng 63 tỉnh.
  - `Fact_Hourly_Air_Monitoring` (**1.660.176 dòng**): AQI, PM2.5, SO2, NO2 hàng giờ năm 2024.
* **Chiều Chuẩn Hóa Dùng Chung (Conformed Dimensions):**
  - `Dim_Date`: 81 năm (1970–2050), mốc chính sách Đổi Mới và Net-Zero.
  - `Dim_Province`: 63 tỉnh thành chuẩn GSO, mã số 2 ký tự.
  - `Dim_Sector`: 9 phân ngành chuẩn IPCC.
  - `Dim_Station` (189 trạm) & `Dim_Time_Of_Day` (24 giờ).
* **Speaker Notes:** Việc áp dụng Conformed Dimensions là chìa khóa để liên kết chéo giữa dữ liệu kinh tế và dữ liệu phát thải môi trường trên cùng một trục thời gian và địa lý.

---

### Slide 6: Xử Lý ETL & Cơ Chế Kiểm Soát Lỗi (Data Engineering)
* **Công cụ:** Visual Studio SSIS Solution (`NetZero_ETL.sln`) gồm 4 gói tự động.
* **Kỹ thuật nạp SCD Type 1 MERGE:** Đảm bảo tính Idempotent (chạy lại bao nhiêu lần cũng không sinh dữ liệu rác).
* **GDP Overcounting Guard (Bảo vệ kép chống nhân đôi GDP):**
  - Giải quyết bài toán kinh điển: GDP chỉ thuộc về cấp quốc gia (`Sector_Code = 'TOT'`), khi phân tích theo 9 phân ngành con, GDP được gán `NULL` để tránh việc tính tổng bị nhân lên 9 lần.
* **Ghi log kiểm toán (`staging.ETL_Audit_Log`):** Ghi nhận chi tiết thời gian bắt đầu, kết thúc, số dòng xử lý và mã lỗi.
* **Speaker Notes:** Chúng em đặc biệt chú trọng tính toán vẹn dữ liệu, xây dựng cơ chế Overcounting Guard ở cả tầng SQL View và tầng DAX.

---

### Slide 7: Tối Ưu Hóa Dữ Liệu Lớn Với Columnstore Index (Big Data Performance)
* **Quy mô:** Bảng `Fact_Hourly_Air_Monitoring` chứa **1.660.176 bản ghi** (189 trạm $\times$ 8.784 giờ năm 2024).
* **Kỹ thuật Nạp Khối (.NET SqlBulkCopy):** Nạp toàn bộ 1.66M dòng chỉ trong **173 giây** (~9.600 dòng/giây).
* **Hiệu Năng Clustered Columnstore Index (CCI):**
  - **Tỷ lệ nén dung lượng:** Nén từ 128.04 MB xuống **24.81 MB (giảm 81% dung lượng đĩa)**.
  - **Tốc độ truy vấn phân tích:** Phép tính Aggregate 4 bảng JOIN trên 1.66M dòng thực thi chỉ trong **0.08 giây (< 100ms)**.
* **Speaker Notes:** Nhờ công nghệ Columnstore Index, chúng em chứng minh được cơ sở dữ liệu hoàn toàn đáp ứng tiêu chuẩn thời gian thực cho các báo cáo phân tích Big Data.

---

### Slide 8: Bản Đồ Địa Lý Số TopoJSON 63 Tỉnh Thành Việt Nam
* **Tệp không gian số:** `vietnam_provinces.topojson` (Dung lượng siêu nhẹ: **150.30 KB**).
* **Đặc tính kỹ thuật:**
  - Chuẩn hóa cấu trúc đa lớp (`vietnam_provinces` & `provinces`).
  - Khớp nối **100% (63/63 tỉnh thành)** theo mã `Province_Code` ('01' đến '96') và tên tiếng Việt Unicode.
  - Tương thích hoàn hảo với visual **Shape Map (Preview)** trong Microsoft Power BI Desktop.
  - Thời gian kết xuất bản đồ trên Dashboard: **< 0.2 giây**.
* **Speaker Notes:** Việc chuẩn hóa tệp TopoJSON 150 KB giúp visual bản đồ trong Power BI hiển thị tức thì toàn bộ ranh giới dải đất chữ S của Việt Nam mà không hề có độ trễ.

---

### Slide 9: Thư Viện Độ Đo Phân Tích DAX Measures
* **Quy mô:** **35 công thức DAX chuyên sâu** được tổ chức khoa học trong bảng `_Measures`.
* **6 Nhóm Nghiệp Vụ Chính:**
  1. Phát thải quốc gia & GDP sạch (có Overcounting Guard).
  2. Kinh tế & Tách rời tỉnh thành (Hệ số Tapio Decoupling).
  3. Giám sát không khí Big Data 2024 (AQI, PM2.5, Giờ vượt chuẩn QCVN).
  4. Chuỗi thời gian Time Intelligence (YoY Growth %, 5-Year CAGR %).
  5. Lộ trình Net-Zero 2030 (Khoảng cách NDC Gap, Hạn ngạch Quota phân bổ).
  6. Trực quan hóa động (Mã màu Hex động: `#10B981` Xanh / `#F59E0B` Vàng / `#EF4444` Đỏ).
* **Speaker Notes:** 100% các công thức DAX sử dụng hàm `DIVIDE(..., BLANK())` để triệt tiêu lỗi chia cho 0 và hỗ trợ định dạng màu sắc có điều kiện tự động.

---

### Slide 10: Demo Dashboard Trang 1 - Báo Cáo Điều Hành Quốc Gia (Executive Overview)
* **Bố cục giao diện:** Thiết kế theo chuẩn giao diện Net-Zero Emerald Nền tối (Dark Slate `#0F172A`).
* **Các thành phần trực quan:**
  - **Dải 4 Thẻ KPI:** Tổng GHG (384.2 MtCO2e), GDP ($430B), Năng lượng tái tạo (32.4%), Khoảng cách NDC 2030 (+167.3 MtCO2e).
  - **Hero Shape Map 63 tỉnh:** Phân tầng màu theo Chỉ số Tách rời Kinh tế - Carbon (Tapio Index).
  - **Biểu đồ Đường kép Dual-Axis (1990–2024):** Tương quan giữa tăng trưởng GDP và phát thải khí nhà kính.
  - **Biểu đồ Phân rã Ngành:** Tỷ trọng phát thải 9 ngành IPCC (Năng lượng chiếm 48%, Công nghiệp 24%, Nông nghiệp 18%).
* **Speaker Notes:** Trang 1 giúp các nhà lãnh đạo nắm bắt ngay bức tranh tổng thể: Việt Nam tăng trưởng kinh tế nhanh nhưng tốc độ phát thải vẫn đang tăng, đòi hỏi chính sách chuyển dịch năng lượng quyết liệt để đạt mốc NDC 2030.

---

### Slide 11: Demo Dashboard Trang 2 - Phân Tích Chi Tiết Tỉnh & Cảnh Báo Sớm
* **Các tính năng nổi bật:**
  - **Thanh lọc phân cấp:** Lọc theo Vùng kinh tế trọng điểm $\rightarrow$ Miền $\rightarrow$ Từng Tỉnh cụ thể.
  - **Đồng hồ cảnh báo hạn ngạch 2030 (Gauge Chart):** Kim đo tự động chuyển sang màu Đỏ khi địa phương có lượng phát thải vượt trần hạn ngạch phân bổ.
  - **Ma trận 4 góc phần tư (Scatter Plot Tapio):** Phân nhóm 63 tỉnh thành thành 4 phân khúc (Tiên phong xanh, Mở rộng thâm dụng, Bảo tồn sinh thái, Nguy cơ cảnh báo đỏ).
  - **Giám sát vi mô Big Data 2024:** So sánh số giờ ô nhiễm giữa Giờ cao điểm giao thông và Giờ thường tại từng trạm quan trắc địa phương.
* **Speaker Notes:** Trang 2 cung cấp công cụ giám sát vi mô đến từng trạm đo và từng địa phương, hỗ trợ việc cảnh báo sớm và phân bổ hạn ngạch tín chỉ carbon trong tương lai.

---

### Slide 12: Phát Hiện Nghiệp Vụ Nổi Bật (Key Business Insights)
1. **Nghịch lý Đô thị Lớn:** Hà Nội và TP.HCM có GRDP bình quân đầu người cao nhưng số giờ ô nhiễm bụi mịn PM2.5 vượt chuẩn QCVN 05:2023 cao gấp 3–5 lần vùng nông thôn.
2. **Điểm nóng Xả thải Công nghiệp:** Các tỉnh trọng điểm công nghiệp (Bắc Ninh, Hải Dương, Quảng Ninh, Đồng Nai) có cường độ carbon cao, đối mặt với nguy cơ bị áp thuế biên giới carbon **CBAM** khi xuất khẩu sang châu Âu.
3. **Giá trị Lá chắn Xanh:** Các tỉnh duy trì tỷ lệ che phủ rừng > 50% (Lâm Đồng, Tuyên Quang, Quảng Nam) có chỉ số tách rời Tapio rất tốt (Strong Decoupling), giữ được chất lượng không khí trong lành quanh năm.
* **Speaker Notes:** Đây là những bằng chứng số liệu định lượng xác thực, chứng minh giá trị thực tiễn to lớn mà kho dữ liệu mang lại cho công tác hoạch định chính sách.

---

### Slide 13: Đảm Bảo Chất Lượng & Kiểm Thử Tự Động (Quality Assurance)
* **Quy trình Kiểm định 4 Cấp độ:**
  1. *Cấp dữ liệu nguồn:* Data Profiling Gate (khử trùng lặp, chuẩn hóa tiếng Việt, kiểm tra NULL < 5%).
  2. *Cấp mô hình DDL:* Kiểm tra tính toàn vẹn khóa chính, khóa ngoại, ràng buộc CHECK trên SQL Server.
  3. *Cấp đường ống ETL:* Kiểm tra tính toàn vẹn file cấu hình SSIS XML.
  4. *Cấp ứng dụng BI:* Kiểm tra tính toán vẹn của Views ngữ nghĩa, công thức DAX và TopoJSON.
* **Kết quả Kiểm thử Tự Động:** **64/64 test cases ALL PASS 100%**.
* **Speaker Notes:** Toàn bộ hệ thống được bảo vệ bởi bộ test suite tự động 64 ca kiểm thử, đảm bảo không có bất kỳ lỗi hồi quy nào trong suốt quá trình phát triển.

---

### Slide 14: Phân Công Nhiệm Vụ 5 Thành Viên & Tiến Độ Dự Án
| Thành viên | Vai trò | Trọng tâm Kỹ thuật Đóng góp |
| :--- | :--- | :--- |
| **Nguyễn Tuấn Khánh** | Trưởng nhóm / Data Architect | Thiết kế Star Schema, Bus Matrix, DDL CSDL, Điều phối dự án |
| **Võ Quốc Anh** | Data Cleansing & QA Engineer | Thu thập data WB/CW/GSO, làm sạch tiếng Việt, Data Profiling Gate |
| **Hà Trần Bảo Trân** | ETL Pipeline Engineer | Xây dựng 4 gói SSIS, Staging Load, cơ chế MERGE & Audit Log |
| **Võ Văn Nhân** | Big Data & Performance Engineer | Nạp khối 1.66M dòng SqlBulkCopy, Clustered Columnstore Index |
| **Lê Trần Đoan Trang** | BI Developer & Data Analyst | Xây dựng 35 DAX Measures, TopoJSON Map, 2 trang Power BI Dashboard |
* **Speaker Notes:** Cả 5 thành viên trong nhóm đều phụ trách những phân hệ kỹ thuật chuyên sâu và phối hợp chặt chẽ để hoàn thành đúng tiến độ đề ra.

---

### Slide 15: Kết Luận & Hướng Phát Triển Tương Lai (Conclusion & Future Work)
* **Kết luận:** Đồ án đã hiện thực hóa thành công một Kho dữ liệu giám sát phát thải khí nhà kính toàn diện, hiện đại, tối ưu hóa Big Data và cung cấp các báo cáo phân tích trực quan sâu sắc.
* **Hướng phát triển tiếp theo:**
  - Tích hợp thêm ảnh viễn thám vệ tinh (Copernicus Sentinel-5P) đo nồng độ khí nhà kính từ không gian.
  - Xây dựng mô hình học máy (Machine Learning / Prophet / LSTM) dự báo chuỗi thời gian phát thải đến năm 2050.
* **Lời cảm ơn:** Nhóm chúng em xin trân trọng cảm ơn Quý Thầy Cô trong Hội đồng đã lắng nghe và kính mong nhận được những ý kiến đóng góp quý báu!
