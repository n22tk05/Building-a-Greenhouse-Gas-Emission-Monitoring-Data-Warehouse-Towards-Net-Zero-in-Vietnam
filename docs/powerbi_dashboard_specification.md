# Đặc Tả Kiến Trúc Thị Giác & Bố Cục Dashboard Power BI (Visual Storyboard Specification)

**Dự án:** Hệ thống Giám Sát Phát Thải Khí Nhà Kính Hướng Tới Net-Zero Tại Việt Nam (`NetZero_VN_DWH`)  
**Giai đoạn:** Tuần 4 - Phase 4 (Visual Storyboard & Interaction Specification)  
**Tệp cấu hình giao diện (Theme):** [`powerbi/theme_netzero.json`](file:///C:/Users/ADMIN/Desktop/DWH/powerbi/theme_netzero.json)  
**Tệp ranh giới số bản đồ:** [`data/reference/vietnam_provinces.topojson`](file:///C:/Users/ADMIN/Desktop/DWH/data/reference/vietnam_provinces.topojson)  
**Bộ thư viện độ đo DAX:** [`powerbi/dax_measures.dax`](file:///C:/Users/ADMIN/Desktop/DWH/powerbi/dax_measures.dax)

---

## 1. Hệ Thống Nhận Diện Thị Giác & Quy Chuẩn Thiết Kế (Design System)

### 1.1. Bảng Màu Thương Hiệu Net-Zero (Net-Zero Emerald Palette)
| Mã Màu Hex | Vai trò Thị giác | Ứng dụng trên Dashboard |
| :---: | :--- | :--- |
| **`#0F172A`** | **Dark Slate Canvas** | Màu nền bao quát toàn bộ trang Dashboard (tạo chiều sâu, chống mỏi mắt). |
| **`#1E293B`** | **Panel Container** | Màu nền cho từng Card, Chart Panel, bo góc 8px với viền mềm. |
| **`#334155`** | **Hairline Border** | Màu viền phân cách mỏng giúp các khối thông tin tách bạch rõ ràng. |
| **`#10B981`** | **Emerald Green** | Màu điểm nhấn chính: Tín hiệu Tốt, Tách rời mạnh, Đạt cam kết Net-Zero. |
| **`#06B6D4`** | **Cyan Electric** | Thể hiện Năng lượng tái tạo, Chỉ số đổi mới công nghệ sạch. |
| **`#F59E0B`** | **Amber Warning** | Màu cảnh báo trung bình: Tách rời yếu, AQI trung bình. |
| **`#EF4444`** | **Crimson Alert** | Màu báo động đỏ: Vượt trần hạn ngạch carbon, AQI ô nhiễm nghiêm trọng. |
| **`#F8FAFC`** | **Primary Typography** | Màu chữ chính (KPI Callout Value, Tiêu đề Card). |
| **`#94A3B8`** | **Secondary Text** | Màu chữ phụ (Category Label, Đơn vị tính, Chú thích). |

### 1.2. Kích Thước Bố Cục Chuẩn (Canvas Grid)
* **Tỷ lệ hiển thị:** Widescreen 16:9 ($1920 \times 1080$ px hoặc $1280 \times 720$ px).
* **Căn lề (Padding):** Lề ngoài 16px, khoảng cách giữa các panel (Gutter) 12px.
* **Nguyên tắc điều hướng thị giác:** Từ Trên xuống Dưới (Tổng quan $\rightarrow$ Chi tiết), từ Trái sang Phải (Bối cảnh $\rightarrow$ Tương quan $\rightarrow$ Cảnh báo).

---

## 2. Trang 1: Báo Cáo Điều Hành Chiến Lược Phát Thải Quốc Gia (Executive Overview)

### 2.1. Mục Tiêu Nghiệp Vụ
Cung cấp góc nhìn toàn cảnh cấp quốc gia cho các nhà hoạch định chính sách và lãnh đạo: đánh giá mối tương quan giữa quy mô tăng trưởng GDP và xu thế phát thải khí nhà kính (CO2, CH4), theo dõi tiến độ cam kết NDC 2030 và Net-Zero 2050, nhận diện các điểm nóng ô nhiễm trên bản đồ địa lý 63 tỉnh thành.

### 2.2. Sơ Đồ Bố Cục Tọa Độ (Layout Grid Map)
```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [VISUAL 1.1] HEADER BANNER & YEAR SLICER                                   [Mốc thời gian: 2024 ▼]    │
├───────────────────┬───────────────────┬───────────────────────────┬────────────────────────────────────┤
│ [VISUAL 1.2A]     │ [VISUAL 1.2B]     │ [VISUAL 1.2C]             │ [VISUAL 1.2D]                      │
│ TỔNG PHÁT THẢI    │ TỔNG SẢN PHẨM     │ NĂNG LƯỢNG TÁI TẠO        │ KHOẢNG CÁCH NDC 2030               │
│ 384.2 MtCO2e      │ $430.0 Tỷ USD     │ 32.4%                     │ +167.3 MtCO2e                      │
│ (YoY: -1.2%)      │ (YoY: +6.5%)      │ (Đang chuyển dịch tích cực)│ (Nguy cơ vượt trần cam kết)        │
├───────────────────┴───────────────────┴───────────────────────────┴────────────────────────────────────┤
│ ┌───────────────────────────────────────┐ ┌──────────────────────────────────────────────────────────┐ │
│ │ [VISUAL 1.3] HERO SHAPE MAP           │ │ [VISUAL 1.4] DUAL-AXIS TREND (1990 - 2024)               │ │
│ │ 63 Tỉnh Thành Việt Nam                │ │ Cột: GDP sạch ($ Tỷ USD, Overcounting Guard)           │ │
│ │ Phân màu: Decoupling Color Hex        │ │ Đường: Phát thải GHG (MtCO2e) & Mốc Net-Zero 2050        │ │
│ │ • Xanh lá: Tách rời mạnh              │ ├──────────────────────────────────────────────────────────┤ │
│ │ • Vàng: Tách rời yếu                  │ │ [VISUAL 1.5] CƠ CẤU PHÁT THẢI 9 NGÀNH IPCC (DONUT)       │ │
│ │ • Đỏ: Thâm dụng carbon                │ │ Năng lượng (48%) | Công nghiệp (24%) | Nông nghiệp (18%) │ │
│ └───────────────────────────────────────┘ └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3. Cấu Hình Chi Tiết Từng Visual Trang 1
1. **Visual 1.1 - Thanh Tiêu Đề Điều Hành (Top Header):**
   - Tiêu đề: `HỆ THỐNG GIÁM SÁT PHÁT THẢI KHÍ NHÀ KÍNH HƯỚNG TỚI NET-ZERO TẠI VIỆT NAM`.
   - Phụ đề: `Nền tảng Kho dữ liệu Đa chiều & Báo cáo Thông minh (Kimball Star Schema + Big Data 1.66M Dòng)`.
   - Slicer: `vw_Dim_Date_BI[Year]` (Dropdown, chọn mặc định năm 2024).

2. **Visual 1.2 (A-D) - Dải Thẻ Chỉ Số Cốt Lõi (Executive KPI Strip):**
   - **Thẻ 1.2A:** Measure `[Total GHG Emissions (MtCO2e)]`, Callout value màu Trắng, nhãn phụ `[Emissions YoY Growth %]`.
   - **Thẻ 1.2B:** Measure `[National GDP (USD)]` (có Overcounting Guard), format tiền tệ `$#,##0`.
   - **Thẻ 1.2C:** Measure `[Renewable Energy Pct]`, format `0.0%`, Callout value màu Cyan Electric `#06B6D4`.
   - **Thẻ 1.2D:** Measure `[NetZero 2030 Target Gap (MtCO2e)]`, Callout subtitle `[Dynamic KPI Subtitle - NetZero Status]`.

3. **Visual 1.3 - Bản Đồ Phân Vùng 63 Tỉnh Thành (Hero Shape Map):**
   - Loại visual: `Shape map` (Bật trong Options Preview của Power BI).
   - Thiết lập Map settings: `Map type = Custom map`, Import file `vietnam_provinces.topojson`.
   - `Location`: `vw_Dim_Province_Geo_BI[Province_Code]`.
   - `Color saturation`: `[Provincial Decoupling Index]`.
   - Conditional formatting: Màu Xanh lá (`#10B981`) cho Index < 0, Vàng (`#F59E0B`) cho 0 - 0.8, Đỏ (`#EF4444`) cho > 1.2.
   - Tooltips: `Province_Name`, `Region`, `Provincial GRDP (Billion VND)`, `Provincial Carbon Tonnes`, `Decoupling Status Label`.

4. **Visual 1.4 - Biểu Đồ Xu Hướng Đa Trục (Dual-Axis Line & Column Chart):**
   - Trục hoành (Shared X-Axis): `vw_Dim_Date_BI[Year]` (Lọc từ 1990 đến 2024).
   - Cột (Column Values): `[National GDP (USD)]` (Màu xanh dương đậm `#3B82F6`).
   - Đường (Line Values): `[Total GHG Emissions (MtCO2e)]` (Màu xanh ngọc bích `#10B981`).
   - Reference Line: Đường mục tiêu `[Target Emission 2030 (NDC)]` nét đứt màu đỏ.

5. **Visual 1.5 - Cơ Cấu Phát Thải Phân Ngành IPCC (Donut / Treemap):**
   - Category: `vw_Dim_Sector_Hierarchy_BI[Sector_Name_VI]`.
   - Values: `[Total GHG Emissions (MtCO2e)]`.
   - Lọc: Loại trừ `Sector_Code = 'TOT'` để chỉ hiển thị các nhánh ngành con.

---

## 3. Trang 2: Phân Tích Chi Tiết Địa Phương & Cảnh Báo Sớm (Provincial Drill-down & Early Warning)

### 3.1. Mục Tiêu Nghiệp Vụ
Đi sâu vào từng đơn vị hành chính cấp tỉnh: giám sát hạn ngạch carbon phân bổ năm 2030, phân loại địa phương theo mô hình 4 góc phần tư Tapio (Tăng trưởng GRDP vs Thâm dụng Carbon), tích hợp dữ liệu quan trắc không khí Big Data từng giờ để phát hiện các khu vực xả thải vượt chuẩn QCVN.

### 3.2. Sơ Đồ Bố Cục Tọa Độ (Layout Grid Map)
```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [VISUAL 2.1] TOP FILTER BAR: [Vùng KTTĐ: Tất cả ▼]  [Vùng Địa lý: Tất cả ▼]  [Chọn Tỉnh: Hà Nội ▼]      │
├────────────────────────────────────────┬───────────────────────────────────────────────────────────────┤
│ [VISUAL 2.2]                           │ [VISUAL 2.3]                                                  │
│ ĐỒNG HỒ CẢNH BÁO HẠN NGẠCH CARBON 2030 │ MA TRẬN 4 GÓC PHẦN TƯ (GROWTH VS CARBON INTENSITY)           │
│ • Giá trị: [Provincial Carbon Tonnes]  │ • Trục X: Tốc độ tăng trưởng GRDP (%)                         │
│ • Kim trần: [Provincial Quota 2030]    │ • Trục Y: Cường độ Carbon (Tấn / Tỷ VNĐ)                      │
│ • Cảnh báo: Đỏ nếu Quota Realization >100% • Kích thước bóng: Dân số tỉnh                              │
├────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│ [VISUAL 2.4]                           │ [VISUAL 2.5]                                                  │
│ GIÁM SÁT Ô NHIỄM KHÔNG KHÍ HÀNG GIỜ    │ DIỄN GIẢI THÔNG MINH & ĐỀ XUẤT CHÍNH SÁCH (SMART NARRATIVE)  │
│ (1.66M Dòng - Fact_Hourly_Air)         │                                                               │
│ • Cột kép: Giờ Thường vs Giờ Cao Điểm │ Tiêu đề: [Dynamic Card Title - Selected Province]             │
│ • Chỉ số: Avg AQI & Giờ vượt chuẩn     │ "Năm 2024, tỉnh [Hà Nội] đạt GRDP 1.250 nghìn tỷ VNĐ với     │
│   QCVN 05:2023 theo trạm quan trắc     │ phát thải 31.2 triệu tấn CO2e. Trạng thái: Tách rời yếu.      │
│                                        │ Đề xuất: Tăng cường kiểm soát khí thải KCN tại trạm Ba Đình.."│
└────────────────────────────────────────┴───────────────────────────────────────────────────────────────┘
```

### 3.3. Cấu Hình Chi Tiết Từng Visual Trang 2
1. **Visual 2.1 - Thanh Lọc Phân Cấp (Hierarchical Slicer Bar):**
   - Slicer 1: `vw_Dim_Province_Geo_BI[Macro_Region]` (Miền Bắc / Miền Trung / Miền Nam).
   - Slicer 2: `vw_Dim_Province_Geo_BI[Economic_Zone]` (KTTĐ Bắc Bộ, KTTĐ Phía Nam, Khác...).
   - Slicer 3: `vw_Dim_Province_Geo_BI[Province_Name]` (Dropdown tìm kiếm tên 63 tỉnh).

2. **Visual 2.2 - Đồng Hồ Cảnh Báo Hạn Ngạch 2030 (Gauge Chart):**
   - Value: `[Provincial Carbon Tonnes]`.
   - Target value: `[Provincial Emission Quota 2030]`.
   - Minimum: `0`, Maximum: `[Provincial Emission Quota 2030] * 1.5`.
   - Format: Màu kim đo đổi sang Đỏ khi `[Quota Realization %] > 100%`, Xanh lá khi $\le 100\%$.

3. **Visual 2.3 - Ma Trận Phân Nhóm Kinh Tế - Carbon (Scatter Plot 4 Góc Phần Tư):**
   - Trục hoành (X-Axis): `[GRDP YoY Growth %]` (Ngưỡng tham chiếu trung bình toàn quốc: 6.5%).
   - Trục tung (Y-Axis): `[Carbon Intensity (Tonnes per Billion VND)]`.
   - Size: `[Provincial Population]`.
   - Legend: `vw_Dim_Province_Geo_BI[Region]`.
   - 4 Phân nhóm chiến lược:
     + *Góc Dưới - Phải:* **Kinh tế Xanh Tiên phong** (Tăng trưởng cao, Cường độ carbon thấp).
     + *Góc Trên - Phải:* **Mở rộng thâm dụng** (Tăng trưởng cao nhưng Phát thải quá lớn).
     + *Góc Dưới - Trái:* **Ổn định sinh thái** (Tăng trưởng chậm, Bảo tồn rừng tốt).
     + *Góc Trên - Trái:* **Nguy cơ cảnh báo đỏ** (Tăng trưởng chậm nhưng Ô nhiễm nặng).

4. **Visual 2.4 - Giám Sát Chất Lượng Không Khí Vi Mô 2024 (Clustered Column & Line Chart):**
   - Dữ liệu nguồn: View `vw_Fact_Hourly_Air_Monitoring_BI` (DirectQuery/Columnstore 1.66M dòng).
   - X-Axis: `vw_Dim_Station_BI[Station_Name]` (Lọc theo các trạm thuộc tỉnh được chọn).
   - Column Values: `[Exceeding QCVN Hours]` và `[Rush Hour Exceeding Hours]`.
   - Line Value: `[Avg AQI Index]`.
   - Mục đích: Chỉ rõ ô nhiễm do giao thông giờ cao điểm hay do xả thải trạm công nghiệp.

5. **Visual 2.5 - Thẻ Diễn Giải Thông Minh & Khuyến Nghị (Smart Narrative Text Card):**
   - Visual: `Card` hoặc `Smart Narrative textbox`.
   - Header: `[Dynamic Card Title - Selected Province]`.
   - Dynamic Content Measure: Ghép nối tự động các chỉ số của tỉnh được chọn để đưa ra khuyến nghị tức thì.

---

## 4. Ma Trận Tương Tác Lọc Chéo (Cross-Filtering Behavior Matrix)

| Visual Nguồn (Source Click) | Visual Bị Tác Động (Target Impacted) | Hành Vi Tương Tác (Behavior) |
| :--- | :--- | :--- |
| **Bản đồ Shape Map 63 tỉnh (Trang 1)** | Thẻ KPI 1.2A - 1.2D | Lọc dữ liệu về đúng tỉnh được click; hiển thị số liệu riêng của tỉnh. |
| **Bản đồ Shape Map 63 tỉnh (Trang 1)** | Biểu đồ đường Dual-Axis | Chuyển đường xu hướng từ Quốc gia sang Lịch sử phát thải của riêng tỉnh đó. |
| **Donut ngành IPCC (Trang 1)** | Bản đồ Shape Map & KPI | Lọc phát thải toàn quốc theo ngành (Nông nghiệp, Năng lượng...). |
| **Slicer Tỉnh thành (Trang 2)** | Gauge Hạn ngạch & Scatter Plot | Highlight vị trí của tỉnh trên ma trận 4 góc và cập nhật kim đo hạn ngạch. |
| **Slicer Tỉnh thành (Trang 2)** | Visual Giám sát Không khí 2.4 | Drill-down danh sách các trạm quan trắc không khí thuộc địa bàn tỉnh đó. |
