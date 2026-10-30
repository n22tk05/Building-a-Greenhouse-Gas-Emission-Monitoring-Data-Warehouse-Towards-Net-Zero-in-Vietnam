"""Unit tests for Phase 3: Geographic Boundary Asset (Vietnam 63-Province TopoJSON/Shape Map).

Verifies:
1. `data/reference/vietnam_provinces.topojson` exists and is within target size (< 1.5MB).
2. Proper TopoJSON topology format with `vietnam_provinces` and `provinces` layers.
3. Exactly 63 province geometries with zero duplicates and zero missing.
4. 100% referential integrity with `dim_provinces_master.csv` (`Province_Code`, `Province_Name`).
5. `scripts/verify_topojson.py` executes with exit code 0.
"""

import csv
import json
import os
import unittest


class TestVietnamTopojson(unittest.TestCase):
    """Test suite for TopoJSON boundary file."""

    def setUp(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.topo_path = os.path.join(
            self.project_root, "data", "reference", "vietnam_provinces.topojson"
        )
        self.csv_path = os.path.join(
            self.project_root, "data", "reference", "dim_provinces_master.csv"
        )
        self.verify_script = os.path.join(
            self.project_root, "scripts", "verify_topojson.py"
        )

    def test_topojson_file_exists(self):
        self.assertTrue(os.path.exists(self.topo_path), f"Missing: {self.topo_path}")

    def test_file_size_optimized(self):
        size_kb = os.path.getsize(self.topo_path) / 1024
        # Recommended size for Power BI Shape Map: 100KB - 1.5MB
        self.assertLess(size_kb, 1500, f"TopoJSON too large: {size_kb:.2f} KB > 1.5MB")
        self.assertGreater(size_kb, 50, f"TopoJSON suspiciously small: {size_kb:.2f} KB")

    def test_topojson_validity_and_63_provinces(self):
        with open(self.topo_path, "r", encoding="utf-8") as f:
            topo = json.load(f)

        self.assertEqual(topo.get("type"), "Topology")
        self.assertIn("objects", topo)
        self.assertIn("vietnam_provinces", topo["objects"])

        geoms = topo["objects"]["vietnam_provinces"]["geometries"]
        self.assertEqual(len(geoms), 63, f"Expected 63 geometries, got {len(geoms)}")

    def test_referential_integrity_with_master_csv(self):
        with open(self.topo_path, "r", encoding="utf-8") as f:
            topo = json.load(f)

        with open(self.csv_path, "r", encoding="utf-8-sig") as f:
            master_rows = list(csv.DictReader(f))

        master_codes = {r["Province_Code"].strip().zfill(2) for r in master_rows}
        master_names = {r["Province_Name"].strip() for r in master_rows}

        geoms = topo["objects"]["vietnam_provinces"]["geometries"]
        topo_codes = {g["properties"]["Province_Code"] for g in geoms}
        topo_names = {g["properties"]["Province_Name"] for g in geoms}

        self.assertEqual(
            master_codes,
            topo_codes,
            f"Code mismatch! Missing: {master_codes - topo_codes}, Extra: {topo_codes - master_codes}",
        )
        self.assertEqual(
            master_names,
            topo_names,
            f"Name mismatch! Missing: {master_names - topo_names}",
        )

    def test_dual_layer_compatibility_for_powerbi(self):
        with open(self.topo_path, "r", encoding="utf-8") as f:
            topo = json.load(f)

        # Power BI accepts either 'vietnam_provinces' or default 'provinces'
        self.assertIn("provinces", topo["objects"])
        self.assertEqual(
            len(topo["objects"]["provinces"]["geometries"]), 63
        )

    def test_verify_script_executes_successfully(self):
        from scripts.verify_topojson import verify_topojson
        self.assertTrue(verify_topojson(), "Quality gate verification failed!")


if __name__ == "__main__":
    unittest.main()
