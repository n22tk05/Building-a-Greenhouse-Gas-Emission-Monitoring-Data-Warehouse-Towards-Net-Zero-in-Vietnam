# Báo Cáo Đánh Giá & Kiểm Định Chất Lượng Dữ Liệu (Data Profiling & Quality Gate)

**Dự án:** Vietnam Greenhouse Gas Emission Monitoring Data Warehouse Towards Net-Zero  
**Thời điểm tạo:** 2026-09-26 21:41:24  
**Trạng thái kiểm định:** 🟢 **PASSED - READY FOR DWH STAGE 2**  

---

## 1. Tổng Quan Kiểm Định (Validation Executive Summary)

Hệ thống đã thực hiện kiểm định 4 tiêu chí chất lượng dữ liệu cốt lõi (Completeness, Consistency, Referential Integrity, Uniqueness & Validity) trên toàn bộ các tệp dữ liệu đã nạp tại `data/staging/` và `data/reference/`.

| Tiêu chuẩn kiểm định | Kết quả | Mô tả tóm tắt |
|---|:---:|---|
| **1. Completeness (Độ đầy đủ)** | ✅ PASS | Tỷ lệ NULL trên các cột đo lường chính đều < 5.0% |
| **2. Consistency (Tính nhất quán thời gian)** | ✅ PASS | Khoảng thời gian chung 2015–2023 đồng bộ trên cả 3 nguồn (9 năm) |
| **3. Referential Integrity (Toàn vẹn tham chiếu)** | ✅ PASS | 100% mã tỉnh (63/63 tỉnh) trong dữ liệu kinh tế khớp chính xác với danh mục chuẩn |
| **4. Grain & Uniqueness (Độ chi tiết & Khóa duy nhất)** | ✅ PASS | 0 bản ghi trùng lặp khóa tự nhiên trên toàn bộ các tập dữ liệu |
| **5. Value Validity (Miền giá trị hợp lệ)** | ✅ PASS | Các trường đo lường phát thải, dân số, GRDP và tỷ lệ che phủ rừng đạt chuẩn logic |

---

## 2. Chi Tiết Độ Đầy Đủ Dữ Liệu (Completeness Metrics)

Kiểm tra tỷ lệ thiếu dữ liệu (NULL / Missing values) trên các trường dữ liệu bắt buộc:

| Tập dữ liệu | Cột kiểm tra | Số lượng NULL | Tỷ lệ NULL (%) | Đánh giá (< 5%) |
|---|---|:---:|:---:|:---:|
| `wb_national_emissions` | `Year` | 0 | 0.0% | ✅ PASS |
| `wb_national_emissions` | `CO2_MtCO2e` | 1 | 1.79% | ✅ PASS |
| `wb_national_emissions` | `Total_GHG_MtCO2e` | 1 | 1.79% | ✅ PASS |
| `wb_national_emissions` | `Methane_MtCO2e` | 1 | 1.79% | ✅ PASS |
| `cw_sector_emissions` | `Year` | 0 | 0.0% | ✅ PASS |
| `cw_sector_emissions` | `Sector_Code` | 0 | 0.0% | ✅ PASS |
| `cw_sector_emissions` | `Gas` | 0 | 0.0% | ✅ PASS |
| `cw_sector_emissions` | `Emissions_MtCO2e` | 0 | 0.0% | ✅ PASS |
| `gso_provincial_economy` | `Year` | 0 | 0.0% | ✅ PASS |
| `gso_provincial_economy` | `Province_Code` | 0 | 0.0% | ✅ PASS |
| `gso_provincial_economy` | `GRDP_Billion_VND` | 0 | 0.0% | ✅ PASS |
| `gso_provincial_economy` | `Population` | 0 | 0.0% | ✅ PASS |
| `gso_provincial_economy` | `Estimated_Carbon_Tonnes` | 0 | 0.0% | ✅ PASS |
| `dim_provinces_master` | `Province_Code` | 0 | 0.0% | ✅ PASS |
| `dim_provinces_master` | `Province_Name` | 0 | 0.0% | ✅ PASS |
| `dim_provinces_master` | `Region` | 0 | 0.0% | ✅ PASS |
| `dim_provinces_master` | `Economic_Zone` | 0 | 0.0% | ✅ PASS |
| `dim_provinces_master` | `Area_Km2` | 0 | 0.0% | ✅ PASS |

---

## 3. Tính Nhất Quán & Giao Thoa Thời Gian (Temporal Consistency)

- **World Bank (wb_national_emissions):** 1970 – 2025
- **ClimateWatch (cw_sector_emissions):** 1990 – 2023
- **Tổng cục Thống kê GSO (gso_provincial_economy):** 2015 – 2024
- **Giai đoạn giao thoa đồng bộ (3 nguồn):** 2015 – 2023 (9 năm liên tục)

*Nhận định:* Dữ liệu hoàn toàn đảm bảo tính xuyên suốt cho giai đoạn phân tích trọng điểm tiến trình Net-Zero của Việt Nam (2015–2023).

---

## 4. Tính Toàn Vẹn Tham Chiếu Tỉnh Thành (Referential Integrity)

- **Số lượng tỉnh thành trong danh mục chuẩn (`dim_provinces_master`):** 63
- **Số lượng mã tỉnh xuất hiện trong dữ liệu kinh tế (`gso_provincial_economy`):** 63
- **Số mã không khớp (Unmatched):** 0
- **Tỷ lệ khớp:** 100% (63/63 tỉnh thành phố trực thuộc Trung ương)

---

## 5. Kiểm Tra Khóa Tự Nhiên & Độ Trùng Lặp (Natural Keys Uniqueness)

| Bảng dữ liệu | Khóa tự nhiên xác định (Natural Key) | Số bản ghi trùng lặp | Kết luận |
|---|---|:---:|:---:|
| `wb_national_emissions` | `[Year]` | 0 | ✅ Duy nhất |
| `cw_sector_emissions` | `[Year, Sector_Code, Gas]` | 0 | ✅ Duy nhất |
| `gso_provincial_economy` | `[Year, Province_Code]` | 0 | ✅ Duy nhất |
| `dim_provinces_master` | `[Province_Code]` | 0 | ✅ Duy nhất |

---

## 6. Thống Kê Mô Tả Dữ Liệu Trọng Tâm (Summary Statistics)

### World Bank National Emissions
- **Tổng phát thải quốc gia (Total GHG MtCO2e):**
  - Nhỏ nhất (Min): 62.68 MtCO2e
  - Lớn nhất (Max): 584.26 MtCO2e
  - Trung bình (Mean): 198.71 MtCO2e
  - Trung vị (Median): 139.37 MtCO2e
- **Phát thải CO2 riêng biệt (CO2 MtCO2e):**
  - Min: 13.56 | Max: 430.82 | Mean: 101.48 MtCO2e

### ClimateWatch Sector Emissions
- **Phát thải phân bổ theo ngành (Emissions MtCO2e):**
  - Min: 0.09 MtCO2e
  - Max: 486.04 MtCO2e
  - Mean: 63.10 MtCO2e

### GSO Provincial Economy & Estimated Carbon
- **GRDP cấp tỉnh (Tỷ VNĐ):**
  - Min: 4,266.57 tỷ VNĐ
  - Max: 1,765,279.05 tỷ VNĐ
  - Mean: 113,538.62 tỷ VNĐ
- **Ước tính phát thải carbon cấp tỉnh (Tấn CO2e):**
  - Min: 272,000 tấn
  - Max: 144,070,000 tấn
  - Mean: 10,527,070 tấn

---

## 7. Kết Luận & Cổng Kiểm Soát Chất Lượng (Quality Gate Decision)

> [!NOTE]  
> Toàn bộ 4 tập dữ liệu đã vượt qua 100% các tiêu chí kiểm tra kỹ thuật và logic nghiệp vụ. Các tập tin CSV tại `data/staging/` và `data/reference/` đã đạt chất lượng chuẩn để tiến hành nạp vào mô hình dữ liệu quan hệ (Relational Staging Tables) trên SQL Server ở Tuần 2.
