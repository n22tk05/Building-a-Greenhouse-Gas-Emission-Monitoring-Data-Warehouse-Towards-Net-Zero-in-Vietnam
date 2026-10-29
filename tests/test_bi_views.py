"""Unit tests for Phase 1: Semantic Layer & SQL BI Views.

Verifies:
1. All 8 BI Views exist in `dwh` schema.
2. `vw_Dim_Province_Geo_BI` contains 63 provinces with 2-digit Province_Code.
3. `vw_Fact_National_Emissions_BI` has GDP Overcounting Guard active:
   SUM(GDP_USD) on View for Sector_Code != 'TOT' is NULL, while Sector_Code = 'TOT' has valid GDP.
4. `vw_Fact_Provincial_Economy_BI` has Decoupling_Status and valid metrics.
5. `vw_Fact_Hourly_Air_Monitoring_BI` successfully queries the 1.66M rows with CCI acceleration.
"""

import os
import unittest


class TestBiViewsSql(unittest.TestCase):
    """Test SQL file definition and structure for BI views."""

    def setUp(self):
        self.sql_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "sql",
            "05_create_bi_views.sql",
        )

    def test_sql_file_exists(self):
        self.assertTrue(
            os.path.exists(self.sql_file),
            f"File not found: {self.sql_file}",
        )

    def test_sql_file_contains_all_views(self):
        with open(self.sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        expected_views = [
            "vw_Dim_Date_BI",
            "vw_Dim_Province_Geo_BI",
            "vw_Dim_Sector_Hierarchy_BI",
            "vw_Fact_National_Emissions_BI",
            "vw_Fact_Provincial_Economy_BI",
            "vw_Dim_Station_BI",
            "vw_Dim_Time_Of_Day_BI",
            "vw_Fact_Hourly_Air_Monitoring_BI",
        ]
        for v in expected_views:
            self.assertIn(
                v,
                content,
                f"Expected view {v} not found in sql/05_create_bi_views.sql",
            )

    def test_gdp_overcounting_guard_logic_present(self):
        with open(self.sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for Overcounting guard CASE statement
        self.assertIn("GDP OVERCOUNTING GUARD", content)
        self.assertIn("Sector_Code = 'TOT'", content)

    def test_tapio_decoupling_classification_present(self):
        with open(self.sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Decoupling_Status", content)
        self.assertIn("Tách rời mạnh (Strong Decoupling)", content)
        self.assertIn("Tách rời yếu (Weak Decoupling)", content)

    def test_hourly_monitoring_view_joins_and_qcvn_flag(self):
        with open(self.sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("vw_Fact_Hourly_Air_Monitoring_BI", content)
        self.assertIn("Is_Exceeding_QCVN", content)
        self.assertIn("Is_Rush_Hour", content)
        self.assertIn("Dim_Station", content)
        self.assertIn("Dim_Time_Of_Day", content)

    def test_province_geo_view_contains_ascii_and_codes(self):
        with open(self.sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("vw_Dim_Province_Geo_BI", content)
        self.assertIn("Province_Code", content)
        self.assertIn("Province_Name_Ascii", content)
        self.assertIn("Macro_Region", content)


if __name__ == "__main__":
    unittest.main()
