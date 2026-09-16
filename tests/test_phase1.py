import sys
import unittest
from pathlib import Path
import pandas as pd

from scripts.utils import (
    DATA_DIR, RAW_DIR, STAGING_DIR, REFERENCE_DIR,
    save_json, load_json, save_csv, ensure_directories
)

class TestPhase1Scaffolding(unittest.TestCase):
    def setUp(self):
        ensure_directories()

    def test_directories_exist(self):
        self.assertTrue(DATA_DIR.exists(), "Thư mục data phải tồn tại")
        self.assertTrue(RAW_DIR.exists(), "Thư mục data/raw phải tồn tại")
        self.assertTrue(STAGING_DIR.exists(), "Thư mục data/staging phải tồn tại")
        self.assertTrue(REFERENCE_DIR.exists(), "Thư mục data/reference phải tồn tại")

    def test_save_and_load_json_vietnamese(self):
        test_file = RAW_DIR / "test_vietnamese.json"
        data = {
            "country": "Việt Nam",
            "provinces": ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Bà Rịa - Vũng Tàu", "Đắk Lắk"],
            "target": "Phát thải ròng bằng 0 (Net-Zero 2050)"
        }
        save_json(data, test_file)
        self.assertTrue(test_file.exists())
        
        loaded = load_json(test_file)
        self.assertEqual(loaded["country"], "Việt Nam")
        self.assertEqual(loaded["provinces"][3], "Bà Rịa - Vũng Tàu")
        test_file.unlink()  # Dọn dẹp sau khi test

    def test_save_csv_utf8_sig(self):
        test_file = STAGING_DIR / "test_vietnamese.csv"
        df = pd.DataFrame([
            {"Province_Code": "01", "Province_Name": "Hà Nội", "GRDP_Billion_VND": 1200000},
            {"Province_Code": "79", "Province_Name": "Hồ Chí Minh", "GRDP_Billion_VND": 1600000},
            {"Province_Code": "48", "Province_Name": "Đà Nẵng", "GRDP_Billion_VND": 135000}
        ])
        save_csv(df, test_file)
        self.assertTrue(test_file.exists())

        # Đọc lại kiểm tra encoding
        df_read = pd.read_csv(test_file, encoding="utf-8-sig")
        self.assertEqual(len(df_read), 3)
        self.assertEqual(df_read.iloc[0]["Province_Name"], "Hà Nội")
        test_file.unlink()  # Dọn dẹp sau khi test

if __name__ == "__main__":
    unittest.main()
