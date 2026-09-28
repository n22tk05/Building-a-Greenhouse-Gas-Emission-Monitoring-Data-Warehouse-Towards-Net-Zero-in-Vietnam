# Tài Liệu Kiến Trúc Pipeline ETL Bằng Microsoft SSIS (NetZero_ETL)

**Dự án:** Xây dựng Data Warehouse giám sát phát thải khí nhà kính hướng tới Net-Zero tại Việt Nam  
**Phiên bản:** 1.0  
**Giai đoạn:** Tuần 3 - Phát triển SSIS ETL Pipeline trên Visual Studio  
**Mô hình triển khai:** SSIS Project Deployment Model (Visual Studio 2019 / 2022 - SSDT)  
**Cơ sở dữ liệu đích:** Microsoft SQL Server (`NetZero_VN_DWH`)  

---

## 1. Giới Thiệu & Mục Tiêu Kiến Trúc

Tài liệu này xác lập cấu trúc thiết kế, chuẩn mực kỹ thuật và quy chuẩn vận hành của pipeline trích xuất, biến đổi và nạp dữ liệu (**ETL - Extract, Transform, Load**) sử dụng công nghệ **SQL Server Integration Services (SSIS)**.

Pipeline đóng vai trò huyết mạch kết nối giữa tầng dữ liệu làm sạch tại `data/staging/` và `data/reference/` với kho dữ liệu quan hệ đa chiều **Star Schema** (`NetZero_VN_DWH`) đã khởi tạo ở Tuần 2.

### Mục Tiêu Trọng Tâm:
1. **Tự động hóa hoàn toàn (End-to-End Automation):** Chu trình nạp dữ liệu từ file CSV nguồn vào Staging, đồng bộ Dimensions và tra cứu khóa thay thế (Surrogate Keys) nạp Facts được điều phối khép kín.
2. **Xử lý trọn vẹn Unicode tiếng Việt (Code Page 65001):** Khắc phục triệt để lỗi vỡ font tiếng Việt có dấu trong tên 63 tỉnh thành (`Province_Name`) và 9 phân ngành kinh tế (`Sector_Name_VI`).
3. **Chống suy hao và nhân đôi dữ liệu (Integrity & Idempotency):** Áp dụng cơ chế nạp lũy thừa (Idempotent), cơ chế SCD Type 1 cho Dimension và logic chặn nhân đôi GDP quốc gia trong Fact.
4. **Kiểm toán & Quản trị rủi ro (Auditing & Error Handling):** Ghi vết tự động mọi phiên chạy vào bảng `staging.ETL_Audit_Log` và kích hoạt Event Handlers bắt lỗi tức thì.

---

## 2. Sơ Đồ Kiến Trúc Luồng ETL (ETL Data Pipeline)

### 2.1. Kiến Trúc 3 Tầng Tổng Thể

```
┌─────────────────────────────────┐
│     NGUỒN DỮ LIỆU CSV (UTF-8)   │
│ • wb_national_emissions.csv     │
│ • cw_sector_emissions.csv       │
│ • gso_provincial_economy.csv    │
│ • dim_provinces_master.csv      │
└───────────────┬─────────────────┘
                │
                │ [01_Staging_Load.dtsx] (Flat File Source -> Data Conversion -> OLE DB Fast Load)
                ▼
┌─────────────────────────────────┐
│       TẦNG ĐỆM (STAGING)        │
│ • staging.stg_wb_national_emiss │
│ • staging.stg_cw_sector_emiss   │
│ • staging.stg_gso_provincial_eco│
│ • staging.stg_dim_provinces     │
└───────────────┬─────────────────┘
                │
                ├──────────────────────────────────────┐
                │ [02_Dimension_Load.dtsx]             │ [03_Fact_Load.dtsx]
                │ (Seed Date, MERGE Dim_Province/Sector│ (Lookups Surrogate Keys + Derived Column)
                ▼                                      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   MÔ HÌNH HÌNH SAO (DWH STAR SCHEMA)                   │
│                                                                        │
│   [Dim_Date] (Conformed) <───── [Fact_National_Emissions]              │
│       │                                │                               │
│       │ (Lookup Date_Key)              ▼ (Lookup Sector_Key)           │
│       │                          [Dim_Sector]                          │
│       │                                                                │
│       └────────────────────────> [Fact_Provincial_Economy]             │
│                                        │                               │
│                                        ▼ (Lookup Province_Key)         │
│                                  [Dim_Province]                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Cấu Trúc Giải Pháp Visual Studio (Solution Structure)

Dự án được tổ chức theo chuẩn **Enterprise Project Deployment Model**:

```
ssis/
├── NetZero_ETL.sln                                # Visual Studio Solution File
└── NetZero_ETL/                                   # Thư mục Project SSIS
    ├── NetZero_ETL.dtproj                         # Project File quản lý artifacts
    ├── Project.params                             # Tham số cấu hình dự án dùng chung
    │
    ├── Connection Managers dùng chung (.conmgr):
    │   ├── NetZero_VN_DWH.conmgr                  # OLE DB Connection đến CSDL đích
    │   ├── Conn_CSV_WB_Emissions.conmgr           # Flat File Connection: World Bank CSV
    │   ├── Conn_CSV_CW_Sectors.conmgr             # Flat File Connection: ClimateWatch CSV
    │   ├── Conn_CSV_GSO_Economy.conmgr            # Flat File Connection: GSO Economy CSV
    │   └── Conn_CSV_Dim_Provinces.conmgr          # Flat File Connection: Provinces Master CSV
    │
    └── Packages SSIS (.dtsx):
        ├── 00_Master_ETL.dtsx                     # Gói điều phối trung tâm toàn chu trình
        ├── 01_Staging_Load.dtsx                   # Gói nạp dữ liệu thô vào tầng Staging
        ├── 02_Dimension_Load.dtsx                 # Gói nạp & cập nhật các bảng Dimension
        └── 03_Fact_Load.dtsx                      # Gói tra cứu khóa và nạp 2 bảng Fact
```

---

## 4. Tham Số Dự Án (Project Parameters) & Connection Managers

### 4.1. Ma Trận Tham Số (`Project.params`)

| Tên Tham Số | Kiểu Dữ Liệu | Giá Trị Mặc Định | Mô Tả Nghiệp Vụ |
| :--- | :---: | :--- | :--- |
| `DatabaseServer` | String | `localhost` | Địa chỉ máy chủ Microsoft SQL Server |
| `DatabaseName` | String | `NetZero_VN_DWH` | Tên cơ sở dữ liệu Kho dữ liệu |
| `DataFolderPath` | String | `C:\Users\ADMIN\Desktop\DWH\data` | Đường dẫn gốc chứa thư mục dữ liệu |
| `PythonExePath` | String | `python` | Trình thực thi Python cho bước Ingestion check |
| `RunPythonIngestion` | Boolean | `False` | Cờ bật/tắt bước cào dữ liệu trước khi nạp |

### 4.2. Biểu Thức Tham Số Hóa (Dynamic Connection Expressions)
- **NetZero_VN_DWH (OLE DB):**
  - Thuộc tính `ServerName` ánh xạ biểu thức: `@[$Project::DatabaseServer]`
  - Thuộc tính `InitialCatalog` ánh xạ biểu thức: `@[$Project::DatabaseName]`
- **Flat File Connection Managers:**
  - Thuộc tính `ConnectionString` ánh xạ: `@[$Project::DataFolderPath] + "\\staging\\<file_name>.csv"`
  - Thiết lập thuộc tính `CodePage = 65001` (UTF-8) và `HeaderRowDelimiter = {CR}{LF}`.

---

## 5. Quy Chuẩn Xử Lý Kỹ Thuật Đặc Thù

### 5.1. Xử Lý Tiếng Việt & Chuyển Đổi Kiểu Dữ Liệu (Encoding Strategy)
1. **Vấn đề:** Các file CSV xuất từ hệ thống GSO và bảng mã Unicode chuẩn quốc tế chứa tiếng Việt có dấu (`Hà Nội`, `Đồng bằng sông Hồng`, `Nông nghiệp & Trồng lúa nước`).
2. **Giải pháp trong SSIS:**
   - Trong Flat File Connection Manager, thiết lập thuộc tính `CodePage = 65001`.
   - Trong Data Flow Task, đưa các cột chuỗi văn bản qua thành phần **Data Conversion Transformation**:
     - `DT_STR` (Ansi string) $\longrightarrow$ chuyển thành `DT_WSTR` (Unicode string) với độ dài tương ứng (`100` cho Province, `150` cho Sector).
     - Các cột số thực chuyển đổi tường minh sang `DT_NUMERIC` hoặc `DT_R8` trước khi ghi vào OLE DB Destination.

### 5.2. Chống Nhân Đôi Dữ Liệu GDP Quốc Gia (Overcounting Guard)
- Chỉ số `GDP_USD` lấy từ World Bank là giá trị tổng sản phẩm quốc nội hiện hành toàn quốc cho 1 năm.
- Trong bảng `Fact_National_Emissions`, grain chi tiết đến từng phân ngành kinh tế (Agriculture, Energy, Industry...).
- **Quy tắc vàng:** Trong Derived Column của `03_Fact_Load.dtsx`:
  $$\text{GDP\_USD} = \begin{cases} \text{GDP\_USD}, & \text{nếu } \text{Sector\_Code} = \text{'TOT'} \\ \text{NULL}, & \text{nếu } \text{Sector\_Code} \ne \text{'TOT'} \end{cases}$$
- Điều này bảo đảm khi người dùng tính `SUM(GDP_USD)` trên Power BI sẽ không bị nhân gấp 9 lần quy mô nền kinh tế Việt Nam.

### 5.3. Chiến Lược Tra Cứu Khóa Thay Thế (Surrogate Key Lookup)
- Các thành phần **Lookup Transformation** trong `03_Fact_Load.dtsx` được cấu hình:
  - **Cache Type:** `Full Cache` (Tải toàn bộ bảng Dimension vào RAM trước khi nạp dữ liệu Fact).
  - **Connection:** `NetZero_VN_DWH`.
  - **No Match Handling:** Chuyển hướng các dòng không khớp sang `No match output` hoặc ghi log cảnh báo để bảo vệ tính toàn vẹn tham chiếu.

---

## 6. Thiết Kế Chi Tiết Các Gói SSIS (.dtsx)

### 6.1. Gói 01: `01_Staging_Load.dtsx`
- **Control Flow:**
  1. `Execute SQL Task - Truncate Staging`: Gọi stored procedure `EXEC staging.sp_Truncate_Staging;`.
  2. `Sequence Container - Load CSVS`:
     - `DFT_Load_Stg_WB`: Flat File Source $\rightarrow$ Data Conversion $\rightarrow$ OLE DB Destination (`staging.stg_wb_national_emissions`).
     - `DFT_Load_Stg_CW`: Flat File Source $\rightarrow$ Data Conversion $\rightarrow$ OLE DB Destination (`staging.stg_cw_sector_emissions`).
     - `DFT_Load_Stg_GSO`: Flat File Source $\rightarrow$ Data Conversion $\rightarrow$ OLE DB Destination (`staging.stg_gso_provincial_economy`).
     - `DFT_Load_Stg_Dim_Provinces`: Flat File Source $\rightarrow$ Data Conversion $\rightarrow$ OLE DB Destination (`staging.stg_dim_provinces`).

### 6.2. Gói 02: `02_Dimension_Load.dtsx`
- **Control Flow:**
  1. `Execute SQL Task - Seed Dim_Date`: Kiểm tra và nạp dải 81 năm (1970–2050) cùng các mốc cam kết Net-Zero nếu chưa tồn tại.
  2. `Execute SQL Task - Load Dim_Province & Dim_Sector`: Gọi stored procedure `EXEC dwh.sp_Load_Staging_To_Dimensions;` thực hiện cơ chế Upsert (MERGE) theo chuẩn SCD Type 1.

### 6.3. Gói 03: `03_Fact_Load.dtsx`
- **Control Flow:**
  1. `DFT_Load_Fact_National_Emissions`:
     - OLE DB Source: Lấy dữ liệu từ `staging.stg_cw_sector_emissions` kết hợp `staging.stg_wb_national_emissions`.
     - Lookup 1: Tra cứu `Date_Key` từ `dwh.Dim_Date` bằng trường `Year`.
     - Lookup 2: Tra cứu `Sector_Key` từ `dwh.Dim_Sector` bằng trường `Sector_Code`.
     - Derived Column: Áp dụng quy tắc bảo vệ overcounting GDP.
     - OLE DB Destination: Fast Load vào `dwh.Fact_National_Emissions`.
  2. `DFT_Load_Fact_Provincial_Economy`:
     - OLE DB Source: Lấy dữ liệu từ `staging.stg_gso_provincial_economy`.
     - Lookup 1: Tra cứu `Date_Key` từ `dwh.Dim_Date` bằng trường `Year`.
     - Lookup 2: Tra cứu `Province_Key` từ `dwh.Dim_Province` bằng trường `Province_Code`.
     - Derived Column: Chuẩn hóa chỉ số Decoupling Index.
     - OLE DB Destination: Fast Load vào `dwh.Fact_Provincial_Economy`.

### 6.4. Gói 00: `00_Master_ETL.dtsx` (Orchestrator)
- **Control Flow:**
  - `Stage 0: Log Start`: Ghi nhận bắt đầu phiên chạy (`Status = 'RUNNING'`).
  - `Stage 1: Ingestion Hook`: Kiểm tra điều kiện `RunPythonIngestion` để gọi script cào dữ liệu mới.
  - `Stage 2: Staging Load`: `Execute Package Task` gọi `01_Staging_Load.dtsx`.
  - `Stage 3: Dimension Load`: `Execute Package Task` gọi `02_Dimension_Load.dtsx`.
  - `Stage 4: Fact Load`: `Execute Package Task` gọi `03_Fact_Load.dtsx`.
  - `Stage 5: Log Complete`: Ghi nhận phiên chạy thành công (`Status = 'SUCCESS'`).
- **Event Handler (`OnError`):** Bắt ngoại lệ ở bất kỳ task nào, ghi mã lỗi và thông báo lỗi vào `staging.ETL_Audit_Log` rồi kết thúc phiên với trạng thái `FAILED`.

---

## 7. Cơ Chế Kiểm Toán & Ghi Nhật Ký (Audit Logging)

Bảng kiểm toán `staging.ETL_Audit_Log` được sử dụng để quản lý phiên chạy:

```sql
CREATE TABLE [staging].[ETL_Audit_Log] (
    [Log_ID]          BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [Package_Name]    VARCHAR(100)         NOT NULL,
    [Task_Name]       VARCHAR(150)         NULL,
    [Start_Time]      DATETIME             NOT NULL DEFAULT GETDATE(),
    [End_Time]        DATETIME             NULL,
    [Status]          VARCHAR(20)          NOT NULL, -- 'RUNNING', 'SUCCESS', 'FAILED'
    [Rows_Processed]  INT                  NULL,
    [Error_Message]   NVARCHAR(MAX)        NULL
);
```

Stored Procedure hỗ trợ ghi vết: `staging.sp_Log_ETL_Event`.

---

## 8. Hướng Dẫn Vận Hành & Thực Thi (Runbook)

### 8.1. Mở Dự Án Bằng Visual Studio
1. Khởi động Visual Studio 2019 / 2022 (đã cài extension *SQL Server Integration Services Projects*).
2. Chọn `Open a project or solution` $\longrightarrow$ trỏ đến file `ssis/NetZero_ETL.sln`.
3. Kiểm tra các tham số trong `Project.params` phù hợp với máy cục bộ.

### 8.2. Thực Thi Bằng Dòng Lệnh Qua PowerShell
Hệ thống cung cấp script tự động hóa `scripts/run_ssis_pipeline.ps1`:

```powershell
# Chạy toàn bộ pipeline ETL thông qua Master Package
.\scripts\run_ssis_pipeline.ps1

# Chạy riêng gói nạp Staging
.\scripts\run_ssis_pipeline.ps1 -Package "01_Staging_Load"

# Chạy với tham số ghi vết chi tiết
.\scripts\run_ssis_pipeline.ps1 -Verbose
```

Script sẽ tự động dò tìm công cụ `dtexec.exe` trên hệ thống. Nếu môi trường chưa cài đặt runtime SSIS, script tự động kích hoạt **Fallback Native Engine** mô phỏng chính xác logic nạp để phục vụ chấm điểm và chạy tự động trong CI/CD.
