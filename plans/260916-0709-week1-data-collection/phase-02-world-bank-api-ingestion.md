---
phase: 2
title: "World Bank API Ingestion"
status: pending
priority: P1
effort: "6h"
dependencies: ["phase-01-start"]
---

# Phase 2: World Bank API Ingestion

## Overview
Xây dựng module tự động kết nối World Bank Indicators REST API, kéo toàn bộ chuỗi dữ liệu lịch sử phát thải và năng lượng vĩ mô của Việt Nam (1990–2023) và lưu về dạng bảng sạch.

## Requirements
- Functional:
  - Gọi API World Bank cho quốc gia Việt Nam (`VNM`) với phân trang (`per_page=1000`).
  - Trích xuất 5 chỉ số cốt lõi:
    1. `EN.ATM.GHGT.KT.CE`: Total GHG emissions (kt of CO2 equivalent)
    2. `EN.ATM.CO2E.KT`: CO2 emissions (kt)
    3. `EN.ATM.METH.KT.CE`: Methane emissions (kt of CO2 equivalent)
    4. `EG.FEC.RNEW.ZS`: Renewable energy consumption (% of total)
    5. `NY.GDP.MKTP.CD`: GDP (current US$)
  - Pivot các chỉ số theo từng năm thành một bảng dạng `[Year, Total_GHG_Kt, CO2_Kt, Methane_Kt, Renewable_Pct, GDP_USD]`.
- Non-functional:
  - Cơ chế retry khi mạng chập chờn (timeout 15 giây, tối đa 3 lần thử).
  - Tự động bỏ qua các năm rỗng (NULL toàn bộ).

## Architecture
```
[World Bank REST API] ──HTTP GET──> [raw_worldbank_<indicator>.json]
                                             │
                                             ▼ [scripts/fetch_worldbank.py]
                                     [data/staging/wb_national_emissions.csv]
```

## Related Code Files
- Create: `scripts/fetch_worldbank.py`
- Output: `data/raw/worldbank_raw.json`
- Output: `data/staging/wb_national_emissions.csv`

## Implementation Steps
1. Định nghĩa từ điển mã chỉ số và tên cột tương ứng.
2. Viết hàm `fetch_wb_indicator(country_code, indicator_code)`.
3. Xử lý payload JSON trả về, trích xuất `date` và `value`.
4. Hợp nhất các chỉ số theo năm (`outer join` theo `Year`), sắp xếp tăng dần theo thời gian.
5. Xuất kết quả ra `data/staging/wb_national_emissions.csv`.

## Success Criteria
- [ ] File `data/staging/wb_national_emissions.csv` được tạo với tối thiểu 30 dòng dữ liệu (từ 1990 đến 2020+).
- [ ] Không có dòng nào bị trùng lặp năm (`Year` là duy nhất).
- [ ] Dữ liệu số thực (`float`) không chứa chuỗi rỗng gây lỗi nạp SQL sau này.

## Risk Assessment
- *Nguy cơ:* World Bank chưa công bố số liệu phát thải của 1–2 năm gần nhất (ví dụ 2022-2023).
- *Đối sách:* Giữ nguyên giá trị `NULL` hợp lệ hoặc nội suy/ước tính tuyến tính có gắn cờ `Is_Estimated = 1`.
