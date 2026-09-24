import os
import sys
import unittest
from pathlib import Path

# Đảm bảo thư mục gốc dự án nằm trong sys.path khi chạy trực tiếp
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from scripts.utils import DATA_DIR, STAGING_DIR, REFERENCE_DIR
from scripts.verify_datasets import (
    load_datasets,
    check_completeness,
    check_consistency,
    check_referential_integrity,
    check_grain_uniqueness,
    check_value_validity,
    generate_summary_statistics,
    run_verification,
    REPORT_FILE
)

class TestPhase5DataProfilingAndQualityGate(unittest.TestCase):
    def setUp(self):
        self.df_wb, self.df_cw, self.df_econ, self.df_dim = load_datasets()

    def test_load_datasets(self):
        """Kiểm tra việc nạp dữ liệu từ các file CSV staging và reference."""
        self.assertGreater(len(self.df_wb), 0, "Dữ liệu World Bank không được rỗng")
        self.assertGreater(len(self.df_cw), 0, "Dữ liệu ClimateWatch không được rỗng")
        self.assertEqual(len(self.df_econ), 630, "Dữ liệu kinh tế GSO phải đủ 630 dòng (63 tỉnh x 10 năm)")
        self.assertEqual(len(self.df_dim), 63, "Danh mục tỉnh thành phải đúng 63 tỉnh thành")

    def test_completeness_gate(self):
        """Kiểm tra cổng độ đầy đủ: tỷ lệ NULL các cột đo lường chính < 5%."""
        result = check_completeness(self.df_wb, self.df_cw, self.df_econ, self.df_dim)
        self.assertTrue(result["status"], "Tất cả các cột đo lường chính phải có tỷ lệ NULL < 5%")

    def test_consistency_gate(self):
        """Kiểm tra tính nhất quán về mốc thời gian giao thoa."""
        result = check_consistency(self.df_wb, self.df_cw, self.df_econ)
        self.assertTrue(result["status"], "Khoảng thời gian giao thoa phải hợp lệ")
        self.assertGreaterEqual(result["common_year_count"], 5, "Cần ít nhất 5 năm giao thoa đồng bộ")
        self.assertIn(2015, result["common_years"])
        self.assertIn(2022, result["common_years"])
        self.assertIn(2023, result["common_years"])

    def test_referential_integrity_gate(self):
        """Kiểm tra tính toàn vẹn tham chiếu 100% giữa bảng kinh tế và danh mục chuẩn."""
        result = check_referential_integrity(self.df_econ, self.df_dim)
        self.assertTrue(result["status"], "100% mã tỉnh phải khớp với danh mục chuẩn")
        self.assertEqual(len(result["unmatched_codes"]), 0, "Không được có mã tỉnh nào không khớp")
        self.assertEqual(result["dim_provinces_count"], 63)
        self.assertEqual(result["econ_provinces_count"], 63)

    def test_grain_uniqueness_gate(self):
        """Kiểm tra mức độ chi tiết và tính duy nhất của khóa tự nhiên (0 duplicates)."""
        result = check_grain_uniqueness(self.df_wb, self.df_cw, self.df_econ, self.df_dim)
        self.assertTrue(result["status"], "Không được có bản ghi nào bị trùng lặp khóa tự nhiên")
        for key, count in result["duplicates"].items():
            self.assertEqual(count, 0, f"Khóa {key} bị trùng lặp {count} bản ghi")

    def test_value_validity_gate(self):
        """Kiểm tra tính hợp lệ của miền giá trị logic."""
        result = check_value_validity(self.df_wb, self.df_cw, self.df_econ)
        self.assertTrue(result["status"], "Các giá trị phát thải, dân số, GRDP phải hợp lệ logic")

    def test_summary_statistics(self):
        """Kiểm tra việc trích xuất các thông số thống kê mô tả cốt lõi."""
        stats = generate_summary_statistics(self.df_wb, self.df_cw, self.df_econ)
        self.assertIn("wb", stats)
        self.assertIn("cw", stats)
        self.assertIn("econ", stats)
        self.assertGreater(stats["wb"]["Total_GHG_MtCO2e"]["max"], 0)
        self.assertGreater(stats["econ"]["GRDP_Billion_VND"]["mean"], 0)

    def test_run_verification_and_report_generation(self):
        """Kiểm tra quy trình chạy tổng thể và tạo báo cáo markdown."""
        passed = run_verification()
        self.assertTrue(passed, "Quy trình kiểm định tổng thể phải trả về True (ALL PASSED)")
        self.assertTrue(REPORT_FILE.exists(), f"File báo cáo {REPORT_FILE} phải tồn tại")
        
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("PASSED - READY FOR DWH STAGE 2", content)
        self.assertIn("Total_GHG_MtCO2e", content)
        self.assertIn("dim_provinces_master", content)

if __name__ == "__main__":
    unittest.main()
