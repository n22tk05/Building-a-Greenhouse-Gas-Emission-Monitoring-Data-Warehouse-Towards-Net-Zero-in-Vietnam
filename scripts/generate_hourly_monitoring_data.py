"""
Script tự động sinh 1.65 triệu dòng dữ liệu quan trắc vi mô cấp giờ (189 trạm x 365 ngày x 24 giờ năm 2024).
Phục vụ bảng dwh.Fact_Hourly_Air_Monitoring và dwh.Dim_Station cho đồ án Net-Zero Vietnam DWH.
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Thiết lập mã hóa UTF-8 cho console Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
STAGING_DIR = DATA_DIR / "staging"
REF_DIR = DATA_DIR / "reference"

STAGING_DIR.mkdir(parents=True, exist_ok=True)
REF_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print(" [NETZERO DWH] SINH 1.65 TRIEU DONG DU LIEU QUAN TRAC CAP GIO")
print("=" * 70)

# 1. Đọc danh mục 63 tỉnh thành để tạo trạm quan trắc
prov_csv = REF_DIR / "dim_provinces_master.csv"
if not prov_csv.exists():
    raise FileNotFoundError(f"Không tìm thấy file {prov_csv}")

df_prov = pd.read_csv(prov_csv, dtype={"Province_Code": str})
print(f"[1/4] Đã nạp danh mục {len(df_prov)} tỉnh thành từ {prov_csv.name}.")

# Tọa độ tham chiếu xấp xỉ cho các trung tâm vùng
region_coords = {
    "Đồng bằng sông Hồng": (20.8, 105.8),
    "Đông Nam Bộ": (10.8, 106.7),
    "Bắc Trung Bộ & Duyên hải miền Trung": (16.0, 108.2),
    "Trung du & Miền núi phía Bắc": (21.5, 104.5),
    "Đồng bằng sông Cửu Long": (10.0, 105.5),
    "Tây Nguyên": (13.5, 108.0)
}

# 2. Sinh danh mục 189 trạm quan trắc (3 trạm / tỉnh)
station_rows = []
station_types = [
    ("Khu Công Nghiệp", "KCN", 1.35),       # Hệ số phát thải cao
    ("Đô Thị Giao Thông", "DT", 1.15),      # Cao điểm giao thông
    ("Vùng Đệm Sinh Thái", "ST", 0.70)      # Phát thải thấp, nền sạch
]

np.random.seed(42)

for idx, p in df_prov.iterrows():
    p_code = str(p["Province_Code"]).zfill(2)
    p_name = p["Province_Name"]
    region = p.get("Region", "Đồng bằng sông Hồng")
    base_lat, base_lon = region_coords.get(region, (16.0, 106.0))
    
    # Biến thiên tọa độ nhẹ giữa các tỉnh
    prov_lat = base_lat + np.random.uniform(-1.0, 1.0)
    prov_lon = base_lon + np.random.uniform(-0.8, 0.8)
    
    for s_idx, (s_type, s_prefix, s_factor) in enumerate(station_types, 1):
        st_code = f"ST-{p_code}-{s_idx:02d}"
        st_name = f"Trạm {s_type} {p_name} ({s_prefix}-{p_code})"
        st_lat = round(prov_lat + np.random.uniform(-0.08, 0.08), 6)
        st_lon = round(prov_lon + np.random.uniform(-0.08, 0.08), 6)
        
        station_rows.append({
            "Station_Code": st_code,
            "Station_Name": st_name,
            "Province_Code": p_code,
            "Province_Name": p_name,
            "Station_Type": s_type,
            "Emission_Factor": s_factor,
            "Latitude": st_lat,
            "Longitude": st_lon,
            "Is_Active": 1
        })

df_stations = pd.DataFrame(station_rows)
stations_path = REF_DIR / "dim_stations_master.csv"
df_stations.drop(columns=["Emission_Factor"]).to_csv(stations_path, index=False, encoding="utf-8-sig")
print(f"[2/4] Đã tạo danh mục 189 trạm quan trắc: {stations_path.name} (3 trạm/tỉnh).")

# 3. Tạo khung thời gian cho năm 2024 (365 ngày x 24 giờ = 8.760 giờ)
date_range = pd.date_range(start="2024-01-01 00:00:00", end="2024-12-31 23:00:00", freq="h")
total_hours = len(date_range)
n_stations = len(df_stations)
total_records = n_stations * total_hours

print(f"[3/4] Đang sinh {total_records:,} bản ghi đo đạc (189 trạm x {total_hours:,} giờ)...")

# Trích xuất các mảng thời gian vector hóa
hours_arr = date_range.hour.to_numpy() # 0-23
months_arr = date_range.month.to_numpy() # 1-12
days_arr = date_range.day.to_numpy() # 1-31

# Hệ số chu kỳ ngày đêm (Diurnal cycle): Đỉnh phát thải vào 07:00-09:00 và 17:00-19:00
diurnal_weights = np.array([
    0.65, 0.60, 0.58, 0.58, 0.62, 0.75, # 00:00 - 05:00 (Đêm)
    0.95, 1.35, 1.40, 1.25, 1.10, 1.05, # 06:00 - 11:00 (Sáng cao điểm)
    1.00, 1.02, 1.08, 1.15, 1.30, 1.45, # 12:00 - 17:00 (Chiều cao điểm)
    1.38, 1.20, 1.05, 0.90, 0.80, 0.72  # 18:00 - 23:00 (Tối)
])

# Mở file CSV để ghi từng trạm (tránh tràn RAM khi ghi 1.65 triệu dòng)
output_csv = STAGING_DIR / "hourly_air_monitoring_2024.csv"

header = [
    "Date_Key", "Year", "Month", "Day", "Hour_24",
    "Station_Code", "Province_Code",
    "CO2_ppm", "CO_mg_m3", "NO2_ug_m3", "SO2_ug_m3",
    "PM25_ug_m3", "PM10_ug_m3", "AQI_Index", "AQI_Category", "Is_Exceeding_QCVN"
]

with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
    f.write(",".join(header) + "\n")
    
    batch_count = 0
    for s_idx, s in df_stations.iterrows():
        st_code = s["Station_Code"]
        p_code = s["Province_Code"]
        st_factor = s["Emission_Factor"]
        
        # Mức cơ sở theo tỉnh (Hà Nội, HCM, Bình Dương, Quảng Ninh phát thải cao hơn)
        is_high_ind = p_code in ["01", "79", "74", "75", "31", "22", "27"]
        ind_mult = 1.35 if is_high_ind else 0.95
        
        # Tạo nhiễu ngẫu nhiên cho 8760 giờ của trạm
        noise = np.random.normal(1.0, 0.12, total_hours)
        hour_factors = diurnal_weights[hours_arr] * st_factor * ind_mult * noise
        hour_factors = np.clip(hour_factors, 0.4, 2.5)
        
        # Nồng độ các khí (CO2, CO, NO2, SO2, PM2.5, PM10)
        co2 = np.round(415.0 + 85.0 * hour_factors + np.random.uniform(-10, 15, total_hours), 2)
        co = np.round(0.85 * hour_factors + np.random.uniform(0.1, 0.4, total_hours), 2)
        no2 = np.round(18.0 * hour_factors + np.random.uniform(2.0, 8.0, total_hours), 2)
        so2 = np.round(12.0 * hour_factors + np.random.uniform(1.0, 6.0, total_hours), 2)
        pm25 = np.round(22.0 * hour_factors + np.random.uniform(3.0, 12.0, total_hours), 2)
        pm10 = np.round(pm25 * np.random.uniform(1.4, 1.8, total_hours), 2)
        
        # Tính chỉ số AQI xấp xỉ dựa trên PM2.5 (chất ô nhiễm chính tại VN)
        aqi = np.clip(np.round(pm25 * 2.2 + no2 * 0.4), 15, 320).astype(int)
        
        # Phân loại AQI Category & QCVN 05:2023/BTNMT (PM2.5 trung bình 24h chuẩn là 50 ug/m3)
        is_exceeding = (pm25 > 50.0).astype(int)
        
        categories = np.where(aqi <= 50, "Tốt",
                     np.where(aqi <= 100, "Trung bình",
                     np.where(aqi <= 150, "Kém",
                     np.where(aqi <= 200, "Xấu", "Rất xấu"))))
        
        # Ghép thành DataFrame của 1 trạm
        df_station_hours = pd.DataFrame({
            "Date_Key": 2024,
            "Year": 2024,
            "Month": months_arr,
            "Day": days_arr,
            "Hour_24": hours_arr,
            "Station_Code": st_code,
            "Province_Code": p_code,
            "CO2_ppm": co2,
            "CO_mg_m3": co,
            "NO2_ug_m3": no2,
            "SO2_ug_m3": so2,
            "PM25_ug_m3": pm25,
            "PM10_ug_m3": pm10,
            "AQI_Index": aqi,
            "AQI_Category": categories,
            "Is_Exceeding_QCVN": is_exceeding
        })
        
        df_station_hours.to_csv(f, header=False, index=False)
        batch_count += 1
        if batch_count % 30 == 0 or batch_count == n_stations:
            print(f"  -> Tiến độ: Đã sinh dữ liệu cho {batch_count}/{n_stations} trạm quan trắc ({batch_count * total_hours:,} dòng)...")

file_size_mb = os.path.getsize(output_csv) / (1024 * 1024)
print(f"[4/4] HOÀN TẤT SINH DỮ LIỆU:")
print(f" - File Staging : {output_csv}")
print(f" - Tổng số dòng : {total_records:,} dòng")
print(f" - Dung lượng   : {file_size_mb:.2f} MB")
print("=" * 70)
