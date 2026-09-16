# Data Warehouse Giám Sát Phát Thải Khí Nhà Kính Hướng Tới Net-Zero Tại Việt Nam
### Vietnam Greenhouse Gas Emission Monitoring Data Warehouse & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-2019%2F2022-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![SSIS](https://img.shields.io/badge/ETL-SSIS-5C2D91?style=for-the-badge&logo=microsoft&logoColor=white)](https://docs.microsoft.com/sql/integration-services/)
[![Power BI](https://img.shields.io/badge/BI-Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Status](https://img.shields.io/badge/Status-In%20Development%20(Week%201)-success?style=for-the-badge)](#)

---

## 📌 Giới Thiệu Đề Tài (Overview)

Dự án xây dựng hệ thống **Kho dữ liệu (Data Warehouse)** và nền tảng **Business Intelligence (BI)** phục vụ theo dõi, giám sát và phân tích đa chiều phát thải khí nhà kính (GHG), năng lượng và chỉ số kinh tế xanh của 63 tỉnh thành hướng tới cam kết quốc gia **Net-Zero 2050** của Việt Nam.

Hệ thống được thiết kế theo chuẩn phương pháp luận **Kimball (Star Schema)**, tự động hóa từ khâu trích xuất API mở quốc tế đến xử lý dữ liệu và trực quan hóa hỗ trợ ra quyết định.

👉 **Đề cương chi tiết:** Xem [PROJECT_BRIEF_NetZero_DWH.md](./PROJECT_BRIEF_NetZero_DWH.md)

---

## 🎯 Mục Tiêu Cốt Lõi

1. **Tự động hóa nạp dữ liệu (Automated Ingestion):** Kéo dữ liệu phát thải lịch sử quốc gia từ **World Bank Open Data API**, phân bổ ngành kinh tế từ **ClimateWatch API** và số liệu kinh tế địa phương từ **Tổng cục Thống kê (GSO)**.
2. **Mô hình hóa dữ liệu chuẩn mực (Star Schema):** Xây dựng kho dữ liệu trên **Microsoft SQL Server** với các bảng Dimension chuẩn tắc (`Dim_Province`, `Dim_Date`, `Dim_Sector`) và 2 bảng Fact (`Fact_National_Emissions`, `Fact_Provincial_Economy`).
3. **Quy trình ETL chuyên nghiệp (SSIS Pipeline):** Tự động chuyển đổi dữ liệu từ tầng Staging, làm sạch ký tự tiếng Việt, xử lý tra cứu khóa đại diện (Surrogate Keys).
4. **Phân tích & Cảnh báo thông minh (Power BI Dashboard):**
   * **Hero Visual:** Bản đồ nhiệt phân vùng 63 tỉnh thành Việt Nam (Choropleth TopoJSON Map).
   * **Decoupling Index:** Chỉ số phân tách phát thải trên mỗi tỷ đồng GRDP ($\text{CO}_2\text{e} / \text{GRDP}$).
   * **Early Warning System:** Cảnh báo sớm các địa phương vượt ngưỡng hạn ngạch phát thải.

---

## 🏗️ Kiến Trúc Hệ Thống (Architecture)

```
[ NGUỒN DỮ LIỆU ĐẦU VÀO ]
 ├── World Bank API (REST JSON)
 ├── ClimateWatch API (REST JSON)
 └── Niên giám Thống kê GSO (CSV/Excel)
       │
       ▼ [Python Ingestion Script]
[ TẦNG STAGING (BRONZE) ]
 ├── stg_WorldBank_Emissions
 ├── stg_ClimateWatch_Sectors
 └── stg_GSO_Provinces
       │
       ▼ [SSIS ETL Pipeline]
[ TẦNG DATA WAREHOUSE (STAR SCHEMA) ]
 ├── Dim_Date (Conformed)
 ├── Dim_Province (Conformed)
 ├── Dim_Sector (Conformed)
 ├── Fact_National_Emissions (Grain: Năm x Ngành)
 └── Fact_Provincial_Economy (Grain: Năm x Tỉnh)
       │
       ▼ [DirectQuery / Import]
[ TRỰC QUAN HÓA & BI (POWER BI) ]
 ├── Trang 1: Executive Overview (Bản đồ 63 tỉnh + 4 KPI Cards + Xu hướng)
 └── Trang 2: Provincial Drill-Down & Early Warning (Bộ lọc tỉnh + Gauge cảnh báo)
```

---

## 📂 Cấu Trúc Thư Mục (Project Structure)

```
DWH/
├── data/
│   ├── raw/                 # Dữ liệu JSON/CSV thô tải về từ API và cổng mở
│   ├── staging/             # Dữ liệu bảng sạch chuẩn UTF-8 sẵn sàng nạp SSIS
│   └── reference/           # Danh mục chuẩn 63 tỉnh thành, bảng mã ngành
├── scripts/                 # Mã nguồn Python tự động hóa
│   ├── __init__.py
│   ├── utils.py             # Hàm tiện ích (logging, I/O UTF-8-sig cho tiếng Việt)
│   ├── fetch_worldbank.py   # Kéo chỉ số phát thải World Bank API
│   ├── fetch_climatewatch.py# Kéo phát thải phân ngành ClimateWatch API
│   └── clean_gso_data.py    # Chuẩn hóa số liệu 63 tỉnh thành từ GSO
├── tests/                   # Bộ kiểm thử tự động (Unit Tests)
│   └── test_phase1.py       # Kiểm thử cấu trúc môi trường & encoding UTF-8
├── plans/                   # Kế hoạch chi tiết theo chuẩn AgentKit
│   └── 260916-0709-week1-data-collection/ # Kế hoạch chi tiết Tuần 1
├── sql/                     # Script DDL tạo Database & Star Schema (Tuần 2)
├── ssis/                    # Visual Studio SSIS Solution (Tuần 3)
├── bi/                      # File báo cáo Power BI (.pbix) (Tuần 4)
├── requirements.txt         # Thư viện Python phụ thuộc
└── PROJECT_BRIEF_NetZero_DWH.md # Đề cương chi tiết đồ án
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Thử (Quick Start)

### 1. Yêu cầu hệ thống
* Python 3.11+
* Microsoft SQL Server 2019 / 2022 (Developer Edition) & SSMS
* Visual Studio 2022 kèm extension SQL Server Integration Services (SSIS)
* Power BI Desktop

### 2. Cài đặt môi trường Python
```bash
# Clone hoặc mở thư mục dự án
cd C:\Users\ADMIN\Desktop\DWH

# Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt
# Hoặc sử dụng uv:
uv pip install -r requirements.txt
```

### 3. Kiểm tra môi trường & Khởi tạo thư mục
```bash
python scripts/utils.py

# Chạy unit test kiểm tra
python -m unittest tests/test_phase1.py
```

---

## 📅 Lộ Trình Triển Khai (4-Week Implementation Plan)

| Tuần | Giai đoạn | Trọng tâm công việc | Trạng thái |
| :---: | :--- | :--- | :---: |
| **Tuần 1** | **Data Collection & Cleaning** | Viết script Python kéo API World Bank, ClimateWatch, chuẩn hóa dữ liệu GSO 63 tỉnh. | 🟡 Đang thực hiện (20%) |
| **Tuần 2** | **DWH Modeling & SQL Server** | Thiết kế Star Schema, viết script DDL tạo bảng Staging và Fact/Dim trên SQL Server. | ⚪ Sắp tới |
| **Tuần 3** | **ETL Pipeline với SSIS** | Xây dựng Package SSIS tự động nạp Staging, làm sạch dữ liệu, tra cứu khóa đại diện. | ⚪ Sắp tới |
| **Tuần 4** | **Power BI & Thuyết minh** | Thiết kế 2 trang Dashboard (Hero Map 63 tỉnh), viết các độ đo DAX và hoàn thiện báo cáo. | ⚪ Sắp tới |

---

## 📜 Căn Cứ Pháp Lý & Tham Chiếu Nghiên Cứu
* **Cam kết COP26 (2021):** Tuyên bố của Thủ tướng Chính phủ về mục tiêu Net-Zero vào năm 2050.
* **Nghị định 06/2022/NĐ-CP:** Quy định giảm nhẹ phát thải khí nhà kính và bảo vệ tầng ô-dôn.
* **Quyết định 01/2022/QĐ-TTg & 13/2024/QĐ-TTg:** Danh mục cơ sở phát thải khí nhà kính phải kiểm kê.
* **World Bank Open Data:** Chỉ số phát thải quốc gia Việt Nam (`VNM`).

---
**Tác giả:** Đồ án thực hiện độc lập (Solo Project)  
**Liên hệ / Hỗ trợ:** Vui lòng tạo Issue hoặc xem chi tiết tại [`plans/`](./plans/)
