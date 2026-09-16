---
phase: 4
title: "GSO Provincial Data Preparation"
status: pending
priority: P1
effort: "8h"
dependencies: ["phase-01-start"]
---

# Phase 4: GSO Provincial Data Preparation

## Overview
Xây dựng tập dữ liệu kinh tế - xã hội chuẩn tắc cho 63 tỉnh thành Việt Nam (GRDP, dân số, diện tích, vùng kinh tế) từ niên giám thống kê Tổng cục Thống kê (GSO) và tạo bảng từ điển danh mục tỉnh thành.

## Requirements
- Functional:
  - Chuẩn hóa danh mục 63 tỉnh thành Việt Nam kèm mã hành chính quốc gia (01 Hà Nội, 79 TP.HCM...).
  - Bổ sung phân vùng địa lý: Vùng kinh tế (Đồng bằng sông Hồng, Đông Nam Bộ, Tây Nguyên...) và Vùng kinh tế trọng điểm (KTTĐ Bắc Bộ, KTTĐ Phía Nam...).
  - Thu thập chuỗi số liệu GRDP (tỷ đồng), Dân số (người), Tỷ lệ che phủ rừng (%) của 63 tỉnh qua các năm (2015–2023).
  - Ước lượng lượng carbon phát thải địa phương (`Estimated_Carbon_Tonnes`) dựa trên hệ số tiêu thụ năng lượng và quy mô công nghiệp của từng tỉnh.
- Non-functional:
  - Xử lý triệt để các biến thể tên tỉnh (ví dụ: "Hồ Chí Minh", "TP. Hồ Chí Minh", "TP.HCM").
  - Lưu file mã hóa UTF-8 with BOM (`utf-8-sig`) để SSIS và Excel không bị lỗi font tiếng Việt.

## Architecture
```
[Niên Giám GSO / Thống kê mở] ──> [scripts/clean_gso_data.py]
                                            │
                                            ├─> [data/reference/dim_provinces_master.csv]
                                            └─> [data/staging/gso_provincial_economy.csv]
```

## Related Code Files
- Create: `scripts/clean_gso_data.py`
- Output: `data/reference/dim_provinces_master.csv`
- Output: `data/staging/gso_provincial_economy.csv`

## Implementation Steps
1. Khởi tạo danh mục chuẩn 63 tỉnh thành kèm mã tỉnh, tên không dấu, tên có dấu, và vùng miền.
2. Viết script đọc dữ liệu thống kê GSO (hoặc tổng hợp bảng số liệu GRDP từ niên giám).
3. Làm sạch số liệu: chuyển đổi định dạng số (xóa dấu phẩy, chuyển chuỗi sang số thực), điền giá trị thiếu.
4. Tính toán sơ bộ chỉ số phát thải ước tính của từng tỉnh theo tỷ trọng công nghiệp.
5. Xuất ra 2 file CSV sạch sẵn sàng làm đầu vào cho `Dim_Province` và `Fact_Provincial_Economy`.

## Success Criteria
- [ ] Danh mục tỉnh chuẩn có chính xác 63 dòng, không thiếu hoặc trùng tỉnh nào.
- [ ] Bảng kinh tế cấp tỉnh có đầy đủ số liệu GRDP, dân số của 63 tỉnh cho giai đoạn nghiên cứu.
- [ ] Tên tỉnh khớp 100% với tên trên file bản đồ `vietnam_provinces.topojson` dùng cho Power BI.

## Risk Assessment
- *Nguy cơ:* Một số tỉnh có số liệu thống kê bị khuyết năm hoặc thay đổi cách tính GRDP (năm so sánh).
- *Đối sách:* Chuẩn hóa toàn bộ GRDP về cùng một mặt bằng giá hiện hành (current prices) và ghi chú rõ trong metadata.
