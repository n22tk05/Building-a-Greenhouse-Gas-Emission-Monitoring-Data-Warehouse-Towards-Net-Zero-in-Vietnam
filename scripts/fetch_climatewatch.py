import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# Đảm bảo thư mục gốc dự án nằm trong sys.path khi chạy trực tiếp
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests
import pandas as pd
from scripts.utils import RAW_DIR, STAGING_DIR, save_json, save_csv, logger

# Ánh xạ mã ngành chuẩn và tên tiếng Việt phục vụ Dim_Sector & Fact_Emissions
SECTOR_MAPPING: Dict[str, Dict[str, str]] = {
    "Energy": {"code": "ENG", "name_vi": "Năng lượng & Khai khoáng", "category": "Energy"},
    "Electricity/Heat": {"code": "ELE", "name_vi": "Sản xuất Điện & Nhiệt", "category": "Energy"},
    "Manufacturing/Construction": {"code": "IND", "name_vi": "Công nghiệp Chế biến & Xây dựng", "category": "Industry"},
    "Industrial Processes": {"code": "IPU", "name_vi": "Quá trình Công nghiệp (Xi măng, Thép)", "category": "Industry"},
    "Agriculture": {"code": "AGR", "name_vi": "Nông nghiệp & Trồng lúa nước", "category": "Agriculture"},
    "Transportation": {"code": "TRA", "name_vi": "Giao thông Vận tải", "category": "Transport"},
    "Waste": {"code": "WST", "name_vi": "Xử lý Chất thải & Nước thải", "category": "Waste"},
    "Building": {"code": "BLD", "name_vi": "Tòa nhà & Dân dụng", "category": "Building"},
    "Total excluding LULUCF": {"code": "TOT", "name_vi": "Tổng phát thải quốc gia (trừ LULUCF)", "category": "Total"}
}

API_URL = "https://www.climatewatchdata.org/api/v1/data/historical_emissions?regions=VNM"

def fetch_climatewatch_data(retries: int = 3, timeout: int = 20) -> Dict[str, Any]:
    """
    Gọi ClimateWatch Historical Emissions REST API với cơ chế thử lại.
    """
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Dang tai du lieu ClimateWatch cho Vietnam (lan thu {attempt}/{retries})...")
            response = requests.get(API_URL, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and "data" in data and len(data["data"]) > 0:
                logger.info(f"-> Thanh cong: {len(data['data'])} chuoi du lieu nganh tu ClimateWatch.")
                return data
            else:
                logger.warning("Phan hoi tu ClimateWatch khong chua du lieu hop le.")
        except requests.RequestException as e:
            logger.warning(f"Loi ket noi khi tai ClimateWatch: {e}")
            if attempt < retries:
                time.sleep(2 * attempt)
            else:
                logger.error(f"Khong the ket noi ClimateWatch sau {retries} lan thu.")
                raise
    return {}

def parse_sector_emissions(payload: Dict[str, Any]) -> pd.DataFrame:
    """
    Phân tích cấu trúc JSON của ClimateWatch thành bảng phẳng các ngành.
    """
    records = payload.get("data", [])
    rows = []
    
    for item in records:
        sector_raw = item.get("sector")
        gas = item.get("gas")
        source = item.get("source")
        emissions_series = item.get("emissions", [])
        
        # Ưu tiên lấy tổng khí nhà kính (All GHG) hoặc CO2 nếu không có All GHG
        if gas not in ["All GHG", "CO2"]:
            continue
            
        # Ánh xạ sang danh mục ngành chuẩn
        sector_meta = SECTOR_MAPPING.get(sector_raw)
        sector_code = sector_meta["code"] if sector_meta else "OTH"
        sector_name_vi = sector_meta["name_vi"] if sector_meta else sector_raw
        sector_category = sector_meta["category"] if sector_meta else "Other"
        
        for point in emissions_series:
            year = point.get("year")
            val = point.get("value")
            
            if year and val is not None:
                rows.append({
                    "Year": int(year),
                    "Sector_Code": sector_code,
                    "Sector_Name_EN": sector_raw,
                    "Sector_Name_VI": sector_name_vi,
                    "Sector_Category": sector_category,
                    "Gas": gas,
                    "Source": source,
                    "Emissions_MtCO2e": float(val)
                })
                
    if not rows:
        return pd.DataFrame()
        
    df = pd.DataFrame(rows)
    
    # Loại bỏ bản ghi trùng lặp (giữ bản ghi đầu tiên nếu cùng Year x Sector_Code x Gas)
    df = df.drop_duplicates(subset=["Year", "Sector_Code", "Gas"]).copy()
    
    # Sắp xếp tăng dần theo Năm và Mã ngành
    df = df.sort_values(["Year", "Sector_Code"]).reset_index(drop=True)
    return df

def run_climatewatch_ingestion() -> pd.DataFrame:
    """
    Thực thi toàn bộ pipeline thu thập dữ liệu phát thải theo ngành.
    """
    logger.info("Bat dau thu thap du lieu phat thai theo nganh (ClimateWatch)...")
    payload = fetch_climatewatch_data()
    
    # 1. Lưu payload thô JSON
    raw_path = RAW_DIR / "climatewatch_raw.json"
    save_json(payload, raw_path)
    
    # 2. Xử lý & Chuẩn hóa
    df_sectors = parse_sector_emissions(payload)
    
    # 3. Lưu bảng dữ liệu Staging dạng CSV UTF-8-sig
    staging_path = STAGING_DIR / "cw_sector_emissions.csv"
    save_csv(df_sectors, staging_path)
    
    logger.info(f"Hoan tat Phase 3: {len(df_sectors)} dong du lieu phat thai theo nganh.")
    return df_sectors

if __name__ == "__main__":
    df = run_climatewatch_ingestion()
    print("\n--- 5 DÒNG DỮ LIỆU ĐẦU TIÊN (PREVIEW) ---")
    print(df.head(5))
    print(f"\nTổng số dòng: {len(df)}")
    print("Danh sách các ngành thu thập được:")
    print(df[["Sector_Code", "Sector_Name_VI", "Gas"]].drop_duplicates())
