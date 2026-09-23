import unittest
from pathlib import Path
import pandas as pd

from scripts.utils import REFERENCE_DIR, STAGING_DIR

class TestPhase4GSODataPreparation(unittest.TestCase):
    def setUp(self):
        self.dim_provinces_path = REFERENCE_DIR / "dim_provinces_master.csv"
        self.staging_econ_path = STAGING_DIR / "gso_provincial_economy.csv"

    def test_dim_provinces_master(self):
        self.assertTrue(self.dim_provinces_path.exists(), "File dim_provinces_master.csv phải tồn tại")
        df_dim = pd.read_csv(self.dim_provinces_path, encoding="utf-8-sig", dtype={"Province_Code": str})

        # 1. Đúng chính xác 63 tỉnh thành
        self.assertEqual(len(df_dim), 63, f"Việt Nam có 63 tỉnh thành, thực tế có {len(df_dim)}")

        # 2. Mã tỉnh phải duy nhất
        self.assertEqual(df_dim["Province_Code"].nunique(), 63, "Mã tỉnh phải là duy nhất")

        # 3. Kiểm tra các tỉnh thành phố tiêu biểu
        sample_provinces = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Bà Rịa - Vũng Tàu", "Đắk Lắk", "Quảng Ninh"]
        for p in sample_provinces:
            self.assertIn(p, df_dim["Province_Name"].values, f"Thiếu tỉnh thành: {p}")

        # 4. Các cột bắt buộc
        expected_cols = ["Province_Code", "Province_Name", "Province_Name_Ascii", "Region", "Economic_Zone", "Area_Km2", "Is_Industrial_Hub"]
        for col in expected_cols:
            self.assertIn(col, df_dim.columns)

    def test_provincial_economy_staging(self):
        self.assertTrue(self.staging_econ_path.exists(), "File gso_provincial_economy.csv phải tồn tại")
        df_econ = pd.read_csv(self.staging_econ_path, encoding="utf-8-sig", dtype={"Province_Code": str})
        df_dim = pd.read_csv(self.dim_provinces_path, encoding="utf-8-sig", dtype={"Province_Code": str})

        # 1. Đủ 630 dòng (63 tỉnh x 10 năm từ 2015 đến 2024)
        self.assertEqual(len(df_econ), 630, f"Cần đúng 630 bản ghi (63 tỉnh x 10 năm), thực tế có {len(df_econ)}")

        # 2. Kiểm tra tính toàn vẹn tham chiếu (Referential Integrity): mọi mã tỉnh đều nằm trong Dim
        dim_codes = set(df_dim["Province_Code"].values)
        econ_codes = set(df_econ["Province_Code"].values)
        self.assertTrue(econ_codes.issubset(dim_codes), "Tất cả mã tỉnh trong bảng kinh tế phải nằm trong danh mục chuẩn")

        # 3. Không có bản ghi trùng lặp cặp [Year, Province_Code]
        self.assertEqual(df_econ.duplicated(subset=["Year", "Province_Code"]).sum(), 0)

        # 4. Các giá trị đo lường phải dương
        self.assertTrue((df_econ["GRDP_Billion_VND"] > 0).all())
        self.assertTrue((df_econ["Population"] > 0).all())
        self.assertTrue((df_econ["Estimated_Carbon_Tonnes"] > 0).all())
        self.assertTrue((df_econ["Decoupling_Index"] > 0).all())

if __name__ == "__main__":
    unittest.main()
