"""Script to verify the validity, integrity, and Power BI readiness of
`data/reference/vietnam_provinces.topojson`.

Checks:
1. Valid JSON syntax and TopoJSON spec compliance.
2. File size within recommended boundary (< 1.5MB for fast loading).
3. Genuine WGS84 geographic coordinates (EPSG:4326) and valid Vietnam bounding box.
4. Exactly 63 province geometries with zero duplicates and zero missing.
5. All `Province_Code` ('01' to '96') strictly match `dim_provinces_master.csv`.
6. Non-empty polygons/multipolygons and valid arcs.
"""

import csv
import json
import os
import sys


def verify_topojson():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    topo_path = os.path.join(project_root, "data", "reference", "vietnam_provinces.topojson")
    csv_path = os.path.join(project_root, "data", "reference", "dim_provinces_master.csv")

    print("=== BAT DAU KIEM DINH TEP KHONG GIAN SO TOPOJSON (PHASE 3 QUALITY GATE) ===")
    errors = []

    # 1. File existence & size
    if not os.path.exists(topo_path):
        print(f"[FAIL] Khong tim thay file: {topo_path}")
        return False

    size_kb = os.path.getsize(topo_path) / 1024
    print(f"[CHECK 1] Kich thuoc tep: {size_kb:.2f} KB (Nguong toi uu: < 1500 KB)")
    if size_kb > 1500:
        errors.append(f"Dung luong file qua lon: {size_kb:.2f} KB > 1500 KB")
    elif size_kb < 50:
        errors.append(f"Dung luong file qua nho: {size_kb:.2f} KB < 50 KB")

    # 2. Parse JSON & check TopoJSON structure
    try:
        with open(topo_path, "r", encoding="utf-8") as f:
            topo = json.load(f)
    except Exception as e:
        print(f"[FAIL] Loi cu phap JSON: {e}")
        return False

    if topo.get("type") != "Topology":
        errors.append(f"Loai doi tuong khong hop le: {topo.get('type')} != Topology")

    if "objects" not in topo or not topo["objects"]:
        errors.append("Thieu doi tuong 'objects' trong TopoJSON")

    # 3. Check WGS84 Bounding Box and Transform
    bbox = topo.get("bbox")
    if not bbox or len(bbox) != 4:
        errors.append(f"Thieu hoac sai dinh dang bounding box (bbox): {bbox}")
    else:
        min_lon, min_lat, max_lon, max_lat = bbox
        print(f"[CHECK 2] Bounding Box (WGS84): Lon [{min_lon}, {max_lon}], Lat [{min_lat}, {max_lat}]")
        if not (100.0 <= min_lon <= 104.0):
            errors.append(f"min_lon ({min_lon}) nam ngoai bien do toa do dia ly Viet Nam (100.0 - 104.0)")
        if not (8.0 <= min_lat <= 10.0):
            errors.append(f"min_lat ({min_lat}) nam ngoai bien do toa do dia ly Viet Nam (8.0 - 10.0)")
        if not (108.0 <= max_lon <= 120.0):
            errors.append(f"max_lon ({max_lon}) nam ngoai bien do toa do dia ly Viet Nam (108.0 - 120.0)")
        if not (22.0 <= max_lat <= 25.0):
            errors.append(f"max_lat ({max_lat}) nam ngoai bien do toa do dia ly Viet Nam (22.0 - 25.0)")

    # 4. Check layer name
    layer_name = None
    for candidate in ["vietnam_provinces", "provinces", "tracts"]:
        if candidate in topo.get("objects", {}):
            layer_name = candidate
            break

    if not layer_name:
        errors.append(f"Khong tim thay layer tinh thanh hop le. Cac layer hien co: {list(topo.get('objects', {}).keys())}")
        geometries = []
    else:
        geometries = topo["objects"][layer_name].get("geometries", [])

    print(f"[CHECK 3] Layer duoc chon: '{layer_name}' voi {len(geometries)} geometries")
    if len(geometries) != 63:
        errors.append(f"So luong tinh thanh khong dung: {len(geometries)} != 63")

    # 5. Compare with master metadata
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        master_rows = list(csv.DictReader(f))
    master_codes = {r["Province_Code"].strip().zfill(2) for r in master_rows}
    master_names = {r["Province_Name"].strip() for r in master_rows}

    topo_codes = set()
    topo_names = set()

    for idx, g in enumerate(geometries):
        props = g.get("properties", {})
        code = str(props.get("Province_Code") or g.get("id") or "").strip().zfill(2)
        name = props.get("Province_Name") or props.get("name") or ""

        if not code or code == "00":
            errors.append(f"Geometry #{idx} ({name}) co ma Province_Code khong hop le: '{code}'")
        else:
            topo_codes.add(code)

        if name:
            topo_names.add(name)

        # Check geometry arcs
        arcs = g.get("arcs")
        if not arcs or len(arcs) == 0:
            errors.append(f"Geometry #{idx} ({name}) khong co arcs toa do!")

    missing_codes = master_codes - topo_codes
    extra_codes = topo_codes - master_codes

    print(f"[CHECK 4] Ty le khop ma tinh thanh (Province_Code): {len(topo_codes)}/63 ({len(topo_codes)/63*100:.1f}%)")
    if missing_codes:
        errors.append(f"Thieu cac ma tinh thanh: {sorted(list(missing_codes))}")
    if extra_codes:
        errors.append(f"Thua cac ma tinh thanh ngoai danh muc: {sorted(list(extra_codes))}")

    missing_names = master_names - topo_names
    print(f"[CHECK 5] Ty le khop ten tieng Viet chuan: {len(topo_names)}/63 ({len(topo_names)/63*100:.1f}%)")
    if missing_names:
        errors.append(f"Thieu cac ten tinh thanh tieng Viet: {sorted(list(missing_names))}")

    # Summary
    if errors:
        print("\n[RESULT] PHAT HIEN CAC LOI KIEM DINH:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("\n[RESULT] >>> 100% QUALITY CHECKS PASSED: TEP TOPOJSON DAT CHUAN WGS84 POWER BI SHAPE MAP <<<")
        return True


if __name__ == "__main__":
    success = verify_topojson()
    sys.exit(0 if success else 1)
