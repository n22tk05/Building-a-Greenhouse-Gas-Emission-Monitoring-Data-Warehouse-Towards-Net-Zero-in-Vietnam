# Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero
## Hệ Thống Kho Dữ Liệu Giám Sát Phát Thải Khí Nhà Kính Hướng Tới Mục Tiêu Net-Zero Tại Việt Nam

[![University](https://img.shields.io/badge/University-VKU%20%7C%20The%20University%20of%20Danang-E31837?style=for-the-badge&logo=mortarboard&logoColor=white)](http://vku.udn.vn)
[![Course](https://img.shields.io/badge/Course-Data%20Warehouse%20(DWH)-0078D4?style=for-the-badge&logo=databricks&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-2019%2F2022-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![SSIS](https://img.shields.io/badge/ETL-SSIS%202022-5C2D91?style=for-the-badge&logo=microsoft&logoColor=white)](https://docs.microsoft.com/sql/integration-services/)
[![Power BI](https://img.shields.io/badge/BI-Power%20BI%20Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Status](https://img.shields.io/badge/Project%20Status-Completed%20100%25-success?style=for-the-badge)](#)

---

## 🏛️ Thông Tin Đồ Án (Academic Information)

- **Đơn vị đào tạo:** Trường Đại học Công nghệ Thông tin và Truyền thông Việt - Hàn (VKU), Đại học Đà Nẵng
- **Khoa:** Khoa Khoa học Máy tính (Computer Science Department)
- **Học phần:** Kho dữ liệu (Data Warehouse)
- **Đề tài:** *Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero* (Hệ thống Kho dữ liệu giám sát phát thải khí nhà kính hướng tới mục tiêu Net-Zero tại Việt Nam)
- **Sinh viên thực hiện:** **Nguyễn Quang Tuấn**
- **Mã sinh viên:** `22AD053` — **Lớp:** `22AD`
- **Giảng viên hướng dẫn:** **ThS. Mai Lam** (MD. Mai Lam)
- **Thời gian hoàn thành:** Tháng 11 / 2026

---

## 📌 Giới Thiệu Tổng Quan (Executive Summary)

Biến đổi khí hậu toàn cầu và cam kết lịch sử của Thủ tướng Chính phủ Việt Nam tại Hội nghị **COP26 (Net-Zero vào năm 2050)** đặt ra yêu cầu cấp thiết về một hệ thống dữ liệu tập trung, đa chiều, có khả năng đo lường, báo cáo và thẩm định (MRV) lượng phát thải khí nhà kính (GHG).

Dự án này nghiên cứu và xây dựng toàn diện **Kho dữ liệu phát thải khí nhà kính quốc gia** tích hợp công nghệ phân tích thông minh Business Intelligence, kết hợp giữa:
1. **Dữ liệu vĩ mô đa niên (1970–2023):** Thu thập từ Ngân hàng Thế giới (World Bank) và Climate Watch (CAIT/PIK), bao gồm phát thải CO2, CH4, N2O của 9 lĩnh vực phân loại IPCC và các chỉ tiêu kinh tế vĩ mô (GDP, dân số, năng lượng tái tạo).
2. **Dữ liệu kinh tế - sinh thái cấp địa phương (63 tỉnh thành):** Chuẩn hóa từ Niên giám Tổng cục Thống kê (GSO) về GRDP, dân số, cơ cấu công nghiệp, độ che phủ rừng và ước tính hấp thụ/phát thải carbon địa phương.
3. **Dữ liệu lớn vi mô quan trắc thời gian thực (Big Data 2024):** Mô phỏng và tích hợp **1.66 triệu dòng** quan trắc hàng giờ tại **189 trạm khí quyển** trên toàn quốc (nồng độ CO2 ppm, PM2.5, PM10, AQI theo quy chuẩn QCVN 05:2023/BTNMT).

---

## 🎯 Điểm Nhấn Kỹ Thuật Đột Phá (Core Engineering Highlights)

| Phân hệ Kỹ thuật | Giải pháp & Công nghệ Triển khai | Kết quả & Hiệu năng Đạt được |
| :--- | :--- | :--- |
| **Mô hình hóa Đa chiều** | Kiến trúc **Kimball Constellation Star Schema** với 5 bảng chiều (`Dim_Date`, `Dim_Province`, `Dim_Sector`, `Dim_Station`, `Dim_Time_Of_Day`) và 3 bảng Fact. | Dùng chung Conformed Dimensions giữa vĩ mô quốc gia, địa phương và chuỗi thời gian vi mô. |
| **Xử lý Dữ liệu Lớn (Big Data)** | Áp dụng **Clustered Columnstore Index (CCI)** kết hợp phân vùng trên bảng 1.66M dòng `Fact_Hourly_Air_Monitoring`. | Nén dung lượng **giảm 81%** (từ 128 MB xuống 24.8 MB); truy vấn tổng hợp 4 bảng JOIN chạy trong **0.08 giây (< 100ms)**. |
| **Đường ống ETL Tự động** | Thiết kế 4 gói **SSIS** (`00_Master`, `01_Staging`, `02_Dimension`, `03_Fact`) kết hợp streaming **.NET `SqlBulkCopy`**. | Tốc độ nạp dữ liệu đạt **> 55,000 dòng/giây**; kiểm soát lỗi tự động lưu vết tại `staging.ETL_Audit_Log`. |
| **Chống Nhân đôi GDP** | Cơ chế **GDP Overcounting Guard** tại tầng ETL và Semantic View, khẳng định chỉ gán GDP quốc gia tại mã ngành `TOT`. | Triệt tiêu hoàn toàn lỗi cộng dồn GDP nhân 9 lần khi người dùng lọc đa ngành trong báo cáo. |
| **Đồng bộ Dữ liệu Lịch sử** | Triển khai **Slowly Changing Dimension Type 1 (SCD Type 1 MERGE)** có tính chất Idempotent. | Chạy lại tiến trình ETL nhiều lần mà không gây trùng lặp khóa hoặc mất tính toàn vẹn tham chiếu. |
| **Địa lý Số Tùy biến (GIS)** | Biên tập file ranh giới số **`vietnam_provinces.topojson`** (150 KB) tương thích 100% mã tỉnh GSO ('01' đến '96'). | Tích hợp thành công **Shape Map** 63 tỉnh trên Power BI với khả năng tương tác lọc chéo mượt mà. |
| **Mô hình Phân tách Tapio** | Số hóa lý thuyết **Tapio Elasticity Model** thành các DAX Measures đánh giá tính phân tách kinh tế - carbon. | Phân nhóm địa phương thành 4 trạng thái: *Tách rời mạnh, Tách rời yếu, Tách rời suy thoái, Tăng trưởng thâm dụng*. |

---

## 🏗️ Kiến Trúc Hệ Thống (3-Tier DWH Architecture)

```
[ NGUỒN DỮ LIỆU ĐẦU VÀO (DATA SOURCES) ]
 ├── World Bank Open Data (GDP, Dân số, Tỷ lệ Năng lượng tái tạo 1970–2023)
 ├── Climate Watch / CAIT-PIK (Phát thải khí nhà kính 9 ngành IPCC 1970–2023)
 ├── Tổng cục Thống kê GSO (GRDP, Lao động, Diện tích, Độ che phủ rừng 63 tỉnh thành)
 └── 189 Trạm Quan Trắc Khí Quyển (Chuỗi dữ liệu vi mô 1.66 Triệu dòng năm 2024)
                           │
                           ▼ (Python Ingestion & Data Profiling Gate)
[ TẦNG DỮ LIỆU TRUNG GIAN (STAGING AREA - SCHEMA: [staging]) ]
 ├── stg_wb_national_emissions, stg_cw_sector_emissions
 ├── stg_gso_provincial_economy, stg_dim_provinces, stg_dim_stations
 ├── stg_hourly_air_monitoring
 └── ETL_Audit_Log (Ghi vết kiểm toán tự động: Package, Task, Start, End, Status, Rows)
                           │
                           ▼ (SSIS Orchestration + SCD Type 1 MERGE + .NET SqlBulkCopy)
[ TẦNG KHO DỮ LIỆU CHUẨN KIMBALL (CORE DATA WAREHOUSE - SCHEMA: [dwh]) ]
 ├── DIMENSION TABLES:
 │    ├── Dim_Date (1970–2050: Niên độ, Thập kỷ, Kế hoạch 5 năm, Mốc Net-Zero)
 │    ├── Dim_Province (63 tỉnh thành, Vùng kinh tế, Trọng điểm công nghiệp)
 │    ├── Dim_Sector (9 lĩnh vực phát thải chuẩn IPCC, Scope 1, 2, 3)
 │    ├── Dim_Station (189 trạm quan trắc, Tọa độ Lat/Long, Loại trạm)
 │    └── Dim_Time_Of_Day (24 khung giờ, Giờ cao điểm sáng/chiều, Ban đêm)
 └── FACT TABLES:
      ├── Fact_National_Emissions (Phát thải vĩ mô & GDP quốc gia 1970–2023)
      ├── Fact_Provincial_Economy (Phát thải, GRDP, Hấp thụ carbon & Decoupling 63 tỉnh)
      └── Fact_Hourly_Air_Monitoring (1,660,176 dòng + Clustered Columnstore Index)
                           │
                           ▼ (8 BI Semantic Views với DirectQuery & Dual Mode)
[ TẦNG PHÂN TÍCH & BÁO CÁO (POWER BI DESKTOP ANALYTICS PLATFORM) ]
 ├── Trang 1: Báo Cáo Điều Hành Chiến Lược Phát Thải Quốc Gia (Executive Overview)
 │    ├── 4 Thẻ KPI: Tổng GHG, GDP, % Năng lượng tái tạo, Chỉ số Decoupling Tapio
 │    ├── Bản đồ phân vùng nhiệt 63 tỉnh thành (Custom TopoJSON Shape Map)
 │    ├── Biểu đồ xu hướng tăng trưởng GDP vs Phát thải CO2 (Dual-axis Line & Column)
 │    └── Cơ cấu tỷ trọng phát thải 9 ngành IPCC (Donut / Treemap)
 └── Trang 2: Phân Tích Địa Phương & Cảnh Báo Sớm Hạn Ngạch 2030 (Provincial Deep-Dive)
      ├── Đồng hồ cảnh báo hạn ngạch phát thải phân bổ 2030 (Gauge Chart: Xanh/Vàng/Đỏ)
      ├── Ma trận phân nhóm 4 góc phần tư: Tăng trưởng GRDP vs Cường độ Carbon (Scatter Plot)
      ├── Bảng xếp hạng Top 10 địa phương phát thải cao nhất kèm thanh màu trực quan (Data Bars)
      └── Thẻ tóm tắt thông minh (Smart Narrative) tự động sinh nhận định chính sách
```

---

## 📂 Cấu Trúc Thư Mục Dự Án (Project Organization)

```
DWH/
├── data/
│   ├── raw/                             # Dữ liệu JSON/CSV thô tải từ API quốc tế
│   ├── staging/                         # Dữ liệu đã làm sạch UTF-8 sẵn sàng nạp ETL
│   ├── reference/                       # Danh mục chuẩn: dim_provinces, dim_stations
│   │   └── vietnam_provinces.topojson   # Bản đồ số 63 tỉnh tối ưu cho Power BI Shape Map
│   ├── data_profiling_report.md         # Báo cáo đánh giá chất lượng dữ liệu đầu vào
│   └── week*_verification_report.md     # Biên bản nghiệm thu kỹ thuật từng giai đoạn
├── docs/                                # Tài liệu học thuật và tài liệu kỹ thuật
│   ├── bao_cao_thuyet_minh_do_an.md     # Thuyết minh đồ án 5 chương hoàn chỉnh
│   ├── dwh_star_schema_design.md        # Đặc tả thiết kế mô hình sao Ralph Kimball
│   ├── ssis_etl_architecture.md         # Kiến trúc chi tiết các gói SSIS và Data Flow
│   ├── powerbi_dashboard_specification.md# Đặc tả bố cục, màu sắc, tọa độ 2 trang Dashboard
│   ├── dax_measures_dictionary.md       # Từ điển định nghĩa 35 công thức DAX chuyên sâu
│   └── presentation_slides.md           # Slide bảo vệ đồ án
├── powerbi/                             # Tài nguyên xây dựng báo cáo Power BI
│   ├── dax_measures.dax                 # Toàn bộ mã nguồn 35 DAX measures
│   ├── theme_netzero.json               # File theme giao diện Dark Slate & Emerald Green
│   └── README_BUILD_GUIDE.md            # Hướng dẫn chi tiết từng bước dựng Dashboard
├── scripts/                             # Scripts Python & PowerShell tự động hóa
│   ├── fetch_worldbank.py               # Thu thập tự động dữ liệu World Bank API
│   ├── fetch_climatewatch.py            # Thu thập dữ liệu phát thải ngành Climate Watch
│   ├── clean_gso_data.py                # Xử lý và làm sạch niên giám thống kê GSO 63 tỉnh
│   ├── generate_hourly_monitoring_data.py# Sinh dữ liệu mô phỏng 1.66M dòng quan trắc
│   ├── load_data_to_sql.ps1             # Nạp dữ liệu vào SQL Server tự động
│   ├── load_hourly_monitoring.ps1       # Streaming nạp 1.66M dòng qua .NET SqlBulkCopy
│   └── verify_topojson.py               # Kiểm tra tính toàn vẹn 63 tỉnh trong TopoJSON
├── sql/                                 # Kịch bản T-SQL triển khai cơ sở dữ liệu
│   ├── 00_init_database.sql             # Khởi tạo CSDL NetZero_VN_DWH
│   ├── 01_create_staging_tables.sql     # DDL các bảng Staging & bảng ETL_Audit_Log
│   ├── 02_create_star_schema.sql        # DDL mô hình sao DWH (Dim, Fact, Foreign Keys)
│   ├── 03_seed_dimensions.sql           # Nạp dữ liệu khởi tạo cho các bảng chiều
│   ├── 03b_etl_stored_procedures.sql    # Stored Procedures nạp Staging sang Dim & Fact
│   ├── 04_sample_analytic_queries.sql   # Các câu truy vấn phân tích nghiệp vụ mẫu
│   ├── 05_create_bi_views.sql           # 8 Views ngữ nghĩa tối ưu hóa cho Power BI
│   └── 06_create_hourly_monitoring_tables.sql # DDL bảng Big Data vi mô & cấu hình CCI
├── ssis/                                # Giải pháp SSIS trên Visual Studio 2022
│   └── NetZero_ETL/                     # Dự án SSIS chứa 4 gói (.dtsx) và connection managers
├── tests/                               # Bộ kiểm thử tự động toàn diện (64+ test cases)
│   ├── test_data_ingestion.py           # Kiểm tra toàn vẹn dữ liệu thu thập
│   ├── test_star_schema_ddl.py          # Kiểm tra cấu trúc bảng, ràng buộc khóa chính/khóa ngoại
│   ├── test_hourly_monitoring.py        # Kiểm tra bảng Big Data 1.66M dòng & chỉ mục CCI
│   ├── test_bi_views.py                 # Kiểm tra logic tính toán của 8 BI Views
│   ├── test_dax_logic.py                # Kiểm tra độ chính xác thuật toán DAX
│   └── test_topojson.py                 # Kiểm tra ánh xạ 63 tỉnh trên bản đồ TopoJSON
├── DWH.docx                             # Báo cáo đồ án chính thức (Định dạng Word chuẩn VKU)
├── requirements.txt                     # Danh mục thư viện Python phụ thuộc
└── README.md                            # Tài liệu tổng quan hệ thống
```

---

## 🚀 Hướng Dẫn Cài Đặt & Vận Hành (Quick Start Runbook)

### 1. Chuẩn bị Môi trường (Prerequisites)
- **Hệ điều hành:** Windows 10 / 11 (64-bit)
- **Cơ sở dữ liệu:** Microsoft SQL Server 2019 hoặc 2022 Developer / Standard
- **Công cụ quản trị:** SQL Server Management Studio (SSMS 19 hoặc 20)
- **Môi trường phát triển ETL:** Visual Studio 2022 Community kèm extension *SQL Server Integration Services Projects (SSIS)*
- **Nền tảng BI:** Microsoft Power BI Desktop (Bản phát hành từ 2023 trở về sau)
- **Ngôn ngữ thực thi:** Python 3.11+ và PowerShell 5.1+

### 2. Cài đặt Thư viện Python
Mở Terminal tại thư mục gốc dự án:
```powershell
pip install -r requirements.txt
```

### 3. Khởi tạo Cơ sở dữ liệu và Star Schema
Chạy tuần tự các script T-SQL trong thư mục `sql/` thông qua SSMS hoặc PowerShell:
```powershell
# 1. Khởi tạo CSDL NetZero_VN_DWH
Invoke-Sqlcmd -ServerInstance "localhost" -InputFile "sql/00_init_database.sql"

# 2. Tạo bảng Staging và bảng kiểm toán ETL_Audit_Log
Invoke-Sqlcmd -ServerInstance "localhost" -Database "NetZero_VN_DWH" -InputFile "sql/01_create_staging_tables.sql"

# 3. Tạo cấu trúc Star Schema (Fact, Dim, Ràng buộc Khóa ngoại & Check Constraints)
Invoke-Sqlcmd -ServerInstance "localhost" -Database "NetZero_VN_DWH" -InputFile "sql/02_create_star_schema.sql"

# 4. Khởi tạo Stored Procedures đồng bộ dữ liệu (SCD Type 1 MERGE)
Invoke-Sqlcmd -ServerInstance "localhost" -Database "NetZero_VN_DWH" -InputFile "sql/03b_etl_stored_procedures.sql"

# 5. Tạo cấu trúc bảng Big Data 1.66M dòng kèm Clustered Columnstore Index (CCI)
Invoke-Sqlcmd -ServerInstance "localhost" -Database "NetZero_VN_DWH" -InputFile "sql/06_create_hourly_monitoring_tables.sql"

# 6. Tạo 8 BI Views phục vụ kết nối Power BI
Invoke-Sqlcmd -ServerInstance "localhost" -Database "NetZero_VN_DWH" -InputFile "sql/05_create_bi_views.sql"
```

### 4. Nạp Dữ liệu Toàn Diện (ETL Execution)
```powershell
# Nạp toàn bộ dữ liệu vĩ mô (World Bank, Climate Watch, GSO 63 tỉnh)
powershell -ExecutionPolicy Bypass -File scripts/load_data_to_sql.ps1

# Streaming 1.66 triệu dòng dữ liệu quan trắc không khí tốc độ cao qua .NET SqlBulkCopy
powershell -ExecutionPolicy Bypass -File scripts/load_hourly_monitoring.ps1
```

### 5. Kiểm tra Kết quả Bảng Kiểm toán (Audit Trail)
Mở SSMS và chạy truy vấn kiểm tra:
```sql
USE [NetZero_VN_DWH];
GO

SELECT [Log_ID], [Package_Name], [Task_Name], [Start_Time], [End_Time], [Status], [Rows_Processed]
FROM [staging].[ETL_Audit_Log]
ORDER BY [Log_ID] ASC;
```

### 6. Khởi Chạy và Trực quan hóa trên Power BI Desktop
1. Mở **Power BI Desktop**, bật tính năng **Shape map visual** (`File > Options and settings > Options > Preview features > Shape map visual`).
2. Chọn **Get data > SQL Server**, điền Server `localhost`, Database `NetZero_VN_DWH`, chọn chế độ **Import** (hoặc DirectQuery).
3. Nạp 8 Views ngữ nghĩa trong schema `dwh` (`vw_Fact_..._BI`, `vw_Dim_..._BI`).
4. Import theme màu Net-Zero: Vào tab **View > Themes > Browse for themes**, chọn file `powerbi/theme_netzero.json`.
5. Tạo visual **Shape Map**, kéo `Province_Code` vào **Location**, tại phần **Format visual > Map settings > Custom map**, duyệt chọn file `data/reference/vietnam_provinces.topojson`.
6. Thực hiện theo hướng dẫn chi tiết tại [`powerbi/README_BUILD_GUIDE.md`](./powerbi/README_BUILD_GUIDE.md).

---

## 🧪 Kiểm Thử Hệ Thống (Regression Test Suite)

Dự án áp dụng quy trình kiểm thử tự động nghiêm ngặt nhằm đảm bảo tính toàn vẹn từ dữ liệu nguồn, mô hình Star Schema, các hàm nghiệp vụ đến độ phân giải của bản đồ TopoJSON:

```bash
python -m unittest discover tests
```
*Kết quả kiểm thử tự động:* **100% Test Cases ALL PASS**, đáp ứng đầy đủ tiêu chí nghiệm thu của đề tài nghiên cứu Data Warehouse.

---

## 📜 Căn Cứ Pháp Lý & Tài Liệu Tham Khảo (References)

1. **Cam kết COP26 (2021):** Tuyên bố của Thủ tướng Chính phủ Việt Nam tại Hội nghị lần thứ 26 các Bên tham gia Công ước Khung của Liên Hợp Quốc về Biến đổi Khí hậu về mục tiêu đạt mức phát thải ròng bằng “0” (Net-Zero) vào năm 2050.
2. **Nghị định số 06/2022/NĐ-CP:** Quy định giảm nhẹ phát thải khí nhà kính và bảo vệ tầng ô-dôn của Chính phủ Việt Nam.
3. **Quyết định số 01/2022/QĐ-TTg & Quyết định số 13/2024/QĐ-TTg:** Danh mục các lĩnh vực, cơ sở phát thải khí nhà kính phải thực hiện kiểm kê khí nhà kính.
4. **QCVN 05:2023/BTNMT:** Quy chuẩn kỹ thuật quốc gia về chất lượng không khí xung quanh do Bộ Tài nguyên và Môi trường ban hành.
5. **Kimball, R., & Ross, M. (2013):** *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
6. **Tapio, P. (2005):** Towards a theory of decoupling: degrees of decoupling in the EU and the case of road traffic in Finland between 1970 and 2001. *Transport Policy*, 12(2), 137–151.
7. **IPCC (2006/2019):** *2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories*. Intergovernmental Panel on Climate Change.

---

## ⚖️ Giấy Phép & Bản Quyền (License & Academic Rights)

Đồ án được phát triển phục vụ mục đích nghiên cứu và học thuật tại **Trường Đại học Công nghệ Thông tin và Truyền thông Việt - Hàn (VKU), Đại học Đà Nẵng**.  
Mã nguồn phát hành theo giấy phép [MIT License](./LICENSE). Mọi hành vi trích dẫn nội dung vui lòng ghi rõ nguồn tác giả.
