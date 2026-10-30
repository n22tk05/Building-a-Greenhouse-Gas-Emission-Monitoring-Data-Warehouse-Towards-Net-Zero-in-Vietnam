# Từ Điển Độ Đo DAX (Power BI DAX Measures Dictionary)
**Dự án:** Hệ thống Giám Sát Phát Thải Khí Nhà Kính Hướng Tới Net-Zero Tại Việt Nam  
**Giai đoạn:** Tuần 4 - Phase 2 (DAX Measures Library & Analytical Metrics Engine)  
**File định nghĩa nguồn:** [`powerbi/dax_measures.dax`](file:///C:/Users/ADMIN/Desktop/DWH/powerbi/dax_measures.dax)

---

## 1. Danh Mục Độ Đo Cấp Quốc Gia (National Emissions Metrics)

| Tên Measure | Công thức DAX Tóm tắt | Kiểu dữ liệu & Format | Mục đích Nghiệp vụ | Visual đề xuất |
| :--- | :--- | :--- | :--- | :--- |
| `Total GHG Emissions (MtCO2e)` | `SUM(vw_Fact_National_Emissions_BI[Emissions_MtCO2e])` | Decimal (`#,##0.00 MtCO2e`) | Tổng phát thải khí nhà kính toàn quốc | KPI Card, Line Chart |
| `Total CO2 Emissions (MtCO2e)` | `SUM(vw_Fact_National_Emissions_BI[CO2_MtCO2e])` | Decimal (`#,##0.00 MtCO2`) | Tổng phát thải CO2 đơn lẻ | Area Chart, Bar Chart |
| `Total Methane Emissions (MtCO2e)` | `SUM(vw_Fact_National_Emissions_BI[Methane_MtCO2e])` | Decimal (`#,##0.00 MtCH4e`) | Phát thải khí Methane quy đổi | Area Chart |
| `National GDP (USD)` | `CALCULATE(MAX(GDP_USD), Sector_Code = "TOT")` | Currency (`$#,##0`) | **GDP sạch (Chống nhân đôi)** khi filter ngành | KPI Card, Scatter Plot |
| `National Emission Intensity` | `DIVIDE(Total GHG * 1M, GDP / 1M)` | Decimal (`#,##0.00 Tấn/Triệu USD`) | Hiệu quả phát thải trên quy mô nền kinh tế | Line Chart, KPI Card |
| `Renewable Energy Pct` | `AVERAGE(Renewable_Energy_Pct)` | Percentage (`0.0%`) | Tỷ lệ năng lượng tái tạo quốc gia | Gauge, Donut Chart |

---

## 2. Danh Mục Độ Đo Cấp Tỉnh Thành (Provincial Economics & Decoupling)

| Tên Measure | Công thức DAX Tóm tắt | Kiểu dữ liệu & Format | Mục đích Nghiệp vụ | Visual đề xuất |
| :--- | :--- | :--- | :--- | :--- |
| `Provincial Carbon Tonnes` | `SUM(vw_Fact_Provincial_Economy_BI[Estimated_Carbon_Tonnes])` | Decimal (`#,##0.00 Tấn`) | Tổng phát thải carbon ước tính của tỉnh | Map Bubble, Bar Chart |
| `Provincial GRDP (Billion VND)` | `SUM(vw_Fact_Provincial_Economy_BI[GRDP_Billion_VND])` | Decimal (`#,##0.00 Tỷ VNĐ`) | Tổng sản phẩm trên địa bàn 63 tỉnh | Map, Bar Chart |
| `Provincial Decoupling Index` | `AVERAGE(vw_Fact_Provincial_Economy_BI[Decoupling_Index])` | Decimal (`0.0000`) | Chỉ số tách rời kinh tế - môi trường Tapio | Scatter Plot, Table |
| `Carbon Intensity (Tonnes/Billion VND)` | `DIVIDE(Carbon Tonnes, GRDP)` | Decimal (`#,##0.00 Tấn/Tỷ VNĐ`) | Mức thâm dụng carbon của kinh tế địa phương | Bar Chart, Scatter Plot |
| `Carbon Per Capita (Tonnes/Person)` | `DIVIDE(Carbon Tonnes, Population)` | Decimal (`#,##0.00 Tấn/Người`) | Phát thải carbon bình quân đầu người | Map Choropleth |
| `Carbon Density (Tonnes/Km2)` | `DIVIDE(Carbon Tonnes, Area_Km2)` | Decimal (`#,##0.00 Tấn/Km²`) | Mật độ phát thải theo diện tích tự nhiên | Map Choropleth |
| `Forest Coverage Pct` | `AVERAGE(vw_Fact_Provincial_Economy_BI[Forest_Coverage_Pct])` | Percentage (`0.0%`) | Tỷ lệ che phủ rừng ("Lá chắn xanh") | Scatter Plot, Matrix |

---

## 3. Danh Mục Giám Sát Không Khí Big Data 2024 (1.66 Triệu Dòng)

| Tên Measure | Công thức DAX Tóm tắt | Kiểu dữ liệu & Format | Mục đích Nghiệp vụ | Visual đề xuất |
| :--- | :--- | :--- | :--- | :--- |
| `Avg AQI Index` | `AVERAGE(vw_Fact_Hourly_Air_Monitoring_BI[AQI_Index])` | Integer (`#,##0`) | Chỉ số chất lượng không khí trung bình | KPI Card, Gauge |
| `Avg PM2.5 (ug/m3)` | `AVERAGE(vw_Fact_Hourly_Air_Monitoring_BI[PM25_ug_m3])` | Decimal (`#,##0.0 µg/m³`) | Nồng độ bụi mịn PM2.5 trung bình | Line Chart, Area Chart |
| `Avg CO2 Concentration (ppm)` | `AVERAGE(vw_Fact_Hourly_Air_Monitoring_BI[CO2_ppm])` | Decimal (`#,##0.0 ppm`) | Nồng độ CO2 tức thời tại các trạm | Line Chart |
| `Exceeding QCVN Hours` | `SUM(vw_Fact_Hourly_Air_Monitoring_BI[Is_Exceeding_QCVN])` | Integer (`#,##0 Giờ`) | Tổng số giờ không khí vi phạm quy chuẩn QCVN | KPI Card, Bar Chart |
| `Exceeding QCVN Rate %` | `DIVIDE(Exceeding Hours, Total Hours)` | Percentage (`0.0%`) | Tỷ lệ % thời gian không khí bị ô nhiễm | Gauge, Donut Chart |
| `Rush Hour Exceeding Hours` | `CALCULATE(Exceeding Hours, Is_Rush_Hour = 1)` | Integer (`#,##0 Giờ`) | Số giờ ô nhiễm trong khung giờ cao điểm | Clustered Column Chart |

---

## 4. Danh Mục Time Intelligence & Xu Hướng (Time Intelligence & CAGR)

| Tên Measure | Công thức DAX Tóm tắt | Kiểu dữ liệu & Format | Mục đích Nghiệp vụ | Visual đề xuất |
| :--- | :--- | :--- | :--- | :--- |
| `Emissions Prior Year` | `CALCULATE(Total GHG, SAMEPERIODLASTYEAR(Year_Date))` | Decimal (`#,##0.00 MtCO2e`) | Phát thải năm trước liền kề | Tooltip, KPI Card |
| `Emissions YoY Growth %` | `DIVIDE(Total GHG - Prior, Prior)` | Percentage (`+0.0%;-0.0%`) | Tăng trưởng phát thải so với cùng kỳ (%) | KPI Indicator, Watermark |
| `GRDP Prior Year` | `CALCULATE(GRDP, SAMEPERIODLASTYEAR(Year_Date))` | Decimal (`#,##0.00 Tỷ VNĐ`) | GRDP năm trước liền kề | Tooltip |
| `GRDP YoY Growth %` | `DIVIDE(GRDP - Prior, Prior)` | Percentage (`+0.0%;-0.0%`) | Tăng trưởng kinh tế so với cùng kỳ (%) | KPI Indicator |
| `5-Year Emissions CAGR %` | `((Current / Base5Year) ^ (1/5)) - 1` | Percentage (`+0.0%;-0.0%`) | Tốc độ tăng trưởng kép phát thải 5 năm | Line Trend, KPI |

---

## 5. Danh Mục Lộ Trình Net-Zero 2030 / 2050 (Net-Zero Trajectory & Gap)

| Tên Measure | Công thức DAX Tóm tắt | Kiểu dữ liệu & Format | Mục đích Nghiệp vụ | Visual đề xuất |
| :--- | :--- | :--- | :--- | :--- |
| `Baseline 2020 Emissions` | `CALCULATE(Total GHG, Year = 2020)` | Decimal (`#,##0.00 MtCO2e`) | Mức phát thải cơ sở năm 2020 | Target Reference Line |
| `Target Emission 2030 (NDC)`| `Baseline 2020 * (1 - 0.435)` | Decimal (`#,##0.00 MtCO2e`) | Mục tiêu phát thải tối đa năm 2030 (NDC) | Target Reference Line |
| `NetZero 2030 Target Gap (MtCO2e)` | `Total GHG - Target Emission 2030` | Decimal (`+#,##0.00;-#,##0.00`) | Khoảng cách cần cắt giảm để đạt NDC | Bullet Chart, Waterfall |
| `Provincial Quota 2030` | `Target National * (GRDP / Total GRDP)` | Decimal (`#,##0.00 Tấn`) | Hạn ngạch carbon phân bổ cho từng tỉnh | Bar Chart, Table |
| `Quota Realization %` | `DIVIDE(Carbon Tonnes, Quota 2030)` | Percentage (`0.0%`) | Tỷ lệ sử dụng hạn ngạch phát thải (%) | Gauge, Heatmap |

---

## 6. Danh Mục Trực Quan Hóa Động (Dynamic Formatting & Visual Helpers)

| Tên Measure | Giá trị trả về | Mục đích Nghiệp vụ | Ứng dụng trong Power BI |
| :--- | :--- | :--- | :--- |
| `Decoupling Color Hex` | `#10B981` (Xanh), `#F59E0B` (Vàng), `#EF4444` (Đỏ) | Màu sắc động theo trạng thái tách rời kinh tế | Conditional Formatting cho Map & Bar |
| `Decoupling Status Label` | Chuỗi văn bản tiếng Việt mô tả trạng thái Tapio | Hiển thị nhãn chi tiết trên Tooltip | Card Visual, Table, Tooltip |
| `AQI Status Color Hex` | `#10B981`, `#F59E0B`, `#F97316`, `#EF4444`, `#8B5CF6` | Màu sắc chuẩn thang đo AQI Việt Nam | Conditional Formatting cho Slicer & Gauge |
| `Dynamic Card Title` | Chuỗi: `"Báo cáo Phát thải & Kinh tế Xanh: " & Province` | Tiêu đề thay đổi tự động khi chọn Slicer | Card Visual Header |
| `Dynamic KPI Subtitle` | Chuỗi: Cảnh báo dư địa hoặc vượt trần NDC 2030 | Phụ đề thông minh cho KPI Card | KPI Card Subtitle |
