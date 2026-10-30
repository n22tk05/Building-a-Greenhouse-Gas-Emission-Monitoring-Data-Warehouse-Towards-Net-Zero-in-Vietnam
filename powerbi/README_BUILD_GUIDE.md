# Hướng Dẫn Dựng & Vận Hành Dashboard Power BI (Build Runbook)

Tài liệu này hướng dẫn chi tiết từng bước kết nối dữ liệu từ SQL Server, import theme màu, nạp bản đồ TopoJSON 63 tỉnh thành và kéo thả các visual trên **Microsoft Power BI Desktop**.

---

## 1. Yêu Cầu Môi Trường (Prerequisites)
1. **Microsoft Power BI Desktop** (Bản phát hành từ năm 2023 trở về sau).
2. **Microsoft SQL Server** đang chạy trên máy local (`localhost`), database `NetZero_VN_DWH`.
3. Bật tính năng **Shape map visual** trong Power BI:
   - Vào menu: `File` $\rightarrow$ `Options and settings` $\rightarrow$ `Options`.
   - Chọn mục `Preview features` $\rightarrow$ Tích chọn ô `Shape map visual` $\rightarrow$ Nhấn `OK` và khởi động lại Power BI Desktop nếu được yêu cầu.

---

## 2. Bước 1: Kết Nối CSDL & Nạp Mô Hình Ngữ Nghĩa (Data Ingestion)
1. Trong Power BI Desktop, chọn `Get data` $\rightarrow$ `SQL Server`.
2. Điền thông tin:
   - **Server:** `localhost` (hoặc tên máy tính của bạn).
   - **Database:** `NetZero_VN_DWH`.
   - **Data Connectivity mode:** Chọn `Import` (hoặc chọn `DirectQuery` cho bảng Big Data 1.66M dòng).
3. Trong cửa sổ Navigator, chọn 8 Views thuộc schema `dwh`:
   - `vw_Dim_Date_BI`
   - `vw_Dim_Province_Geo_BI`
   - `vw_Dim_Sector_Hierarchy_BI`
   - `vw_Dim_Station_BI`
   - `vw_Dim_Time_Of_Day_BI`
   - `vw_Fact_National_Emissions_BI`
   - `vw_Fact_Provincial_Economy_BI`
   - `vw_Fact_Hourly_Air_Monitoring_BI`
4. Nhấn `Load`.

---

## 3. Bước 2: Nạp Thư Viện DAX Measures
1. Tạo một bảng rỗng để chứa toàn bộ Measures:
   - Vào tab `Home` $\rightarrow$ `Enter Data`.
   - Đặt tên bảng: `_Measures` $\rightarrow$ Nhấn `Load`.
2. Mở file [`powerbi/dax_measures.dax`](file:///C:/Users/ADMIN/Desktop/DWH/powerbi/dax_measures.dax) bằng Notepad hoặc VS Code.
3. Lần lượt nhấn `New Measure` trong Power BI Desktop, copy từng đoạn mã DAX dán vào thanh công thức và định dạng Format String theo hướng dẫn trong [`docs/dax_measures_dictionary.md`](file:///C:/Users/ADMIN/Desktop/DWH/docs/dax_measures_dictionary.md).

---

## 4. Bước 3: Áp Dụng Theme Màu Net-Zero Emerald
1. Trên thanh công cụ Power BI Desktop, vào tab `View`.
2. Nhấn vào mũi tên mở rộng ở phần **Themes** $\rightarrow$ Chọn `Browse for themes`.
3. Trỏ tới file: [`powerbi/theme_netzero.json`](file:///C:/Users/ADMIN/Desktop/DWH/powerbi/theme_netzero.json).
4. Toàn bộ nền trang, bảng màu mặc định và font chữ sẽ tự động chuyển sang phong cách **Dark Slate & Emerald Green** chuyên nghiệp.

---

## 5. Bước 4: Tạo Visual Bản Đồ 63 Tỉnh Thành (Shape Map)
1. Thêm một visual `Shape map` vào Trang 1.
2. Kéo trường `vw_Dim_Province_Geo_BI[Province_Code]` vào ô **Location**.
3. Kéo measure `[Provincial Decoupling Index]` vào ô **Color saturation**.
4. Cấu hình hình dạng bản đồ:
   - Trong bảng **Format visual**, chọn mục `Map settings`.
   - Tại dòng **Map type**, chọn `Custom map`.
   - Nhấn nút `Browse...` $\rightarrow$ Chọn tệp [`data/reference/vietnam_provinces.topojson`](file:///C:/Users/ADMIN/Desktop/DWH/data/reference/vietnam_provinces.topojson).
5. Ngay lập tức hình dạng dải đất chữ S của Việt Nam với đầy đủ 63 tỉnh thành sẽ hiển thị rõ nét!

---

## 6. Bước 5: Bố Cục 2 Trang Dashboard Hoàn Chỉnh
* Thực hiện sắp xếp các visual, slicer và thẻ thông tin theo đúng sơ đồ tọa độ và đặc tả chi tiết trong tài liệu:  
  👉 [`docs/powerbi_dashboard_specification.md`](file:///C:/Users/ADMIN/Desktop/DWH/docs/powerbi_dashboard_specification.md)
