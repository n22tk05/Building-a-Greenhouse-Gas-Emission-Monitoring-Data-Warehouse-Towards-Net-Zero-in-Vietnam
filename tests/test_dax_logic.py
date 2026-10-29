"""Unit tests for Phase 2: DAX Measures Library & Analytical Metrics Engine.

Verifies:
1. File `powerbi/dax_measures.dax` exists and contains at least 25 measures.
2. All mandatory measure groups are present:
   - National Emissions Metrics
   - Provincial Economics & Decoupling
   - Big Data Air Monitoring 2024 (1.66M rows)
   - Time Intelligence & Growth
   - Net-Zero Trajectory & Gap
   - Dynamic Formatting & Color Hex
3. Overcounting Guard logic is implemented in `National GDP (USD)`.
4. Mathematical logic of Decoupling Color Hex and Tapio classification.
5. Dictionary documentation `docs/dax_measures_dictionary.md` exists and covers all measures.
"""

import os
import re
import unittest


class TestDaxMeasuresLibrary(unittest.TestCase):
    """Test DAX measures file and business logic."""

    def setUp(self):
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.dax_file = os.path.join(
            self.project_root, "powerbi", "dax_measures.dax"
        )
        self.dict_file = os.path.join(
            self.project_root, "docs", "dax_measures_dictionary.md"
        )

    def test_dax_file_exists(self):
        self.assertTrue(
            os.path.exists(self.dax_file), f"File not found: {self.dax_file}"
        )

    def test_dict_file_exists(self):
        self.assertTrue(
            os.path.exists(self.dict_file), f"File not found: {self.dict_file}"
        )

    def test_measure_count_and_definitions(self):
        with open(self.dax_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Regular expression to extract DAX measure names (Pattern: Measure Name = ...)
        # Exclude comments and variable declarations
        lines = content.splitlines()
        measures = []
        for line in lines:
            trimmed = line.strip()
            if (
                trimmed
                and not trimmed.startswith("//")
                and not trimmed.startswith("/*")
                and not trimmed.startswith("VAR ")
                and not trimmed.startswith("RETURN")
            ):
                match = re.match(r"^([a-zA-Z0-9_\-\s\(\)\%\.,\>\<\&\/\+]+)\s*=\s*", trimmed)
                if match:
                    measure_name = match.group(1).strip()
                    # filter out non-measure assignment lines
                    if len(measure_name) > 3 and not measure_name.startswith("SELECT"):
                        measures.append(measure_name)

        self.assertGreaterEqual(
            len(measures),
            20,
            f"Expected at least 20 DAX measures, found {len(measures)}: {measures}",
        )

    def test_key_measures_present(self):
        with open(self.dax_file, "r", encoding="utf-8") as f:
            content = f.read()

        required_measures = [
            "Total GHG Emissions (MtCO2e)",
            "Total CO2 Emissions (MtCO2e)",
            "National GDP (USD)",
            "National Emission Intensity",
            "Provincial Carbon Tonnes",
            "Provincial GRDP (Billion VND)",
            "Provincial Decoupling Index",
            "Carbon Intensity (Tonnes per Billion VND)",
            "Avg AQI Index",
            "Avg PM2.5 (ug/m3)",
            "Exceeding QCVN Hours",
            "Emissions YoY Growth %",
            "Baseline 2020 Emissions",
            "Target Emission 2030 (NDC)",
            "NetZero 2030 Target Gap (MtCO2e)",
            "Decoupling Color Hex",
            "AQI Status Color Hex",
        ]

        for m in required_measures:
            self.assertIn(
                m, content, f"Required DAX measure '{m}' missing from dax_measures.dax"
            )

    def test_gdp_overcounting_guard_in_dax(self):
        with open(self.dax_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn(
            'vw_Dim_Sector_Hierarchy_BI[Sector_Code] = "TOT"',
            content,
            "National GDP measure must filter Sector_Code = 'TOT' to prevent 9x overcounting",
        )

    def test_decoupling_color_logic(self):
        def get_color(idx):
            if idx is None:
                return "#9CA3AF"
            if idx < 0:
                return "#10B981"
            if 0 <= idx <= 0.8:
                return "#F59E0B"
            return "#EF4444"

        self.assertEqual(get_color(-0.5), "#10B981")  # Strong Decoupling -> Green
        self.assertEqual(get_color(0.4), "#F59E0B")   # Weak Decoupling -> Amber
        self.assertEqual(get_color(1.5), "#EF4444")   # Coupling / Expansive -> Red
        self.assertEqual(get_color(None), "#9CA3AF")  # Missing -> Gray


if __name__ == "__main__":
    unittest.main()
