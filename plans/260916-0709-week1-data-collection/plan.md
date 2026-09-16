---
title: "Week 1: Data Collection & Preparation (Net-Zero Vietnam DWH)"
description: "Kế hoạch chi tiết Tuần 1: Khởi tạo môi trường, xây dựng script Python tự động thu thập dữ liệu phát thải từ World Bank, ClimateWatch API, chuẩn hóa dữ liệu kinh tế 63 tỉnh thành từ GSO và kiểm thử chất lượng dữ liệu."
status: pending
priority: P1
effort: "28h"
tags: ["dwh", "net-zero", "data-collection", "python", "etl", "week-1"]
created: 2026-09-16
---

# Kế Hoạch Tuần 1: Thu Thập & Chuẩn Bị Dữ Liệu Nguồn (Data Collection & Preparation)

## Overview
Tuần 1 là nền móng cốt lõi cho toàn bộ đồ án Data Warehouse. Mục tiêu là xây dựng các script Python tự động kết nối API mở quốc tế (World Bank, ClimateWatch) và xử lý niên giám thống kê Tổng cục Thống kê (GSO), tạo ra 3 tập dữ liệu nguồn chuẩn hóa (`.csv`) đặt tại `data/staging/` để sẵn sàng nạp vào SQL Server trong Tuần 2.

## Goals

| # | Goal | Priority |
|---|------|----------|
| 1 | Thiết lập cấu trúc thư mục chuẩn và môi trường Python Ingestion | P1 |
| 2 | Thu thập tự động dữ liệu phát thải & năng lượng quốc gia từ World Bank API (1990–2023) | P1 |
| 3 | Thu thập dữ liệu phát thải phân bổ theo ngành từ ClimateWatch API | P1 |
| 4 | Xây dựng danh mục chuẩn 63 tỉnh thành và số liệu GRDP, dân số từ GSO | P1 |
| 5 | Thực hiện Data Profiling & Quality Gate đảm bảo dữ liệu sạch 100% trước Tuần 2 | P1 |

## Phases

| # | Phase | Effort | Status |
|---|-------|:------:|:------:|
| 1 | [Phase 1: Project Scaffolding & Environment Setup](./phase-01-start.md) | 4h | Completed |
| 2 | [Phase 2: World Bank API Ingestion](./phase-02-world-bank-api-ingestion.md) | 6h | Pending |
| 3 | [Phase 3: ClimateWatch Sector Ingestion](./phase-03-climatewatch-sector-ingestion.md) | 6h | Pending |
| 4 | [Phase 4: GSO Provincial Data Preparation](./phase-04-gso-provincial-data-preparation.md) | 8h | Pending |
| 5 | [Phase 5: Data Profiling & Quality Validation Gate](./phase-05-data-profiling-and-validation-gate.md) | 4h | Pending |

## Success Criteria

- [ ] Cấu trúc thư mục `data/raw/`, `data/staging/`, `data/reference/`, `scripts/` được tạo đầy đủ.
- [ ] Script Python gọi thành công World Bank API và xuất file `wb_national_emissions.csv`.
- [ ] Script Python gọi thành công ClimateWatch API và xuất file `cw_sector_emissions.csv`.
- [ ] File danh mục 63 tỉnh thành `dim_provinces_master.csv` và dữ liệu kinh tế `gso_provincial_economy.csv` được chuẩn hóa UTF-8.
- [ ] Script `verify_datasets.py` vượt qua tất cả bài test chất lượng dữ liệu (NULL < 5%, 0 bản ghi trùng lặp khóa, mã tỉnh khớp 100%).

<!-- slug: week1-data-collection -->