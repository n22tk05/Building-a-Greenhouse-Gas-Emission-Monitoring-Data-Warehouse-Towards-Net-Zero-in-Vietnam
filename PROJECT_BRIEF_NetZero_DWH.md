# BẢN ĐỀ CƯƠNG DỰ ÁN (PROJECT BRIEF)
## ĐỀ TÀI: XÂY DỰNG DATA WAREHOUSE GIÁM SÁT PHÁT THẢI KHÍ NHÀ KÍNH HƯỚNG TỚI NET-ZERO TẠI VIỆT NAM

---

### 1. THÔNG TIN CHUNG (GENERAL INFORMATION)
* **Tên đề tài tiếng Việt:** Xây dựng Data Warehouse giám sát phát thải khí nhà kính hướng tới Net-Zero tại Việt Nam
* **Tên tiếng Anh (dự kiến):** Building a Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero in Vietnam
* **Loại hình đề tài:** Đồ án môn học / Khóa luận tốt nghiệp chuyên ngành Hệ thống Thông tin / Khoa học Dữ liệu
* **Hình thức thực hiện:** Cá nhân (Solo Project)
* **Thời gian dự kiến:** 4 tuần (1 tháng)
* **Tech Stack cốt lõi:**
  * **Hệ quản trị CSDL / Kho dữ liệu:** Microsoft SQL Server (Developer Edition) & SSMS
  * **Công cụ ETL chính:** SQL Server Integration Services (SSIS)
  * **Công cụ thu thập dữ liệu (Ingestion):** Python (`requests`, `pandas`, `SQLAlchemy`)
  * **Công cụ phân tích & Trực quan hóa (BI):** Microsoft Power BI Desktop

---

### 2. BỐI CẢNH & TÍNH CẤP THIẾT (BACKGROUND & SIGNIFICANCE)
* **Bối cảnh chính sách:** Việt Nam đã đưa ra cam kết mạnh mẽ đạt phát thải ròng bằng 0 (Net-Zero) vào năm 2050 tại COP26. Chính phủ đã ban hành khung pháp lý đồng bộ gồm **Nghị định 06/2022/NĐ-CP** và **Quyết định 01/2022/QĐ-TTg & 13/2024/QĐ-TTg** quy định các cơ sở phát thải lớn bắt buộc phải thực hiện kiểm kê khí nhà kính.
* **Vấn đề thực tế:** Dữ liệu về môi trường, phát thải năng lượng và các chỉ số kinh tế địa phương tại Việt Nam hiện đang bị phân mảnh, rời rạc giữa các bộ ngành (Tài nguyên Môi trường, Công Thương, Thống kê), không đồng nhất về chu kỳ thu thập (theo giờ của trạm đo vs theo năm của thống kê kinh tế).
* **Giải pháp đề xuất:** Xây dựng một **Kho dữ liệu (Data Warehouse)** tập trung theo phương pháp luận Kimball, tự động thu thập từ các nguồn uy tín quốc tế và quốc gia, làm sạch và mô hình hóa thành lược đồ hình sao (Star Schema). Từ đó, cung cấp nền tảng Business Intelligence giúp theo dõi, phân tích đa chiều và đưa ra cảnh báo sớm về tốc độ phát thải so với tăng trưởng kinh tế cho 63 tỉnh thành.

---

### 3. MỤC TIÊU DỰ ÁN (PROJECT OBJECTIVES)
1. **Mục tiêu kỹ thuật (Engineering):**
   * Xây dựng pipeline tự động thu thập dữ liệu phát thải và kinh tế từ các cổng API quốc tế mở và file thống kê quốc gia.
   * Thiết kế và triển khai tầng dữ liệu đệm (Staging Area) xử lý dữ liệu dị thể (JSON REST API, CSV/Excel).
   * Hiện thực hóa mô hình Star Schema trên Microsoft SQL Server với chuẩn thiết kế Kimball (Surrogate Keys, Conformed Dimensions, Fact Grain rõ ràng).
   * Đóng gói quy trình ETL tự động hóa hoàn toàn bằng SSIS (`.dtsx`).
2. **Mục tiêu phân tích & Nghiệp vụ (Analytics & Business Value):**
   * Xây dựng chỉ số **Decoupling Index** (Hệ số phân tách kinh tế - phát thải: Lượng CO2e phát thải trên mỗi tỷ đồng GRDP) cho từng tỉnh thành.
   * Xây dựng hệ thống cảnh báo sớm (Early Warning System) nhận diện các địa phương hoặc ngành kinh tế có nguy cơ vượt hạn ngạch phát thải.
   * Cung cấp Dashboard trực quan hóa tương tác 2 cấp độ trên Power BI phục vụ lãnh đạo và chuyên viên phân tích.

---

### 4. NGUỒN DỮ LIỆU ĐẦU VÀO (DATA SOURCES)

| STT | Tên nguồn | Đơn vị cung cấp | Định dạng | Nội dung dữ liệu chính |
| :---: | :--- | :--- | :---: | :--- |
| **1** | **World Bank Open Data API** | Ngân hàng Thế giới | REST JSON | Tổng phát thải khí nhà kính (`EN.ATM.GHGT.KT.CE`), CO2, Methane (CH4), tỷ lệ năng lượng tái tạo, tổng GDP Việt Nam từ 1990–nay. Không cần API key. |
| **2** | **ClimateWatch API** | World Resources Institute (WRI) | REST JSON | Phát thải khí nhà kính phân bổ theo từng lĩnh vực kinh tế: Năng lượng, Công nghiệp, Nông nghiệp, Giao thông vận tải, Rác thải. |
| **3** | **Niên giám Thống kê GSO** | Tổng cục Thống kê Việt Nam | CSV / Excel | Tổng sản phẩm trên địa bàn (GRDP), Dân số, Diện tích, Chỉ số sản xuất công nghiệp của 63 tỉnh thành qua các năm. |
| **4** | *(Bổ trợ)* **OpenAQ API** | Open Air Quality Org | REST JSON | Chỉ số đo nồng độ khí thải thực tế (`CO`, `NO2`, `SO2`, `PM2.5`) tại các trạm quan trắc mặt đất ở Hà Nội, TP.HCM, Đà Nẵng. |

---

### 5. THIẾT KẾ KIẾN TRÚC KHO DỮ LIỆU (DATA WAREHOUSE ARCHITECTURE)

#### A. Kiến trúc tổng thể 3 tầng
```
[Nguồn Dữ Liệu]                  [Tầng Staging]                   [Tầng Data Warehouse]              [Tầng Phân Tích]
• World Bank API      ──Python──>  stg_WorldBank_Emissions   ─SSIS─>  Dim_Date (Conformed)      ──Direct──>  Power BI Dashboard
• ClimateWatch API    ──Script──>  stg_ClimateWatch_Sectors   ──ETL──>  Dim_Province (Conformed)   ──Query──>  • Hero Map 63 Tỉnh
• GSO Statistics      ──Pandas──>  stg_GSO_Provinces         ──Load─>  Dim_Sector (Conformed)                 • Decoupling Matrix
                                                                       Fact_National_Emissions                • Early Warnings
                                                                       Fact_Provincial_Economy
```

#### B. Mô hình dữ liệu hình sao (Star Schema Design)
Kho dữ liệu được thiết kế gồm **2 bảng Fact** chia sẻ các **Dimension chuẩn tắc (Conformed Dimensions)**:

1. **Bảng Chiều (Dimension Tables):**
   * `Dim_Date`: `Date_Key (PK)`, `Year`, `Decade`, `Five_Year_Plan_Phase` (Kế hoạch 5 năm quốc gia).
   * `Dim_Province`: `Province_Key (PK)`, `Province_Code`, `Province_Name`, `Region` (Bắc/Trung/Nam), `Economic_Zone` (Vùng kinh tế trọng điểm), `Is_Industrial_Hub`.
   * `Dim_Sector`: `Sector_Key (PK)`, `Sector_Code`, `Sector_Name` (Năng lượng, Luyện kim, Xi măng, Nông nghiệp...), `Scope_Type` (Scope 1 / Scope 2).

2. **Bảng Sự kiện (Fact Tables):**
   * `Fact_National_Emissions`:
     * *Grain (Mức độ chi tiết):* 1 dòng đại diện cho lượng phát thải của 1 lĩnh vực trong 1 năm tại Việt Nam.
     * *Cột:* `Emission_ID (PK)`, `Date_Key (FK)`, `Sector_Key (FK)`, `Total_GHG_Kt`, `CO2_Kt`, `Methane_Kt`, `Renewable_Energy_Pct`.
   * `Fact_Provincial_Economy`:
     * *Grain (Mức độ chi tiết):* 1 dòng đại diện cho các chỉ số kinh tế và phát thải ước lượng của 1 tỉnh thành trong 1 năm.
     * *Cột:* `Economy_ID (PK)`, `Date_Key (FK)`, `Province_Key (FK)`, `GRDP_Billion_VND`, `Population`, `Industrial_Output_VND`, `Forest_Coverage_Pct`, `Estimated_Carbon_Tonnes`.

---

### 6. THIẾT KẾ GIAO DIỆN BÁO CÁO (POWER BI STORYBOARD)

* **Hero Visual (Điểm nhấn trang 1):** Bản đồ phân vùng nhiệt (Choropleth Map) 63 tỉnh thành Việt Nam (sử dụng file `vietnam_provinces.topojson`). Màu sắc thể hiện chỉ số **Decoupling Index** (Xanh lá: Kinh tế tăng trưởng xanh; Đỏ: Vùng báo động thâm dụng năng lượng và phát thải cao). Click vào tỉnh bất kỳ sẽ lọc chéo toàn bộ dữ liệu trên trang.
* **Bố cục 2 Trang báo cáo:**
  * **Trang 1 - Báo cáo Điều hành Quốc gia (Executive Overview):**
    * 4 Thẻ KPI: Tổng phát thải GHG quốc gia | Tăng trưởng GRDP | Tỷ lệ Năng lượng Tái tạo | Chỉ số Decoupling toàn quốc.
    * Biểu đồ đường kép (Dual-axis Line Chart): Tương quan xu hướng 20 năm giữa Phát thải CO2 vs Tăng trưởng GDP.
    * Biểu đồ Donut / Tree-Map: Cơ cấu phát thải theo ngành (Năng lượng, GTVT, Công nghiệp, Nông nghiệp).
  * **Trang 2 - Phân tích Chi tiết Tỉnh & Cảnh báo Sớm (Provincial Drill-down & Warnings):**
    * Bộ lọc dropdown chọn Tỉnh thành.
    * Đồng hồ đo cảnh báo (Gauge Chart): Mức độ phát thải thực tế so với Hạn ngạch mục tiêu Net-Zero 2030 của tỉnh.
    * Biểu đồ ma trận 4 góc phần tư (Growth vs Carbon Intensity Scatter Plot): Phân nhóm tỉnh thành (Nhóm tiên phong xanh vs Nhóm rủi ro chuyển dịch).
    * Thẻ diễn giải tự động (Smart Narrative): Gợi ý hành động chính sách tương ứng cho tỉnh được chọn.

---

### 7. KẾ HOẠCH TRIỂN KHAI 4 TUẦN (4-WEEK ROADMAP)

| Tuần | Giai đoạn | Nhiệm vụ kỹ thuật cụ thể | Sản phẩm bàn giao (Deliverables) |
| :---: | :--- | :--- | :--- |
| **Tuần 1** | **Thu thập & Chuẩn hóa Dữ liệu** | • Viết script Python `fetch_data.py` gọi API World Bank & ClimateWatch.<br>• Tải và làm sạch dữ liệu niên giám thống kê 63 tỉnh thành từ GSO.<br>• Xuất 3 tập file sạch định dạng CSV đặt tại thư mục `data/raw/`. | 3 file dữ liệu nguồn sạch (`emissions_wb.csv`, `sectors_cw.csv`, `provinces_gso.csv`). |
| **Tuần 2** | **Thiết kế DWH & Cài đặt SQL Server** | • Cài đặt SQL Server & SSMS.<br>• Tạo Database `NetZero_VN_DWH`.<br>• Viết và thực thi file script DDL tạo cấu trúc bảng Staging và các bảng Fact/Dim Star Schema (PK, FK, Indexes). | File script SQL `01_create_schema.sql` chạy hoàn chỉnh không lỗi trên SQL Server. |
| **Tuần 3** | **Xây dựng Pipeline ETL (SSIS)** | • Khởi tạo Visual Studio SSIS Project `NetZero_ETL`.<br>• Dựng luồng Control Flow (chạy script Python $\rightarrow$ Truncate Staging $\rightarrow$ Data Flow nạp file CSV).<br>• Thiết lập biến đổi (Transformations): Chuẩn hóa tên tiếng Việt, tra cứu Surrogate Key (`Lookup`), xử lý NULL.<br>• Nạp dữ liệu vào Fact và Dimension Tables. | Package SSIS `Master_ETL.dtsx` thực thi trơn tru từ đầu đến cuối. |
| **Tuần 4** | **Trực quan hóa Power BI & Báo cáo** | • Kết nối Power BI với SQL Server.<br>• Nạp file bản đồ TopoJSON 63 tỉnh thành Việt Nam.<br>• Viết các công thức DAX tính toán chỉ số.<br>• Thiết kế 2 trang Dashboard hoàn chỉnh.<br>• Soạn thảo báo cáo thuyết minh đồ án Word & Slides thuyết trình. | File báo cáo `NetZero_Dashboard.pbix` + Báo cáo thuyết minh đồ án 5 chương hoàn thiện. |

---

### 8. TIÊU CHÍ ĐÁNH GIÁ & ĐIỂM CỘNG HỌC THUẬT (EVALUATION CRITERIA)
* **Tính thời sự và giá trị thực tiễn:** Bám sát cam kết Net-Zero 2050 và các văn bản quy phạm pháp luật của Chính phủ Việt Nam.
* **Chuẩn mực kỹ thuật DWH:** Áp dụng đúng phương pháp luận Kimball (Bus Matrix, Star Schema, Surrogate Key, Grain declaration).
* **Khả năng tự động hóa:** Pipeline có khả năng chạy lại định kỳ (reproducible) từ khâu gọi API đến cập nhật Dashboard mà không cần can thiệp thủ công.
* **Mức độ hoàn thiện trực quan:** Dashboard chuyên nghiệp, có Hero Visual ấn tượng, tư duy UX/UI mạch lạc phục vụ trực tiếp việc ra quyết định.
