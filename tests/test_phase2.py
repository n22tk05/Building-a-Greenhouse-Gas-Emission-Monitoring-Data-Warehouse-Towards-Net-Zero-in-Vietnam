import sys
import unittest
from pathlib import Path
import pandas as pd

from scripts.utils import RAW_DIR, STAGING_DIR, load_json

class TestPhase2WorldBankIngestion(unittest.TestCase):
    def setUp(self):
        self.raw_json_path = RAW_DIR / "worldbank_raw.json"
        self.staging_csv_path = STAGING_DIR / "wb_national_emissions.csv"

    def test_raw_json_exists_and_populated(self):
        self.assertTrue(self.raw_json_path.exists(), "File worldbank_raw.json phải tồn tại")
        data = load_json(self.raw_json_path)
        self.assertIsInstance(data, dict)
        self.assertIn("EN.GHG.CO2.MT.CE.AR5", data)
        self.assertGreater(len(data["EN.GHG.CO2.MT.CE.AR5"]), 0)

    def test_staging_csv_structure_and_grain(self):
        self.assertTrue(self.staging_csv_path.exists(), "File wb_national_emissions.csv phải tồn tại")
        df = pd.read_csv(self.staging_csv_path, encoding="utf-8-sig")

        # 1. Kiểm tra số dòng (tối thiểu 30 năm)
        self.assertGreaterEqual(len(df), 30, f"Dữ liệu cần có ít nhất 30 năm, thực tế có {len(df)}")

        # 2. Kiểm tra các cột bắt buộc
        expected_cols = ["Year", "Total_GHG_MtCO2e", "CO2_MtCO2e", "Methane_MtCO2e", "GDP_USD"]
        for col in expected_cols:
            self.assertIn(col, df.columns, f"Thiếu cột {col} trong file staging CSV")

        # 3. Kiểm tra tính duy nhất của cột Year (Khóa tự nhiên)
        self.assertEqual(len(df), df["Year"].nunique(), "Năm (Year) phải là duy nhất, không trùng lặp")

        # 4. Kiểm tra thứ tự tăng dần
        self.assertTrue(df["Year"].is_monotonic_increasing, "Năm phải được sắp xếp tăng dần")

        # 5. Kiểm tra giá trị CO2 thực tế gần đây (ví dụ năm 2020 phát thải > 200 Mt CO2e)
        recent_co2 = df[df["Year"] == 2020]["CO2_MtCO2e"].values
        if len(recent_co2) > 0 and pd.notna(recent_co2[0]):
            self.assertGreater(recent_co2[0], 200.0)

if __name__ == "__main__":
    unittest.main()
