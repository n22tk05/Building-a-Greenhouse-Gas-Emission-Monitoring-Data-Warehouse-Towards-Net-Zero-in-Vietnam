import os
import sys
import unittest
import re
from pathlib import Path
import pandas as pd

# Đảm bảo thư mục gốc dự án nằm trong sys.path khi chạy trực tiếp
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.utils import STAGING_DIR, REFERENCE_DIR

SQL_DIR = ROOT_DIR / "sql"
INIT_DB_SQL = SQL_DIR / "00_init_database.sql"
STAGING_SQL = SQL_DIR / "01_create_staging_tables.sql"

class TestPhase2SQLStaging(unittest.TestCase):
    def setUp(self):
        self.assertTrue(INIT_DB_SQL.exists(), f"File {INIT_DB_SQL} phải tồn tại")
        self.assertTrue(STAGING_SQL.exists(), f"File {STAGING_SQL} phải tồn tại")

        with open(INIT_DB_SQL, "r", encoding="utf-8") as f:
            self.init_sql_content = f.read()

        with open(STAGING_SQL, "r", encoding="utf-8") as f:
            self.staging_sql_content = f.read()

    def test_database_initialization_script(self):
        """Kiểm tra kịch bản tạo database NetZero_VN_DWH và Collation tiếng Việt."""
        self.assertIn("NetZero_VN_DWH", self.init_sql_content)
        self.assertIn("Vietnamese_CI_AS", self.init_sql_content)
        self.assertIn("CREATE SCHEMA [staging]", self.init_sql_content)
        self.assertIn("CREATE SCHEMA [dwh]", self.init_sql_content)
        self.assertIn("RECOVERY SIMPLE", self.init_sql_content)

    def test_staging_tables_declared(self):
        """Kiểm tra cả 4 bảng staging và stored procedure truncate được khai báo."""
        expected_tables = [
            "staging.stg_wb_national_emissions",
            "staging.stg_cw_sector_emissions",
            "staging.stg_gso_provincial_economy",
            "staging.stg_dim_provinces"
        ]
        for tbl in expected_tables:
            self.assertIn(tbl, self.staging_sql_content, f"Bảng {tbl} phải được định nghĩa trong file SQL")

        self.assertIn("staging.sp_Truncate_Staging", self.staging_sql_content)

    def test_staging_column_coverage_against_csv(self):
        """
        Kiểm tra tính bao phủ 100%: mọi cột trong file CSV Tuần 1 phải có mặt trong DDL SQL tương ứng.
        """
        table_csv_map = {
            "stg_wb_national_emissions": STAGING_DIR / "wb_national_emissions.csv",
            "stg_cw_sector_emissions": STAGING_DIR / "cw_sector_emissions.csv",
            "stg_gso_provincial_economy": STAGING_DIR / "gso_provincial_economy.csv",
            "stg_dim_provinces": REFERENCE_DIR / "dim_provinces_master.csv"
        }

        for tbl_name, csv_path in table_csv_map.items():
            self.assertTrue(csv_path.exists(), f"File CSV {csv_path} phải tồn tại")
            df = pd.read_csv(csv_path, nrows=1)
            csv_cols = set(df.columns)

            # Trích xuất đoạn mã CREATE TABLE của bảng này
            pattern = rf"CREATE TABLE \[staging\]\.\[{tbl_name}\]\s*\((.*?)\);"
            match = re.search(pattern, self.staging_sql_content, re.DOTALL | re.IGNORECASE)
            self.assertIsNotNone(match, f"Không tìm thấy khối CREATE TABLE cho {tbl_name}")

            table_body = match.group(1)
            # Trích xuất danh sách cột [Column_Name] trong khối table
            sql_cols = set(re.findall(r"\[([a-zA-Z0-9_]+)\]", table_body))

            # Xác nhận 100% cột trong CSV nằm trong DDL SQL
            missing_cols = csv_cols - sql_cols
            self.assertEqual(len(missing_cols), 0, 
                             f"Bảng {tbl_name} thiếu các cột sau so với file CSV: {missing_cols}")

            # Kiểm tra 2 cột Metadata bắt buộc
            self.assertIn("Loaded_At", sql_cols, f"Bảng {tbl_name} phải có cột Loaded_At")
            self.assertIn("Source_File", sql_cols, f"Bảng {tbl_name} phải có cột Source_File")

    def test_staging_data_types_and_constraints(self):
        """Kiểm tra các kiểu dữ liệu quan trọng: NVARCHAR cho tiếng Việt, VARCHAR cho mã tỉnh."""
        # Province_Code phải là VARCHAR(10) để giữ số 0 ở đầu
        self.assertRegex(self.staging_sql_content, r"\[Province_Code\]\s+VARCHAR\(10\)")
        # Tên tiếng Việt phải dùng NVARCHAR
        self.assertRegex(self.staging_sql_content, r"\[Province_Name\]\s+NVARCHAR\(100\)")
        self.assertRegex(self.staging_sql_content, r"\[Sector_Name_VI\]\s+NVARCHAR\(150\)")
        # Số tiền tệ và chỉ số đo lường phải dùng DECIMAL
        self.assertIn("DECIMAL(18, 2)", self.staging_sql_content)
        self.assertIn("DECIMAL(18, 4)", self.staging_sql_content)

    def test_idempotent_script(self):
        """Kiểm tra script có khả năng thực thi lại nhiều lần mà không báo lỗi (Idempotent)."""
        drop_table_count = len(re.findall(r"DROP TABLE\s+\[staging\]\.\[stg_", self.staging_sql_content, re.IGNORECASE))
        self.assertEqual(drop_table_count, 4, "Phải có 4 câu lệnh DROP TABLE IF OBJECT_ID IS NOT NULL")
        self.assertIn("DROP PROCEDURE [staging].[sp_Truncate_Staging]", self.staging_sql_content)

if __name__ == "__main__":
    unittest.main()
