---
phase: 1
title: "Project Scaffolding & Environment Setup"
status: completed
priority: P1
effort: "4h"
dependencies: []
---

# Phase 1: Project Scaffolding & Environment Setup

## Overview
Thiết lập toàn bộ cấu trúc thư mục dự án cho tầng Ingestion, môi trường ảo Python và các thư viện cần thiết (`requests`, `pandas`, `openpyxl`).

## Requirements
- Functional:
  - Cấu trúc thư mục dữ liệu phân cấp rõ ràng: `data/raw/`, `data/staging/`, `data/reference/`, `scripts/`.
  - File cấu hình môi trường hoặc dependency management (`requirements.txt` / `pyproject.toml`).
- Non-functional:
  - Khả năng thực thi độc lập trên Windows PowerShell.
  - Xử lý mã hóa UTF-8 chuẩn xác cho dữ liệu tiếng Việt.

## Architecture
Tạo khung làm việc chuẩn cho pipeline dữ liệu:
```
DWH/
├── data/
│   ├── raw/               # Chứa các payload JSON & CSV thô từ API/GSO
│   ├── staging/           # Chứa các file CSV đã làm sạch sẵn sàng cho SSIS
│   └── reference/         # Chứa bảng tra cứu chuẩn (mã 63 tỉnh, danh mục ngành)
├── scripts/               # Chứa mã nguồn Python ingestion
│   └── fetch_data.py
├── plans/                 # Kế hoạch thực hiện theo chuẩn AgentKit
└── requirements.txt
```

## Related Code Files
- Create: `requirements.txt`
- Create: `scripts/utils.py`
- Create: `scripts/__init__.py`

## Implementation Steps
1. Khởi tạo cây thư mục `data/raw`, `data/staging`, `data/reference`, `scripts`.
2. Tạo file `requirements.txt` với `requests>=2.31.0`, `pandas>=2.2.0`, `openpyxl>=3.1.0`.
3. Kiểm tra môi trường Python (`python --version` hoặc `uv`).
4. Viết module phụ trợ `scripts/utils.py` chứa hàm lưu dữ liệu JSON và xuất CSV chuẩn UTF-8.

## Success Criteria
- [x] Cấu trúc thư mục `data/` và `scripts/` được tạo đầy đủ trên ổ đĩa.
- [x] Môi trường Python cài đặt thành công các gói phụ thuộc không lỗi.
- [x] Hàm helper ghi file UTF-8 kiểm thử thành công với ký tự tiếng Việt có dấu.

## Risk Assessment
- *Nguy cơ:* Lỗi Encoding trên Windows PowerShell (mặc định CP1252 hoặc CP936) làm hỏng font tiếng Việt.
- *Đối sách:* Luôn chỉ định rõ ràng `encoding='utf-8-sig'` trong các hàm mở/ghi file của Python.
