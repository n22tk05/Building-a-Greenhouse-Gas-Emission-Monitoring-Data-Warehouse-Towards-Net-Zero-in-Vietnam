import unittest
import os
from pathlib import Path
import pandas as pd

class TestHourlyAirMonitoring(unittest.TestCase):
    """Bộ kiểm tra xác thực tầng dữ liệu mở rộng Big Data (Fact_Hourly_Air_Monitoring)."""

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent
        cls.data_dir = cls.root_dir / "data"
        cls.staging_csv = cls.data_dir / "staging" / "hourly_air_monitoring_2024.csv"
        cls.stations_csv = cls.data_dir / "reference" / "dim_stations_master.csv"
        cls.provinces_csv = cls.data_dir / "reference" / "dim_provinces_master.csv"
        cls.sql_script = cls.root_dir / "sql" / "06_create_hourly_monitoring_tables.sql"

    def test_artifacts_exist(self):
        """Xác nhận các file mã nguồn và dữ liệu mở rộng tồn tại."""
        self.assertTrue(self.sql_script.exists(), "Thiếu file sql/06_create_hourly_monitoring_tables.sql")
        self.assertTrue(self.stations_csv.exists(), "Thiếu file data/reference/dim_stations_master.csv")
        self.assertTrue(self.staging_csv.exists(), "Thiếu file data/staging/hourly_air_monitoring_2024.csv")

    def test_stations_referential_integrity(self):
        """Kiểm tra tính toàn vẹn tham chiếu 189 trạm với 63 tỉnh."""
        df_stations = pd.read_csv(self.stations_csv, dtype={"Province_Code": str})
        df_provinces = pd.read_csv(self.provinces_csv, dtype={"Province_Code": str})
        
        self.assertEqual(len(df_stations), 189, "Số lượng trạm phải đúng bằng 189 (3 trạm x 63 tỉnh)")
        
        station_prov_codes = set(df_stations["Province_Code"].unique())
        master_prov_codes = set(df_provinces["Province_Code"].unique())
        
        self.assertEqual(station_prov_codes, master_prov_codes, "Mã tỉnh trong danh mục trạm phải khớp 100% với 63 tỉnh")

    def test_hourly_staging_volume(self):
        """Kiểm tra dung lượng và cấu trúc file 1.66 triệu dòng."""
        file_size_mb = os.path.getsize(self.staging_csv) / (1024 * 1024)
        self.assertGreater(file_size_mb, 100.0, "File dữ liệu phải lớn hơn 100MB")
        
        # Đọc 100 dòng đầu để kiểm tra header và kiểu dữ liệu
        df_sample = pd.read_csv(self.staging_csv, nrows=100)
        expected_cols = [
            "Date_Key", "Year", "Month", "Day", "Hour_24",
            "Station_Code", "Province_Code",
            "CO2_ppm", "CO_mg_m3", "NO2_ug_m3", "SO2_ug_m3",
            "PM25_ug_m3", "PM10_ug_m3", "AQI_Index", "AQI_Category", "Is_Exceeding_QCVN"
        ]
        self.assertEqual(list(df_sample.columns), expected_cols)
        self.assertTrue((df_sample["CO2_ppm"] >= 380).all())
        self.assertTrue((df_sample["AQI_Index"] >= 0).all())

    def test_sql_ddl_features(self):
        """Kiểm tra file DDL có Clustered Columnstore Index và Dim_Time_Of_Day."""
        with open(self.sql_script, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("Fact_Hourly_Air_Monitoring", content)
        self.assertIn("Dim_Time_Of_Day", content)
        self.assertIn("Dim_Station", content)
        self.assertIn("CCI_Fact_Hourly_Air_Monitoring", content)
        self.assertIn("CLUSTERED COLUMNSTORE INDEX", content)

if __name__ == "__main__":
    unittest.main()
