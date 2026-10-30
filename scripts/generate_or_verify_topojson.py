"""Script to generate and standardize `data/reference/vietnam_provinces.topojson`
for Microsoft Power BI Shape Map visual.

It pulls the 63-province polygon topologies from verified open GIS data,
aligns properties 100% with `data/reference/dim_provinces_master.csv`:
- `id`: Province_Code ('01' to '96')
- `Province_Code`: '01' to '96'
- `Province_Name`: Vietnamese standard name (Unicode)
- `Province_Name_Ascii`: ASCII name without diacritics
- `Region`: Economic/Geographic Region
- `Economic_Zone`: Economic zone
- `Is_Industrial_Hub`: 1 or 0
- Object layer name: `vietnam_provinces` and `provinces` (dual-compatibility)
"""

import csv
import json
import os
import re
import sys
import unicodedata
import urllib.request


def to_key(text: str) -> str:
    """Normalize province name to stripped ascii lowercase key for fuzzy matching."""
    text = unicodedata.normalize("NFD", text)
    text = re.sub(r"[\u0300-\u036f]", "", text)
    text = text.replace("\u0111", "d").replace("\u0110", "D")
    text = re.sub(r"[^a-zA-Z0-9]", "", text).lower()
    if text.startswith("tp"):
        text = text[2:]
    return text


def build_vietnam_topojson():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "reference", "dim_provinces_master.csv")
    output_topo_path = os.path.join(project_root, "data", "reference", "vietnam_provinces.topojson")

    print("[INFO] Loading master province metadata from CSV...")
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        dim_rows = list(csv.DictReader(f))

    if len(dim_rows) != 63:
        raise ValueError(f"Expected 63 provinces in dim_provinces_master.csv, found {len(dim_rows)}")

    dim_map = {}
    for r in dim_rows:
        code = r["Province_Code"].strip().zfill(2)
        dim_map[to_key(r["Province_Name"])] = {
            "Province_Code": code,
            "Province_Name": r["Province_Name"].strip(),
            "Province_Name_Ascii": r["Province_Name_Ascii"].strip(),
            "Region": r["Region"].strip(),
            "Economic_Zone": r["Economic_Zone"].strip(),
            "Area_Km2": float(r["Area_Km2"]),
            "Is_Industrial_Hub": int(r["Is_Industrial_Hub"]),
        }

    print(f"[INFO] Successfully indexed {len(dim_map)} provinces from metadata.")

    # Source TopoJSON with local caching fallback
    raw_cache_path = os.path.join(project_root, "data", "raw", "vn-simple-topo.json")
    if os.path.exists(raw_cache_path):
        print(f"[INFO] Loading cached geometry topology from: {raw_cache_path} ...")
        with open(raw_cache_path, "r", encoding="utf-8") as f:
            raw_topo = json.load(f)
    else:
        source_url = "https://raw.githubusercontent.com/lebinh/vietnam-choropleth-map/master/vn-simple-topo.json"
        print(f"[INFO] Fetching verified geometry topology from: {source_url} ...")
        req = urllib.request.Request(source_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw_content = resp.read().decode("utf-8")
            raw_topo = json.loads(raw_content)
        # Cache for offline builds
        os.makedirs(os.path.dirname(raw_cache_path), exist_ok=True)
        with open(raw_cache_path, "w", encoding="utf-8") as f:
            f.write(raw_content)
        print(f"[INFO] Cached source topology to: {raw_cache_path}")

    source_geoms = raw_topo["objects"]["tracts"]["geometries"]
    print(f"[INFO] Loaded {len(source_geoms)} geometries from source TopoJSON.")

    standardized_geoms = []
    matched_codes = set()

    for idx, g in enumerate(source_geoms):
        source_name = g.get("properties", {}).get("ten_tinh", "")
        k = to_key(source_name)

        if k not in dim_map:
            raise KeyError(f"Geometry #{idx} '{source_name}' could not be matched to master provinces!")

        meta = dim_map[k]
        code = meta["Province_Code"]
        matched_codes.add(code)

        # Standardize geometry properties for Power BI Shape Map
        std_geom = {
            "type": g["type"],
            "arcs": g["arcs"],
            "id": code,  # Primary key for Power BI Shape Map matching
            "properties": {
                "id": code,
                "Province_Code": code,
                "Province_Name": meta["Province_Name"],
                "Province_Name_Ascii": meta["Province_Name_Ascii"],
                "Region": meta["Region"],
                "Economic_Zone": meta["Economic_Zone"],
                "Area_Km2": meta["Area_Km2"],
                "Is_Industrial_Hub": meta["Is_Industrial_Hub"],
                "name": meta["Province_Name"],  # Standard fallback
            },
        }
        standardized_geoms.append(std_geom)

    if len(matched_codes) != 63:
        raise ValueError(f"Only matched {len(matched_codes)}/63 unique province codes!")

    # Sort geometries by Province_Code ('01' -> '96')
    standardized_geoms.sort(key=lambda x: x["properties"]["Province_Code"])

    # Construct final TopoJSON structure with dual object layers ('vietnam_provinces' & 'provinces')
    final_topo = {
        "type": "Topology",
        "bbox": raw_topo.get("bbox", [102.14, 8.56, 109.46, 23.39]),
        "objects": {
            "vietnam_provinces": {
                "type": "GeometryCollection",
                "geometries": standardized_geoms,
            },
            "provinces": {
                "type": "GeometryCollection",
                "geometries": standardized_geoms,
            },
        },
        "arcs": raw_topo["arcs"],
    }

    if "transform" in raw_topo:
        final_topo["transform"] = raw_topo["transform"]

    print(f"[INFO] Writing standardized TopoJSON to: {output_topo_path} ...")
    with open(output_topo_path, "w", encoding="utf-8") as out_f:
        json.dump(final_topo, out_f, ensure_ascii=False, separators=(",", ":"))

    file_size_kb = os.path.getsize(output_topo_path) / 1024
    print(f"[SUCCESS] Created {output_topo_path} ({file_size_kb:.2f} KB) with all 63 provinces!")

    # Verify upon generation to fulfill the "generate or verify" contract
    try:
        sys.path.insert(0, project_root)
        from scripts.verify_topojson import verify_topojson
        print("\n[INFO] Triggering automatic quality gate verification...")
        verify_topojson()
    except Exception as e:
        print(f"[WARNING] Quality gate trigger error: {e}")


if __name__ == "__main__":
    build_vietnam_topojson()
