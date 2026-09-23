import unittest
from pathlib import Path
import pandas as pd

from scripts.utils import RAW_DIR, STAGING_DIR, load_json

class TestPhase3ClimateWatchIngestion(unittest.TestCase):
    def setUp(self):
        self.raw_json_path = RAW_DIR / "climatewatch_raw.json"
        self.staging_csv_path = STAGING_DIR / "cw_sector_emissions.csv"

    def test_raw_json_exists_and_valid(self):
        self.assertTrue(self.raw_json_path.exists(), "File climatewatch_raw.json phải tồn tại")
        data = load_json(self.raw_json_path)
        self.assertIn("data", data)
        self.assertGreater(len(data["data"]), 0)

    def test_staging_csv_structure_and_sectors(self):
        self.assertTrue(self.staging_csv_path.exists(), "File cw_sector_emissions.csv phải tồn tại")
        df = pd.read_csv(self.staging_csv_path, encoding="utf-8-sig")

        # 1. Kiểm tra số dòng tối thiểu
        self.assertGreaterEqual(len(df), 200, f"Dữ liệu cần có ít nhất 200 dòng, thực tế có {len(df)}")

        # 2. Kiểm tra các cột bắt buộc
        expected_cols = ["Year", "Sector_Code", "Sector_Name_VI", "Gas", "Emissions_MtCO2e"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

        # 3. Kiểm tra các ngành cốt lõi
        unique_sectors = set(df["Sector_Code"].unique())
        for required_sector in ["AGR", "IND", "ENG", "ELE"]:
            self.assertIn(required_sector, unique_sectors, f"Thiếu mã ngành cốt lõi: {required_sector}")

        # 4. Kiểm tra tính duy nhất của khóa tự nhiên [Year, Sector_Code, Gas]
        duplicates = df.duplicated(subset=["Year", "Sector_Code", "Gas"])
        self.assertEqual(duplicates.sum(), 0, "Không được có bản ghi trùng lặp khóa tự nhiên")

        # 5. Kiểm tra giá trị phát thải phải là số thực >= 0
        self.assertTrue((df["Emissions_MtCO2e"] >= 0).all(), "Phát thải không thể có giá trị âm")

if __name__ == "__main__":
    unittest.main()
