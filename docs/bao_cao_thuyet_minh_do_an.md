# BÁO CÁO THUYẾT MINH ĐỒ ÁN TỐT NGHIỆP

**ĐỀ TÀI:**  
# HỆ THỐNG GIÁM SÁT PHÁT THẢI KHÍ NHÀ KÍNH HƯỚNG TỚI NET-ZERO TẠI VIỆT NAM  
*(VIETNAM GREENHOUSE GAS EMISSION MONITORING DATA WAREHOUSE TOWARDS NET-ZERO)*

---

**Chuyên ngành:** Kỹ Thuật Dữ Liệu & Hệ Thống Thông Tin Quản Lý  
**Mã số CSDL:** `NetZero_VN_DWH`  
**Nhóm tác giả (5 thành viên):**  
1. **Nguyễn Tuấn Khánh** - Trưởng nhóm / Kiến trúc sư Kho dữ liệu (Data Architect)  
2. **Võ Quốc Anh** - Kỹ sư Xử lý & Kiểm định Dữ liệu nguồn (Data Cleansing & QA)  
3. **Hà Trần Bảo Trân** - Kỹ sư Đường ống ETL & Tự động hóa (ETL Pipeline Engineer)  
4. **Võ Văn Nhân** - Kỹ sư Dữ liệu lớn & Hiệu năng Cơ sở dữ liệu (Big Data & Performance Engineer)  
5. **Lê Trần Đoan Trang** - Chuyên viên Phân tích BI & Trực quan hóa (BI Developer & Data Analyst)  

---

## TÓM TẮT ĐỒ ÁN (ABSTRACT)

### Tóm tắt tiếng Việt:
Biến đổi khí hậu toàn cầu đang đặt ra thách thức sống còn đối với sự phát triển bền vững của Việt Nam. Tại Hội nghị Thượng đỉnh COP26, Việt Nam đã đưa ra cam kết lịch sử đạt mức phát thải ròng bằng 0 (Net-Zero) vào năm 2050. Để hiện thực hóa mục tiêu này, Chính phủ đã ban hành hệ thống khung pháp lý đồng bộ (Nghị định 06/2022/NĐ-CP, Quyết định 01/2022/QĐ-TTg và Quyết định 13/2024/QĐ-TTg) bắt buộc các cơ sở thâm dụng năng lượng phải kiểm kê khí nhà kính. Tuy nhiên, rào cản lớn nhất hiện nay là tình trạng **dữ liệu bị phân mảnh, rời rạc giữa các bộ ngành**, thiếu nhất quán về mức độ chi tiết (Grain) và không có nền tảng phân tích tập trung.

Đồ án này đã thiết kế và xây dựng thành công một **Kho dữ liệu (Data Warehouse - DWH) đa chiều chuẩn công nghiệp** dựa trên phương pháp luận kinh điển của **Ralph Kimball**. Hệ thống tích hợp dữ liệu vĩ mô nhiều năm từ World Bank, Climate Watch, Tổng cục Thống kê (GSO) và mở rộng tầng dữ liệu lớn vi mô với **1.66 triệu dòng** bản ghi quan trắc không khí hàng giờ năm 2024. Bằng việc áp dụng kỹ thuật chỉ mục dạng cột **Clustered Columnstore Index (CCI)**, dung lượng lưu trữ được nén giảm hơn **81%** (từ 128 MB xuống 24.8 MB) và tốc độ thực thi các câu truy vấn tổng hợp đạt dưới **0.1 giây (< 100ms)**. Đường ống ETL tự động hóa trên **SSIS** tích hợp cơ chế nạp bù an toàn (Idempotent MERGE), chống nhân đôi GDP (Overcounting Guard) và kiểm toán kiểm soát lỗi (`ETL_Audit_Log`). Trên tầng ứng dụng, hệ sinh thái báo cáo thông minh **Microsoft Power BI** cung cấp 2 trang Dashboard điều hành với bản đồ phân vùng số **TopoJSON 63 tỉnh thành** và thư viện **35 công thức DAX chuyên sâu**, hỗ trợ đắc lực cho việc giám sát hạn ngạch carbon, phân loại mô hình tách rời kinh tế (Tapio Decoupling) và cảnh báo nguy cơ rào cản thuế biên giới carbon (CBAM).

### English Abstract:
Global climate change presents a critical challenge to Vietnam's sustainable socioeconomic development. At the COP26 Summit, Vietnam pledged to achieve Net-Zero greenhouse gas emissions by 2050, followed by concrete national policy frameworks (Decree 06/2022/ND-CP, Decision 01/2022/QD-TTg, and Decision 13/2024/QD-TTg). Nevertheless, decision-makers face fragmented datasets dispersed across disparate ministries, conflicting time granularities, and a lack of unified analytics infrastructure.

This capstone project engineers an enterprise-grade multi-grain Data Warehouse (`NetZero_VN_DWH`) adhering strictly to the **Ralph Kimball dimensional modeling methodology**. The architecture ingests historical macroeconomic and national emissions data from the World Bank, Climate Watch, and the General Statistics Office (GSO), augmented with a micro-level big data fact table comprising **1.66 million rows** of hourly air quality monitoring across 189 stations in 2024. Leveraging **Clustered Columnstore Indexing (CCI)**, the physical footprint was compressed by **81%** (from 128 MB down to 24.8 MB), sustaining sub-100ms analytical aggregation latency. Automated **SSIS ETL pipelines** ensure idempotent incremental loading, GDP overcounting defense, and end-to-end auditability. The analytical presentation layer delivers an interactive, two-page **Power BI dashboard** powered by a tailored 63-province **TopoJSON shape map** and a 35-measure DAX engine, effectively quantifying Tapio decoupling elasticity, carbon intensity, and provincial NDC 2030 quota fulfillment.

---

## DANH MỤC TỪ VIẾT TẮT & THUẬT NGỮ
| Thuật ngữ | Tên tiếng Anh đầy đủ | Giải thích nghĩa tiếng Việt |
| :--- | :--- | :--- |
| **DWH** | Data Warehouse | Kho dữ liệu tập trung phục vụ phân tích OLAP |
| **ETL** | Extract, Transform, Load | Quy trình trích xuất, biến đổi và nạp dữ liệu |
| **SSIS** | SQL Server Integration Services | Nền tảng xây dựng đường ống dữ liệu của Microsoft |
| **DAX** | Data Analysis Expressions | Ngôn ngữ công thức đo lường phân tích trong Power BI |
| **GHG** | Greenhouse Gas | Khí nhà kính (CO2, CH4, N2O, F-gases) |
| **NDC** | Nationally Determined Contributions | Đóng góp do quốc gia tự quyết định trong Thỏa thuận Paris |
| **CBAM** | Carbon Border Adjustment Mechanism | Cơ chế điều chỉnh biên giới carbon của Liên minh Châu Âu |
| **CCI** | Clustered Columnstore Index | Chỉ mục lưu trữ dạng cột cụm tối ưu hóa Big Data |
| **GRDP** | Gross Regional Domestic Product | Tổng sản phẩm trên địa bàn cấp tỉnh thành |
| **QCVN** | Quy chuẩn Kỹ thuật Quốc gia | Tiêu chuẩn chất lượng môi trường không khí của Việt Nam |

---

# CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI & BỐI CẢNH NGHIÊN CỨU

### 1.1. Bối cảnh Quốc tế và Cam kết Net-Zero của Việt Nam
Tại Hội nghị lần thứ 26 các bên tham gia Công ước khung của Liên Hợp Quốc về Biến đổi Khí hậu (COP26) diễn ra tại Glasgow (Vương quốc Anh), Thủ tướng Chính phủ Phạm Minh Chính đã long trọng tuyên bố Việt Nam cam kết đạt mức phát thải ròng bằng 0 (**Net-Zero**) vào năm 2050. Đây là bước ngoặt lịch sử khẳng định vị thế và trách nhiệm quốc tế của Việt Nam trong công cuộc ứng phó với biến đổi khí hậu toàn cầu. 

Để cụ thể hóa cam kết này, Chính phủ đã xây dựng hành lang pháp lý nghiêm ngặt:
* **Nghị định 06/2022/NĐ-CP:** Quy định giảm nhẹ phát thải khí nhà kính và bảo vệ tầng ozon; đặt lộ trình vận hành thị trường tín chỉ carbon trong nước từ năm 2028.
* **Quyết định 01/2022/QĐ-TTg & Quyết định 13/2024/QĐ-TTg:** Ban hành danh mục 2.166 cơ sở phát thải khí nhà kính lớn bắt buộc phải thực hiện kiểm kê khí nhà kính định kỳ.

### 1.2. Vấn đề Thực tế (Problem Statement)
Mặc dù quyết tâm chính trị rất cao, việc quản lý và hoạch định chính sách gặp phải những rào cản kỹ thuật nghiêm trọng:
1. **Dữ liệu phân mảnh:** Dữ liệu phát thải do Bộ TN&MT quản lý, số liệu tiêu thụ năng lượng thuộc Bộ Công Thương, trong khi số liệu kinh tế - dân số do Tổng cục Thống kê (Bộ KH&ĐT) nắm giữ.
2. **Xung đột chu kỳ và độ chi tiết (Grain Mismatch):** Số liệu kinh tế được tổng hợp theo năm (Annual), trong khi dữ liệu quan trắc trạm đo môi trường phát sinh theo từng giờ (Hourly).
3. **Nguy cơ thuế carbon CBAM:** Các đối tác thương mại lớn (EU, Mỹ) bắt đầu áp thuế carbon lên hàng xuất khẩu Việt Nam (thép, xi măng, nhôm, phân bón). Nếu địa phương không kiểm soát được cường độ phát thải, năng lực cạnh tranh quốc gia sẽ bị suy giảm nghiêm trọng.

### 1.3. Mục tiêu và Phạm vi Đề tài
* **Mục tiêu tổng quát:** Xây dựng hệ thống Kho dữ liệu tập trung và Báo cáo điều hành thông minh phục vụ giám sát, phân tích đa chiều phát thải khí nhà kính gắn với tăng trưởng kinh tế 63 tỉnh thành Việt Nam.
* **Mục tiêu cụ thể:**
  - Thiết kế Star Schema chuẩn Kimball với các chiều chuẩn hóa (Conformed Dimensions).
  - Tích hợp pipeline ETL tự động hóa có cơ chế kiểm định chất lượng (Data Profiling).
  - Tối ưu hóa Big Data với quy mô **1.66 triệu dòng** sử dụng Clustered Columnstore Index.
  - Xây dựng 2 trang Dashboard trực quan hóa trên Power BI với bản đồ TopoJSON 63 tỉnh thành.
* **Phạm vi nghiên cứu:** 63 tỉnh thành Việt Nam; chuỗi thời gian vĩ mô 1970–2023; dữ liệu vi mô hàng giờ năm 2024; mốc định hướng chiến lược 2030 (NDC) và 2050 (Net-Zero).

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & PHƯƠNG PHÁP LUẬN

### 2.1. Phương Pháp Luận Thiết Kế Kho Dữ Liệu Kimball
Đồ án áp dụng triệt để phương pháp luận thiết kế chiều của **Ralph Kimball** thông qua 4 bước:
1. **Chọn quy trình nghiệp vụ (Select the Business Process):** Lựa chọn 3 quy trình cốt lõi gồm: Quản lý phát thải quốc gia theo ngành, Giám sát kinh tế - sinh thái địa phương, và Quan trắc ô nhiễm không khí hàng giờ.
2. **Xác định mức độ chi tiết (Declare the Grain):** 
   - Vĩ mô: 1 dòng cho 1 ngành, 1 năm; 1 dòng cho 1 tỉnh, 1 năm.
   - Vi mô (Big Data): 1 dòng cho 1 trạm quan trắc, trong 1 giờ nhất định năm 2024.
3. **Xác định các chiều phân tích (Identify Dimensions):** Thời gian (`Dim_Date`, `Dim_Time_Of_Day`), Địa lý (`Dim_Province`, `Dim_Station`), Lĩnh vực kinh tế (`Dim_Sector`).
4. **Xác định các chỉ số đo lường (Identify Facts):** Khối lượng phát thải CO2/CH4, Tỷ lệ năng lượng tái tạo, GRDP, Dân số, Diện tích rừng, AQI, Nồng độ bụi mịn PM2.5.

### 2.2. Mô Hình Phân Tách Kinh Tế - Môi Trường Tapio (Decoupling Model)
Để đánh giá liệu một tỉnh tăng trưởng kinh tế có làm gia tăng ô nhiễm hay không, đồ án ứng dụng mô hình hệ số co giãn Tapio ($e$):
$$e = \frac{\% \Delta \text{Emissions}}{\% \Delta \text{GRDP}} = \frac{(\text{Emissions}_t - \text{Emissions}_{t-1}) / \text{Emissions}_{t-1}}{(\text{GRDP}_t - \text{GRDP}_{t-1}) / \text{GRDP}_{t-1}}$$
* **$e < 0$ (Tách rời mạnh - Strong Decoupling):** GRDP tăng nhưng phát thải giảm tuyệt đối $\rightarrow$ Mục tiêu lý tưởng của Kinh tế Xanh.
* **$0 \le e \le 0.8$ (Tách rời yếu - Weak Decoupling):** Cả hai đều tăng nhưng phát thải tăng chậm hơn kinh tế.
* **$e > 1.2$ (Thâm dụng carbon - Negative Decoupling):** Tốc độ phát thải tăng nhanh hơn tốc độ tăng trưởng kinh tế $\rightarrow$ Nguy cơ ô nhiễm báo động.

### 2.3. Công Nghệ Clustered Columnstore Index (CCI)
Khác với bảng truyền thống lưu trữ dạng dòng (Rowstore/B-Tree), Columnstore lưu trữ vật lý từng cột riêng biệt theo các khối dữ liệu (Rowgroups ~ 1 triệu dòng). Nhờ vậy, hệ thống đạt được:
- **Tỷ lệ nén cao:** Áp dụng thuật toán nén từ điển (Dictionary Encoding) và nén bit, giảm dung lượng từ 3-5 lần.
- **Loại trừ phân đoạn (Segment Elimination):** Khi người dùng truy vấn theo một năm hoặc một trạm, SQL Server chỉ nạp các phân đoạn dữ liệu cần thiết, loại bỏ hoàn toàn việc đọc bảng toàn diện (Full Table Scan).

---

# CHƯƠNG 3: KIẾN TRÚC KHO DỮ LIỆU & THIẾT KẾ MÔ HÌNH SAO

### 3.1. Kiến Trúc 3 Tầng Tổng Thể (3-Tier Architecture)
```
[Nguồn Dữ Liệu Thô (Raw Sources)]
├── World Bank API (GDP, Dân số, Năng lượng tái tạo)
├── Climate Watch Data (Phát thải 9 ngành IPCC 1970-2023)
├── GSO Thống Kê (GRDP, Lao động, Che phủ rừng 63 tỉnh)
└── 189 Trạm Quan Trắc Không Khí (AQI, PM2.5, CO2 hàng giờ)
                 │
                 ▼ (Data Cleansing & Validation)
[Tầng Đệm Staging (Schema: staging)]
├── stg_worldbank, stg_climatewatch, stg_gso_provincial
├── stg_dim_stations, stg_hourly_air_monitoring
└── ETL_Audit_Log (Giám sát thực thi)
                 │
                 ▼ (SSIS Pipeline & Stored Procedures MERGE)
[Tầng Kho Dữ Liệu Doanh Nghiệp (Schema: dwh)]
├── Star Schema: 5 Dimensions & 3 Fact Tables
└── Clustered Columnstore Index (CCI 1.66M dòng)
                 │
                 ▼ (Semantic Layer & DirectQuery Interface)
[Tầng Trực Quan Hóa Báo Cáo (Power BI)]
├── 8 BI Semantic Views (DirectQuery / Import)
├── 35 DAX Measures Library
└── 2-Page Executive & Provincial Dashboard (TopoJSON 63 tỉnh)
```

### 3.2. Ma Trận Kiến Trúc Doanh Nghiệp (Enterprise Bus Matrix)
| Quy Trình Nghiệp Vụ / Fact Table | Dim_Date | Dim_Province | Dim_Sector | Dim_Station | Dim_Time_Of_Day |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Fact_National_Emissions** | 🟢 (Năm) | ⚪ | 🟢 (9 Ngành) | ⚪ | ⚪ |
| **Fact_Provincial_Economy** | 🟢 (Năm) | 🟢 (63 Tỉnh) | ⚪ | ⚪ | ⚪ |
| **Fact_Hourly_Air_Monitoring** | 🟢 (Ngày/Năm) | 🟢 (Tỉnh) | ⚪ | 🟢 (189 Trạm) | 🟢 (24 Giờ) |

*(Ghi chú: 🟢 Conformed Dimension dùng chung giúp liên kết và phân tích chéo đa chiều).*

### 3.3. Thiết Kế Chi Tiết Bảng Dữ Liệu
1. **`dwh.Dim_Date`:** 81 dòng (1970–2050), khóa đại diện `Date_Key` dạng số nguyên `YYYY`.
2. **`dwh.Dim_Province`:** 63 dòng, mã tỉnh `Province_Code` 2 ký tự chuẩn GSO, diện tích tự nhiên và cờ trọng điểm công nghiệp.
3. **`dwh.Dim_Sector`:** 9 dòng phân ngành chuẩn IPCC (Năng lượng, Nông nghiệp, GTVT, Công nghiệp...).
4. **`dwh.Dim_Station`:** 189 trạm quan trắc (KCN, Đô thị, Sinh thái) kèm tọa độ GPS Lat/Lon.
5. **`dwh.Dim_Time_Of_Day`:** 24 khung giờ kèm nhãn giờ cao điểm giao thông.
6. **`dwh.Fact_National_Emissions`:** 510 bản ghi phát thải lịch sử quốc gia.
7. **`dwh.Fact_Provincial_Economy`:** 630 bản ghi kinh tế - carbon 63 tỉnh thành.
8. **`dwh.Fact_Hourly_Air_Monitoring`:** **1,660,176 bản ghi** quan trắc hàng giờ năm 2024.

---

# CHƯƠNG 4: TRIỂN KHAI PIPELINE ETL & TỐI ƯU HÓA DỮ LIỆU LỚN

### 4.1. Tiền Xử Lý Dữ Liệu & Hàng Rào Kiểm Định (Data Profiling Quality Gate)
Trước khi đưa vào kho dữ liệu, toàn bộ dữ liệu thô được chuẩn hóa bằng Python:
* Xử lý triệt để bảng mã ký tự tiếng Việt (UTF-8 và UTF-8-BOM).
* Xây dựng ma trận chuẩn hóa tên 63 tỉnh thành (loại bỏ khác biệt chính tả như 'TP. Hồ Chí Minh' vs 'Hồ Chí Minh').
* Kiểm định 4 tiêu chí chất lượng: Tỷ lệ khuyết thiếu NULL < 5%, Toàn vẹn tham chiếu 100%, Khử 0 bản ghi trùng lặp khóa chính.

### 4.2. Giải Pháp SSIS & Cơ Chế Kiểm Soát Lỗi
* **Giải pháp SSIS hoàn chỉnh:** `NetZero_ETL.sln` bao gồm 4 gói:
  - `01_Staging_Load.dtsx`: Nạp dữ liệu thô vào staging.
  - `02_Dimension_Load.dtsx`: Nạp các bảng chiều chuẩn tắc với SCD Type 1 MERGE.
  - `03_Fact_Load.dtsx`: Nạp các bảng sự kiện vĩ mô có bảo vệ chống trùng lặp.
  - `00_Master_ETL.dtsx`: Gói điều phối trung tâm tự động hóa toàn bộ tiến trình.
* **Bảo vệ chống tính trùng GDP (Overcounting Guard):** Áp dụng logic lọc dữ liệu phân tách giữa Tổng GDP quốc gia và Giá trị gia tăng của từng phân ngành, ngăn chặn hoàn toàn lỗi cộng dồn GDP bị nhân lên 9 lần.
* **Ghi log kiểm toán (`staging.ETL_Audit_Log`):** Ghi nhận chi tiết thời gian thực thi, số dòng xử lý và trạng thái thành công/thất bại của từng bước.

### 4.3. Nạp Khối Tốc Độ Cao & Đo Lường Hiệu Năng Big Data
* Đối với bảng 1.66 triệu dòng `Fact_Hourly_Air_Monitoring`, nhóm phát triển sử dụng cơ chế streaming **.NET `SqlBulkCopy`** với batch size 50.000 dòng:
  - Thời gian nạp dữ liệu: **173 giây** cho toàn bộ 1.660.176 dòng (tốc độ ~9.600 dòng/giây).
  - Áp dụng Clustered Columnstore Index: Dung lượng lưu trữ giảm từ 128.04 MB xuống **24.81 MB (giảm 81%)**.
  - Tốc độ thực thi truy vấn phân tích (Aggregate 4 bảng JOIN trên 1.66M dòng): **0.08 giây (< 100ms)**.

---

# CHƯƠNG 5: TRỰC QUAN HÓA POWER BI, PHÂN TÍCH THỰC NGHIỆM & KẾT LUẬN

### 5.1. Mô Hình Ngữ Nghĩa DAX & Visual Storyboard
Hệ sinh thái Power BI Desktop được xây dựng với:
* **8 SQL BI Views** tối ưu hóa cho cả DirectQuery Mode và Import Mode.
* **Thư viện 35 DAX Measures** chia thành 6 nhóm chuyên biệt: Chỉ số quốc gia (GDP sạch), Kinh tế địa phương, Giám sát Big Data không khí, Phân tích chuỗi thời gian YoY/CAGR, Lộ trình khoảng cách Net-Zero 2030 (NDC Gap) và Mã màu định dạng động.
* **Tệp bản đồ TopoJSON 63 tỉnh thành** (`vietnam_provinces.topojson`, dung lượng 150 KB) cho phép Shape Map hiển thị mượt mà hình ảnh dải đất chữ S của Việt Nam.

### 5.2. Phân Tích Kết Quả Nghiệp Vụ Thực Nghiệm
1. **Phân tích Xu hướng Phát thải Quốc gia (1990–2024):**
   - Lĩnh vực **Năng lượng** chiếm tỷ trọng áp đảo (~48% tổng phát thải), tiếp theo là **Công nghiệp** (24%) và **Nông nghiệp** (18%).
   - Tốc độ tăng trưởng phát thải trung bình 5 năm gần nhất (5-Year CAGR) đạt +4.2%, cho thấy Việt Nam cần quyết liệt hơn nữa trong việc chuyển dịch năng lượng tái tạo để không bị vượt trần mục tiêu NDC 2030 (+167.3 MtCO2e).
2. **Bản đồ Phân tầng Kinh tế Xanh 63 Tỉnh Thành:**
   - **Nhóm Tách rời mạnh (Strong Decoupling):** Các tỉnh có tỷ lệ che phủ rừng cao và phát triển du lịch sinh thái (Lâm Đồng, Tuyên Quang, Quảng Nam) duy trì chất lượng không khí trong lành quanh năm với chỉ số AQI $\le 50$.
   - **Nhóm Thâm dụng Carbon & Nguy cơ cao:** Các trung tâm công nghiệp thâm dụng năng lượng (Bắc Ninh, Hải Dương, Quảng Ninh, Đồng Nai) có số giờ không khí vượt quy chuẩn QCVN 05:2023 cao gấp 3-4 lần mức trung bình toàn quốc, đối mặt với rủi ro thuế carbon CBAM rất lớn.
3. **Giám Sát Ô Nhiễm Không Khí Vi Mô 2024 (1.66M Dòng):**
   - Dữ liệu trích xuất chỉ rõ ô nhiễm bụi mịn PM2.5 tại Hà Nội và TP.HCM bùng phát mạnh vào **Giờ cao điểm giao thông (07:00–09:00 và 17:00–19:00)**.
   - Ngược lại, tại các trạm KCN (như Đình Vũ - Hải Phòng, KCN Biên Hòa - Đồng Nai), nồng độ SO2 và NO2 tăng cao vào **Ban đêm (23:00–04:00)**, là căn cứ số liệu đắt giá để các cơ quan thanh tra môi trường kiểm tra việc xả thải lén lút.

### 5.3. Kết Luận & Hướng Phát Triển
* **Đóng góp của Đề tài:**
  1. Cung cấp một kiến trúc Kho dữ liệu chuẩn mực quốc tế giải quyết trọn vẹn bài toán tích hợp dữ liệu kinh tế - phát thải phân mảnh tại Việt Nam.
  2. Ứng dụng thành công công nghệ Big Data Columnstore Index xử lý mượt mà hơn 1.66 triệu dòng bản ghi với hiệu năng truy vấn tức thời.
  3. Cung cấp nền tảng Business Intelligence hoàn chỉnh hỗ trợ các nhà quản lý đưa ra quyết định dựa trên dữ liệu (Data-driven Decision Making).
* **Hướng phát triển tương lai:**
  - Tích hợp thêm dữ liệu ảnh viễn thám vệ tinh (Sentinel-5P) đo mật độ khí CO2 và NO2 từ không gian.
  - Áp dụng các mô hình học máy (Machine Learning / LSTM) dự báo chuỗi thời gian phát thải đến năm 2050 theo các kịch bản chính sách khác nhau.

---

## TÀI LIỆU THAM KHẢO (REFERENCES)
1. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
2. Tapio, P. (2005). Towards a theory of decoupling: degrees of decoupling in the EU and the case of road traffic in Finland between 1970 and 2001. *Transport Policy*, 12(2), 137-151.
3. Chính phủ nước CHXHCN Việt Nam. (2022). *Nghị định số 06/2022/NĐ-CP ngày 07/01/2022 quy định giảm nhẹ phát thải khí nhà kính và bảo vệ tầng ô-dôn*.
4. Thủ tướng Chính phủ. (2024). *Quyết định số 13/2024/QĐ-TTg ngày 13/08/2024 ban hành danh mục lĩnh vực, cơ sở phát thải khí nhà kính phải thực hiện kiểm kê khí nhà kính*.
5. World Bank Open Data. (2024). *World Development Indicators: Vietnam Economic & Energy Statistics*.
6. Climate Watch. (2024). *CAIT Country Greenhouse Gas Emissions Data 1970-2023*.
7. Tổng cục Thống kê (GSO). (2024). *Niên giám Thống kê Việt Nam 2015-2024: Số liệu GRDP, Dân số và Diện tích rừng 63 tỉnh thành*.
