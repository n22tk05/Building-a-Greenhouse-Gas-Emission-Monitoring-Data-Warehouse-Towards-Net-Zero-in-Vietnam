---
phase: 5
title: "Data Profiling & Quality Validation Gate"
status: pending
priority: P1
effort: "4h"
dependencies: ["phase-02-world-bank-api-ingestion", "phase-03-climatewatch-sector-ingestion", "phase-04-gso-provincial-data-preparation"]
---

# Phase 5: Data Profiling & Quality Validation Gate

## Overview
Tiến hành kiểm tra chất lượng dữ liệu (Data Profiling & Quality Assurance) trên toàn bộ 3 tập file đầu ra trước khi chuyển giao sang Tuần 2 (Thiết kế CSDL SQL Server và nạp Staging).

## Requirements
- Functional:
  - Viết script kiểm thử tự động `scripts/verify_datasets.py`.
  - Kiểm tra các tiêu chuẩn chất lượng dữ liệu:
    1. **Completeness (Độ đầy đủ):** Tỷ lệ giá trị NULL trong các cột đo lường quan trọng phải < 5%.
    2. **Consistency (Tính nhất quán):** Cột `Year` trong cả 3 tập dữ liệu phải có khoảng giao thoa hợp lệ (ví dụ: 2015–2022).
    3. **Integrity (Tính toàn vẹn tham chiếu):** Mọi mã tỉnh trong bảng kinh tế phải tồn tại trong danh mục `dim_provinces_master`.
    4. **Grain Validation (Kiểm tra mức độ chi tiết):** Không có bản ghi nào bị trùng lặp khóa tự nhiên (Natural Keys).
- Non-functional:
  - Xuất báo cáo tóm tắt chất lượng dữ liệu dạng Markdown hoặc Console log rõ ràng.

## Architecture
```
[data/staging/*.csv] ──> [scripts/verify_datasets.py] ──> [Báo cáo Quality PASS / FAIL]
                                                                      │
                                                                      ▼
                                                            [Gate mở khóa Tuần 2]
```

## Related Code Files
- Create: `scripts/verify_datasets.py`
- Output: `data/data_profiling_report.md`

## Implementation Steps
1. Đọc các file CSV từ thư mục `data/staging/` và `data/reference/`.
2. Kiểm tra số lượng dòng, số lượng cột, kiểu dữ liệu thực tế của từng cột.
3. Đếm số lượng giá trị NULL, số lượng giá trị âm hoặc bất thường (Outliers).
4. Kiểm tra phép nối (Join test) giữa bảng tỉnh thành và bảng kinh tế.
5. Tạo báo cáo tóm tắt số liệu (`Summary Statistics`: Min, Max, Mean phát thải và GRDP).

## Success Criteria
- [ ] Script `verify_datasets.py` chạy thành công với trạng thái `ALL CHECKS PASSED`.
- [ ] 63/63 tỉnh thành khớp mã tham chiếu 100%.
- [ ] Báo cáo `data_profiling_report.md` được tạo để đưa vào Chương 2 của báo cáo đồ án.

## Risk Assessment
- *Nguy cơ:* Xuất hiện độ lệch lớn giữa các nguồn dữ liệu khác nhau.
- *Đối sách:* Ghi nhận rõ ràng độ lệch trong báo cáo và đưa ra giải pháp chuẩn hóa thống nhất trong tài liệu thuyết minh.
