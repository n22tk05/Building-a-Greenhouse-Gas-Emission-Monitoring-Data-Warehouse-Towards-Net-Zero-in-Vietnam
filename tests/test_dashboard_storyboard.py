"""Unit tests for Phase 4: Two-Page Power BI Dashboard Storyboard & Visual Specification.

Verifies:
1. `powerbi/theme_netzero.json` exists, has valid JSON syntax, and contains required Net-Zero Emerald palette.
2. `docs/powerbi_dashboard_specification.md` exists and covers Page 1 (Executive Overview) and Page 2 (Provincial Drill-down).
3. `powerbi/README_BUILD_GUIDE.md` exists and details step-by-step setup for Shape Map and DAX measures.
4. Color codes in theme match Net-Zero standards (#0F172A, #10B981, #1E293B, #EF4444).
5. Cross-filtering interaction matrix is documented.
"""

import json
import os
import unittest


class TestPowerBiStoryboard(unittest.TestCase):
    """Test suite for Power BI storyboard and visual specs."""

    def setUp(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.theme_path = os.path.join(
            self.project_root, "powerbi", "theme_netzero.json"
        )
        self.spec_path = os.path.join(
            self.project_root, "docs", "powerbi_dashboard_specification.md"
        )
        self.guide_path = os.path.join(
            self.project_root, "powerbi", "README_BUILD_GUIDE.md"
        )

    def test_theme_file_validity(self):
        self.assertTrue(os.path.exists(self.theme_path), f"Missing: {self.theme_path}")
        with open(self.theme_path, "r", encoding="utf-8") as f:
            theme = json.load(f)

        self.assertIn("name", theme)
        self.assertIn("dataColors", theme)
        self.assertIn("background", theme)
        self.assertIn("foreground", theme)

        # Check required Net-Zero palette
        self.assertEqual(theme["background"].upper(), "#0F172A")
        self.assertEqual(theme["foreground"].upper(), "#1E293B")
        self.assertIn("#10B981", [c.upper() for c in theme["dataColors"]])
        self.assertIn("#EF4444", [c.upper() for c in theme["dataColors"]])

    def test_specification_document_content(self):
        self.assertTrue(os.path.exists(self.spec_path), f"Missing: {self.spec_path}")
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check Page 1 and Page 2 sections
        self.assertIn("Trang 1: Báo Cáo Điều Hành", content)
        self.assertIn("Trang 2: Phân Tích Chi Tiết", content)
        self.assertIn("Hero Shape Map", content)
        self.assertIn("4 Góc Phần Tư", content)
        self.assertIn("Cross-Filtering", content)

    def test_build_guide_document_content(self):
        self.assertTrue(os.path.exists(self.guide_path), f"Missing: {self.guide_path}")
        with open(self.guide_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Shape map visual", content)
        self.assertIn("vietnam_provinces.topojson", content)
        self.assertIn("theme_netzero.json", content)
        self.assertIn("_Measures", content)


if __name__ == "__main__":
    unittest.main()
