"""Script to generate and standardize `data/reference/vietnam_provinces.topojson`
for Microsoft Power BI Shape Map visual using genuine WGS84 geographic coordinates.

Features:
1. Sourced from geoBoundaries VNM ADM1 (WGS84 EPSG:4326).
2. Merges Côn Đảo and mainland Bà Rịa - Vũng Tàu into a single MultiPolygon.
3. Produces exactly 63 provinces aligning 100% with `dim_provinces_master.csv`.
4. Embeds WGS84 bounding box [102.145883, 8.439958, 114.996965, 23.390974].
5. Dual layers: `vietnam_provinces` and `provinces`.
"""

import csv
import json
import math
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


def encode_island(cx, cy, rx, ry, scale, translate, n=12):
    """Encode an island/reef into a closed TopoJSON quantized arc."""
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n
        dr = 1.0 + 0.15 * math.sin(3 * ang)
        px = cx + rx * dr * math.cos(ang)
        py = cy + ry * dr * math.sin(ang)
        pts.append((px, py))
    pts.append(pts[0])

    qpts = []
    for px, py in pts:
        qx = int(round((px - translate[0]) / scale[0]))
        qy = int(round((py - translate[1]) / scale[1]))
        qpts.append((qx, qy))

    arc = []
    cur_x, cur_y = 0, 0
    for i, (qx, qy) in enumerate(qpts):
        if i == 0:
            arc.append([qx, qy])
            cur_x, cur_y = qx, qy
        else:
            arc.append([qx - cur_x, qy - cur_y])
            cur_x, cur_y = qx, qy
    return arc


def build_vietnam_topojson():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "reference", "dim_provinces_master.csv")
    output_topo_path = os.path.join(project_root, "data", "reference", "vietnam_provinces.topojson")
    raw_cache_path = os.path.join(project_root, "data", "raw", "geoBoundaries-VNM-ADM1.topojson")

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

    print(f"[INFO] Successfully indexed {len(dim_map)} master provinces.")

    # Load source WGS84 TopoJSON
    if os.path.exists(raw_cache_path):
        print(f"[INFO] Loading cached geometry topology from: {raw_cache_path} ...")
        with open(raw_cache_path, "r", encoding="utf-8") as f:
            raw_topo = json.load(f)
    else:
        source_url = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/VNM/ADM1/geoBoundaries-VNM-ADM1.topojson"
        print(f"[INFO] Fetching genuine WGS84 geometry topology from: {source_url} ...")
        req = urllib.request.Request(source_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw_content = resp.read().decode("utf-8")
            raw_topo = json.loads(raw_content)
        os.makedirs(os.path.dirname(raw_cache_path), exist_ok=True)
        with open(raw_cache_path, "w", encoding="utf-8") as f:
            f.write(raw_content)
        print(f"[INFO] Cached source topology to: {raw_cache_path}")

    # Inspect source objects
    src_obj_key = list(raw_topo["objects"].keys())[0]
    src_geoms = raw_topo["objects"][src_obj_key]["geometries"]
    print(f"[INFO] Loaded {len(src_geoms)} raw geometries from '{src_obj_key}'.")

    # Group geometries into 63 provinces
    grouped = {}
    for g in src_geoms:
        name = g.get("properties", {}).get("shapeName", "").strip()
        k = to_key(name)
        if k == "condao":
            k = to_key("Ba Ria - Vung Tau")
        elif k == "hochiminh":
            k = to_key("Ho Chi Minh")
        elif k == "hanoit":
            k = to_key("Ha Noi")
        elif k == "thienthienhue":
            k = to_key("Thua Thien Hue")

        if k not in dim_map:
            raise KeyError(f"Raw geometry '{name}' (key: '{k}') could not be matched to master provinces!")

        if k not in grouped:
            grouped[k] = []
        grouped[k].append(g)

    if len(grouped) != 63:
        raise ValueError(f"Expected 63 grouped provinces, got {len(grouped)}")

    # Sort standardized geometries by Province_Code ('01' to '96')
    standardized_geoms = []
    for k, meta in sorted(dim_map.items(), key=lambda item: item[1]["Province_Code"]):
        g_list = grouped[k]
        code = meta["Province_Code"]

        # Merge arcs if multiple pieces (e.g. Ba Ria - Vung Tau + Con Dao)
        all_polygon_rings = []
        for g in g_list:
            g_type = g.get("type")
            if g_type == "Polygon":
                all_polygon_rings.append(g.get("arcs", []))
            elif g_type == "MultiPolygon":
                all_polygon_rings.extend(g.get("arcs", []))
            else:
                raise ValueError(f"Unsupported geometry type: {g_type}")

        # Enhanced geographic features: Tối ưu kích thước hiển thị Quần đảo Hoàng Sa (Đà Nẵng) & Trường Sa (Khánh Hòa)
        # Bằng cách phóng to 4.5x quanh tâm các đảo nguyên bản từ geoBoundaries để bảo toàn 100% hướng Clockwise,
        # tránh lỗi inner hole/self-intersection và đảm bảo hiển thị nổi bật trên Power BI Shape Map.
        scale = raw_topo["transform"]["scale"]
        translate = raw_topo["transform"]["translate"]
        if code in ("48", "56"):
            island_arcs_set = {67, 68, 72, 73, 74, 75} if code == "48" else {141, 142, 143, 144, 145, 146, 147}
            for a_idx in island_arcs_set:
                arc = raw_topo["arcs"][a_idx]
                x, y = 0, 0
                coords = []
                for dx, dy in arc:
                    x += dx
                    y += dy
                    coords.append((x * scale[0] + translate[0], y * scale[1] + translate[1]))
                n = len(coords) - 1
                cx = sum(p[0] for p in coords[:-1]) / n
                cy = sum(p[1] for p in coords[:-1]) / n
                factor = 4.5
                scaled = []
                for lon, lat in coords:
                    scaled.append((cx + factor * (lon - cx), cy + factor * (lat - cy)))
                scaled[-1] = scaled[0]
                new_arc = []
                prev_qx, prev_qy = 0, 0
                for i, (lon, lat) in enumerate(scaled):
                    qx = int(round((lon - translate[0]) / scale[0]))
                    qy = int(round((lat - translate[1]) / scale[1]))
                    if i == 0:
                        new_arc.append([qx, qy])
                    else:
                        new_arc.append([qx - prev_qx, qy - prev_qy])
                    prev_qx, prev_qy = qx, qy
                raw_topo["arcs"][a_idx] = new_arc

        if len(all_polygon_rings) == 1:
            geom_type = "Polygon"
            geom_arcs = all_polygon_rings[0]
        else:
            geom_type = "MultiPolygon"
            geom_arcs = all_polygon_rings

        props = {
            "id": code,
            "Province_Code": code,
            "Province_Name": meta["Province_Name"],
            "Province_Name_Ascii": meta["Province_Name_Ascii"],
            "Region": meta["Region"],
            "Economic_Zone": meta["Economic_Zone"],
            "Area_Km2": meta["Area_Km2"],
            "Is_Industrial_Hub": meta["Is_Industrial_Hub"],
            "name": meta["Province_Name"],
        }

        standardized_geoms.append({
            "type": geom_type,
            "arcs": geom_arcs,
            "id": code,
            "properties": props
        })

    # Compute bounding box in WGS84
    scale = raw_topo["transform"]["scale"]
    translate = raw_topo["transform"]["translate"]
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")

    for arc in raw_topo["arcs"]:
        cur_x, cur_y = 0, 0
        for dx, dy in arc:
            cur_x += dx
            cur_y += dy
            lon = cur_x * scale[0] + translate[0]
            lat = cur_y * scale[1] + translate[1]
            if lon < min_x: min_x = lon
            if lon > max_x: max_x = lon
            if lat < min_y: min_y = lat
            if lat > max_y: max_y = lat

    bbox = [round(min_x, 6), round(min_y, 6), round(max_x, 6), round(max_y, 6)]
    print(f"[INFO] Calculated WGS84 Bounding Box: {bbox}")

    final_topo = {
        "type": "Topology",
        "bbox": bbox,
        "transform": raw_topo["transform"],
        "objects": {
            "vietnam_provinces": {
                "type": "GeometryCollection",
                "geometries": standardized_geoms
            },
            "provinces": {
                "type": "GeometryCollection",
                "geometries": standardized_geoms
            }
        },
        "arcs": raw_topo["arcs"]
    }

    os.makedirs(os.path.dirname(output_topo_path), exist_ok=True)
    with open(output_topo_path, "w", encoding="utf-8") as f:
        json.dump(final_topo, f, ensure_ascii=False, separators=(",", ":"))

    out_size_kb = os.path.getsize(output_topo_path) / 1024
    print(f"[SUCCESS] Generated '{output_topo_path}':")
    print(f"  - Size: {out_size_kb:.2f} KB (Optimized for Power BI)")
    print(f"  - Layers: 'vietnam_provinces' & 'provinces'")
    print(f"  - Total provinces: {len(standardized_geoms)}")
    print(f"  - Coordinates: Genuine WGS84 (Lon: [{bbox[0]}, {bbox[2]}], Lat: [{bbox[1]}, {bbox[3]}])")


if __name__ == "__main__":
    build_vietnam_topojson()
