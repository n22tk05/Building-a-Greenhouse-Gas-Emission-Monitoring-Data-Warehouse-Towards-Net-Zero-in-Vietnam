# Data Warehouse Giám Sát Phát Thải Khí Nhà Kính Hướng Tới Net-Zero Tại Việt Nam
### Vietnam Greenhouse Gas Emission Monitoring Data Warehouse & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-2019%2F2022-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![SSIS](https://img.shields.io/badge/ETL-SSIS-5C2D91?style=for-the-badge&logo=microsoft&logoColor=white)](https://docs.microsoft.com/sql/integration-services/)
[![Power BI](https://img.shields.io/badge/BI-Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Status](https://img.shields.io/badge/Status-Completed%20100%25-success?style=for-the-badge)](#)
[![Tests](https://img.shields.io/badge/Tests-64%2F64%20PASS-brightgreen?style=for-the-badge)](#)

---

## 📌 Giới Thiệu Đề Tài (Overview)

Dự án xây dựng hệ thống **Kho dữ liệu (Data Warehouse - DWH)** chuẩn doanh nghiệp và nền tảng **Business Intelligence (BI)** đa chiều phục vụ theo dõi, giám sát và phân tích phát thải khí nhà kính (GHG), năng lượng và chỉ số kinh tế xanh của 63 tỉnh thành hướng tới cam kết quốc gia **Net-Zero 2050** của Việt Nam.

Hệ thống được thiết kế theo chuẩn phương pháp luận **Ralph Kimball (Star Schema)**, mở rộng tầng dữ liệu lớn (Big Data) với **1.66 triệu dòng** quan trắc không khí hàng giờ năm 2024, áp dụng công nghệ chỉ mục dạng cột **Clustered Columnstore Index (CCI)**, đường ống ETL tự động hóa trên **SSIS** và hệ thống Dashboard điều hành thông minh trên **Microsoft Power BI Desktop**.

👉 **Báo cáo Thuyết minh Đồ án 5 chương:** Xem [docs/bao_cao_thuyet_minh_do_an.md](./docs/bao_cao_thuyet_minh_do_an.md)  
👉 **Slide Thuyết trình Bảo vệ:** Xem [docs/presentation_slides.md](./docs/presentation_slides.md)  
👉 **Đặc tả Bố cục Dashboard:** Xem [docs/powerbi_dashboard_specification.md](./docs/powerbi_dashboard_specification.md)  
👉 **Từ điển Công thức DAX:** Xem [docs/dax_measures_dictionary.md](./docs/dax_measures_dictionary.md)  

---

## 🎯 Điểm Nhấn Kỹ Thuật Đột Phá

1. **Mô hình Đa chiều Kimball (Multi-Grain Dimensional Modeling):**
   - Tích hợp 5 chiều phân tích (`Dim_Date`, `Dim_Province`, `Dim_Sector`, `Dim_Station`, `Dim_Time_Of_Day`).
   - 3 bảng Fact: `Fact_National_Emissions` (510 dòng), `Fact_Provincial_Economy` (630 dòng), và `Fact_Hourly_Air_Monitoring` (**1,660,176 dòng**).
2. **Tối ưu hóa Big Data với Clustered Columnstore Index (CCI):**
   - Nén bảng 1.66 triệu dòng từ 128.04 MB xuống **24.81 MB (giảm 81% dung lượng)**.
   - Tốc độ thực thi truy vấn phân tích tổng hợp 4 bảng JOIN: **0.08 giây (< 100ms)**.
3. **Đường ống ETL Tự động hóa & Kiểm soát Lỗi:**
   - 4 gói SSIS tự động hóa (`01_Staging`, `02_Dimension`, `03_Fact`, `00_Master`).
   - Kỹ thuật nạp bù an toàn **SCD Type 1 MERGE (Idempotent)** và bảo vệ kép chống nhân đôi GDP (**GDP Overcounting Guard**).
   - Nhật ký kiểm toán tự động lưu vết tại `staging.ETL_Audit_Log`.
4. **Bản đồ Địa lý Số TopoJSON 63 Tỉnh Thành:**
   - File `data/reference/vietnam_provinces.topojson` (150 KB) khớp 100% ranh giới 63 tỉnh với visual **Shape Map (Preview)** trong Power BI.
5. **Thư viện 35 DAX Measures Chuyên sâu:**
   - Đánh giá khoảng cách mục tiêu Net-Zero 2030 (NDC Gap), Phân loại tách rời kinh tế Tapio, Cường độ carbon và Phân bổ hạn ngạch tín chỉ carbon.
6. **Kiểm thử Tự động Toàn diện (CI/CD Quality Gate):**
   - **64/64 unit tests ALL PASS (100%)** bảo đảm toàn vẹn dữ liệu từ tầng SQL đến tầng báo cáo BI.

---

## 🏗️ Kiến Trúc Hệ Thống (3-Tier DWH Architecture)

```
[ NGUỒN DỮ LIỆU ĐẦU VÀO (RAW SOURCES) ]
 ├── World Bank API (GDP, Dân số, Năng lượng tái tạo 1970-2023)
 ├── Climate Watch Data (Phát thải 9 ngành IPCC 1970-2023)
 ├── Tổng cục Thống kê GSO (GRDP, Lao động, Rừng 63 tỉnh)
 └── 189 Trạm Quan Trắc Không Khí (AQI, PM2.5, SO2, NO2 2024)
       │
       ▼ [Data Cleansing & Profiling Gate]
[ TẦNG STAGING TRUNG GIAN (SCHEMA: staging) ]
 ├── stg_worldbank, stg_climatewatch, stg_gso_provincial
 ├── stg_dim_stations, stg_hourly_air_monitoring
 └── ETL_Audit_Log (Ghi log kiểm toán thời gian thực)
       │
       ▼ [SSIS ETL Pipeline & .NET SqlBulkCopy Streaming]
[ TẦNG KHO DỮ LIỆU CHUẨN DOANH NGHIỆP (SCHEMA: dwh) ]
 ├── Dim_Date, Dim_Province, Dim_Sector, Dim_Station, Dim_Time_Of_Day
 ├── Fact_National_Emissions & Fact_Provincial_Economy
 └── Fact_Hourly_Air_Monitoring (1.66M Dòng + Clustered Columnstore Index)
       │
       ▼ [8 Semantic BI Views - DirectQuery / Import]
[ TẦNG TRỰC QUAN HÓA & PHÂN TÍCH (POWER BI DESKTOP) ]
 ├── Trang 1: Báo Cáo Điều Hành Quốc Gia (Executive Overview & Hero Shape Map)
 └── Trang 2: Phân Tích Chi Tiết Tỉnh & Cảnh Báo Sớm Hạn Ngạch 2030
```

---

## 👥 Phân Công Nhiệm Vụ Nhóm 5 Thành Viên

| STT | Thành viên | Vai trò | Phân hệ Chịu trách nhiệm Chính |
| :---: | :--- | :--- | :--- |
| 1 | **Nguyễn Tuấn Khánh** | Trưởng nhóm / Data Architect | Thiết kế kiến trúc Star Schema, Bus Matrix, DDL SQL Server, Điều phối chung |
| 2 | **Võ Quốc Anh** | Data Cleansing & QA Engineer | Thu thập data WB/CW/GSO, làm sạch tiếng Việt, cổng Data Profiling Gate |
| 3 | **Hà Trần Bảo Trân** | ETL Pipeline Engineer | Xây dựng 4 gói SSIS, Staging Load, cơ chế nạp bù MERGE & Audit Log |
| 4 | **Võ Văn Nhân** | Big Data & Performance Engineer | Nạp khối 1.66M dòng SqlBulkCopy, Clustered Columnstore Index, Benchmark <0.1s |
| 5 | **Lê Trần Đoan Trang** | BI Developer & Data Analyst | Xây dựng 35 DAX Measures, TopoJSON Map 63 tỉnh, 2 trang Power BI Dashboard |

---

## 📂 Cấu Trúc Thư Mục Dự Án (Project Structure)

```
DWH/
├── data/
│   ├── raw/                 # Dữ liệu JSON/CSV thô tải về từ API và cache
│   ├── staging/             # Dữ liệu bảng sạch chuẩn UTF-8 sẵn sàng nạp SSIS
│   ├── reference/           # Danh mục 63 tỉnh, 189 trạm, và vietnam_provinces.topojson
│   ├── data_profiling_report.md
│   ├── week2_schema_verification_report.md
│   ├── week3_etl_verification_report.md
│   └── week4_powerbi_verification_report.md  # Báo cáo nghiệm thu hoàn thành 100%
├── docs/                    # Tài liệu học thuật và đặc tả hệ thống
│   ├── bao_cao_thuyet_minh_do_an.md          # Báo cáo đồ án 5 chương hoàn chỉnh
│   ├── presentation_slides.md                # Slide thuyết trình bảo vệ đồ án
│   ├── dwh_star_schema_design.md             # Tài liệu thiết kế mô hình sao Kimball
│   ├── ssis_etl_architecture.md              # Tài liệu kiến trúc đường ống SSIS
│   ├── powerbi_dashboard_specification.md    # Đặc tả bố cục 2 trang Dashboard Power BI
│   └── dax_measures_dictionary.md            # Từ điển tra cứu 35 công thức DAX
├── powerbi/                 # Tài nguyên phân tích Power BI Desktop
│   ├── dax_measures.dax     # Thư viện toàn bộ 35 công thức DAX chuẩn
│   ├── theme_netzero.json   # Theme giao diện Net-Zero Emerald Nền tối
│   └── README_BUILD_GUIDE.md# Hướng dẫn chi tiết từng bước dựng Dashboard
├── scripts/                 # Bộ mã nguồn Python & PowerShell tự động hóa
│   ├── fetch_worldbank.py   # Thu thập World Bank API
│   ├── fetch_climatewatch.py# Thu thập ClimateWatch API
│   ├── clean_gso_data.py    # Làm sạch số liệu 63 tỉnh thành GSO
│   ├── generate_hourly_monitoring_data.py # Sinh dữ liệu quan trắc 1.66M dòng
│   ├── load_data_to_sql.ps1 # Nạp tự động toàn bộ dữ liệu vào SQL Server
│   ├── load_hourly_monitoring.ps1 # Nạp streaming 1.66M dòng qua SqlBulkCopy
│   └── verify_topojson.py   # Cổng kiểm định chất lượng ranh giới địa lý số
├── sql/                     # Tập hợp kịch bản T-SQL DDL, Stored Procedures & Views
│   ├── 00_init_database.sql # Khởi tạo CSDL NetZero_VN_DWH
│   ├── 01_create_staging_tables.sql
│   ├── 02_create_star_schema.sql
│   ├── 03b_etl_stored_procedures.sql
│   ├── 04_sample_analytic_queries.sql
│   ├── 05_create_bi_views.sql # 8 BI Views ngữ nghĩa
│   └── 06_create_hourly_monitoring_tables.sql # DDL Big Data 1.66M dòng & CCI
├── ssis/                    # Visual Studio SSIS Solution (Gói ETL tự động)
│   └── NetZero_ETL/
├── tests/                   # Bộ kiểm thử tự động toàn diện (64 Test Cases)
│   ├── test_phase1.py       # Kiểm thử môi trường & encoding
│   ├── test_data_ingestion.py # Kiểm thử dữ liệu thu thập
│   ├── test_star_schema_ddl.py # Kiểm thử cấu trúc Star Schema
│   ├── test_ssis_packages.py# Kiểm thử các gói SSIS
│   ├── test_hourly_monitoring.py # Kiểm thử Big Data 1.66M dòng
│   ├── test_bi_views.py     # Kiểm thử 8 BI Views
│   ├── test_dax_logic.py    # Kiểm thử logic công thức DAX
│   ├── test_topojson.py     # Kiểm thử ranh giới 63 tỉnh TopoJSON
│   ├── test_dashboard_storyboard.py # Kiểm thử storyboard giao diện
│   └── test_powerbi_data.py # Kiểm thử tích hợp tổng thể Tuần 4
├── requirements.txt         # Thư viện Python phụ thuộc
└── PROJECT_BRIEF_NetZero_DWH.md
```

---

## 🚀 Hướng Dẫn Vận Hành & Khởi Chạy Nhanh (Quick Start)

### 1. Khởi tạo Cơ sở dữ liệu và Star Schema
Mở PowerShell tại thư mục dự án và chạy:
```powershell
# 1. Khởi tạo CSDL và các bảng
Invoke-Sqlcmd -ServerInstance 'localhost' -InputFile 'sql/00_init_database.sql'
Invoke-Sqlcmd -ServerInstance 'localhost' -Database 'NetZero_VN_DWH' -InputFile 'sql/02_create_star_schema.sql'
Invoke-Sqlcmd -ServerInstance 'localhost' -Database 'NetZero_VN_DWH' -InputFile 'sql/06_create_hourly_monitoring_tables.sql'

# 2. Nạp dữ liệu vào SQL Server
powershell -ExecutionPolicy Bypass -File scripts/load_data_to_sql.ps1
powershell -ExecutionPolicy Bypass -File scripts/load_hourly_monitoring.ps1

# 3. Tạo 8 BI Views ngữ nghĩa
Invoke-Sqlcmd -ServerInstance 'localhost' -Database 'NetZero_VN_DWH' -InputFile 'sql/05_create_bi_views.sql'
```

### 2. Chạy Kiểm thử Toàn hệ thống (Regression Test Suite)
```bash
python -m unittest discover tests
# Kết quả: Ran 64 tests in ~0.2s -> OK (100% ALL PASS)
```

### 3. Mở & Xây dựng Báo cáo trên Power BI Desktop
Xem chi tiết hướng dẫn kéo thả từng visual và nạp bản đồ 63 tỉnh thành tại:  
👉 [`powerbi/README_BUILD_GUIDE.md`](./powerbi/README_BUILD_GUIDE.md)

---

## 📜 Căn Cứ Pháp Lý & Tham Chiếu
* **Cam kết COP26 (2021):** Tuyên bố của Thủ tướng Chính phủ về mục tiêu Net-Zero vào năm 2050.
* **Nghị định 06/2022/NĐ-CP:** Quy định giảm nhẹ phát thải khí nhà kính và bảo vệ tầng ô-dôn.
* **Quyết định 01/2022/QĐ-TTg & 13/2024/QĐ-TTg:** Danh mục 2.166 cơ sở phát thải khí nhà kính phải kiểm kê.
* **QCVN 05:2023/BTNMT:** Quy chuẩn kỹ thuật quốc gia về chất lượng không khí xung quanh.
* **Kimball, R., & Ross, M. (2013):** *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.).
* **Tapio, P. (2005):** Towards a theory of decoupling: degrees of decoupling in the EU. *Transport Policy*, 12(2), 137-151.
