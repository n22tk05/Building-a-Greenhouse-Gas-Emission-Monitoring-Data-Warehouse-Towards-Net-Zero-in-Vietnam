---
phase: 3
title: "ClimateWatch Sector Ingestion"
status: pending
priority: P1
effort: "6h"
dependencies: ["phase-01-start"]
---

# Phase 3: ClimateWatch Sector Ingestion

## Overview
Thu thập dữ liệu phát thải khí nhà kính phân rã theo ngành kinh tế (Sectors: Năng lượng, Giao thông, Công nghiệp, Nông nghiệp, Rác thải) từ ClimateWatch Data API để nạp vào bảng Fact phát thải đa ngành.

## Requirements
- Functional:
  - Gửi request đến ClimateWatch historical emissions API cho quốc gia Việt Nam (`regions=VNM`).
  - Phân loại phát thải theo 5 nhóm ngành chính:
    1. `Energy` (Điện & Nhiệt điện)
    2. `Industrial Processes` (Xi măng, Thép, Hóa chất)
    3. `Agriculture` (Trồng trọt lúa nước, Chăn nuôi)
    4. `Transportation` (Giao thông đường bộ, thủy, hàng không)
    5. `Waste` (Xử lý chất thải rắn & nước thải)
  - Chuẩn hóa đơn vị đo về triệu tấn CO2e (`MtCO2e`) hoặc nghìn tấn (`kt CO2e`).
- Non-functional:
  - Khớp nối trường thời gian `Year` đồng nhất với bảng World Bank.

## Architecture
```
[ClimateWatch API] ──GET JSON──> [scripts/fetch_climatewatch.py]
                                              │
                                              ▼
                                 [data/staging/cw_sector_emissions.csv]
                                 (Year, Sector, Gas, Emissions_MtCO2e)
```

## Related Code Files
- Create: `scripts/fetch_climatewatch.py`
- Output: `data/staging/cw_sector_emissions.csv`

## Implementation Steps
1. Xây dựng hàm gọi endpoint ClimateWatch: `https://www.climatewatchdata.org/api/v1/data/historical_emissions?regions=VNM&source=CAIT`.
2. Lọc các bản ghi theo nguồn phát thải chính thức (CAIT / GHG Protocol).
3. Làm phẳng cấu trúc JSON lồng nhau (Flatten nested JSON arrays).
4. Ánh xạ (mapping) tên ngành tiếng Anh sang mã ngành chuẩn phục vụ `Dim_Sector`.
5. Xuất kết quả ra `data/staging/cw_sector_emissions.csv`.

## Success Criteria
- [ ] Bảng dữ liệu có đầy đủ 5 phân ngành chính cho từng năm.
- [ ] Tổng phát thải các ngành cộng lại xấp xỉ tương đương với tổng phát thải quốc gia từ World Bank (độ lệch < 5%).
- [ ] Chuẩn hóa sẵn mã ngành (`Sector_Code`: `ENG`, `IND`, `AGR`, `TRA`, `WST`).

## Risk Assessment
- *Nguy cơ:* Cấu trúc JSON của ClimateWatch có thể thay đổi tham số lọc theo thời gian.
- *Đối sách:* Có sẵn file backup JSON cục bộ `data/reference/climatewatch_fallback.json` phòng khi API bảo trì.
