import os
import sys
import time
from pathlib import Path

# Đảm bảo thư mục gốc dự án nằm trong sys.path khi chạy trực tiếp
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests
import pandas as pd
from typing import Dict, List, Any, Optional

from scripts.utils import RAW_DIR, STAGING_DIR, save_json, save_csv, logger

# Các chỉ số World Bank chuẩn IPCC AR5 cho Việt Nam (1970 - 2024)
INDICATORS: Dict[str, str] = {
    "EN.GHG.ALL.MT.CE.AR5": "Total_GHG_MtCO2e",
    "EN.GHG.CO2.MT.CE.AR5": "CO2_MtCO2e",
    "EN.GHG.CH4.MT.CE.AR5": "Methane_MtCO2e",
    "EN.GHG.CO2.PC.CE.AR5": "CO2_Per_Capita_Tonnes",
    "EG.FEC.RNEW.ZS": "Renewable_Energy_Pct",
    "NY.GDP.MKTP.CD": "GDP_USD"
}

BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1000"

def fetch_indicator_data(country_code: str, indicator_code: str, retries: int = 3, timeout: int = 15) -> List[Dict[str, Any]]:
    """
    Gọi World Bank REST API với cơ chế retry.
    Trả về danh sách các bản ghi thô cho chỉ số tương ứng.
    """
    url = BASE_URL.format(country=country_code, indicator=indicator_code)
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Dang tai du lieu: {indicator_code} (lan thu {attempt}/{retries})...")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            # Cấu trúc World Bank API: [metadata, records]
            if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
                logger.info(f"-> Thanh cong: {len(data[1])} ban ghi cho {indicator_code}")
                return data[1]
            else:
                logger.warning(f"Phan hoi khong dung cau truc cho {indicator_code}")
                return []
        except requests.RequestException as e:
            logger.warning(f"Loi ket noi khi tai {indicator_code}: {e}")
            if attempt < retries:
                time.sleep(2 * attempt)
            else:
                logger.error(f"Khong the tai {indicator_code} sau {retries} lan thu.")
                raise

def parse_and_pivot_records(raw_by_indicator: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
    """
    Chuyển đổi các danh sách bản ghi thô thành DataFrame phẳng và pivot theo Năm (Year).
    """
    combined_rows = []
    
    for ind_code, records in raw_by_indicator.items():
        column_name = INDICATORS[ind_code]
        for rec in records:
            year_str = rec.get("date")
            val = rec.get("value")
            
            if year_str and year_str.isdigit():
                combined_rows.append({
                    "Year": int(year_str),
                    "Indicator": column_name,
                    "Value": float(val) if val is not None else None
                })
                
    if not combined_rows:
        return pd.DataFrame()
        
    df_long = pd.DataFrame(combined_rows)
    # Pivot an toàn tránh lỗi nếu có bản ghi trùng lặp
    df_pivoted = df_long.pivot_table(index="Year", columns="Indicator", values="Value", aggfunc="first").reset_index()
    
    # Sắp xếp tăng dần theo năm
    df_pivoted = df_pivoted.sort_values("Year").reset_index(drop=True)
    
    # Lọc bỏ những năm mà tất cả các chỉ số phát thải và kinh tế đều là NaN
    value_cols = list(INDICATORS.values())
    existing_cols = [c for c in value_cols if c in df_pivoted.columns]
    df_clean = df_pivoted.dropna(subset=existing_cols, how="all").copy()
    
    return df_clean

def run_worldbank_ingestion(country_code: str = "VNM") -> pd.DataFrame:
    """
    Thực thi toàn bộ pipeline thu thập và làm sạch dữ liệu World Bank.
    """
    logger.info(f"Bat dau thu thap du lieu World Bank cho quoc gia: {country_code}")
    raw_results = {}
    
    for ind_code in INDICATORS.keys():
        records = fetch_indicator_data(country_code, ind_code)
        raw_results[ind_code] = records

    # 1. Lưu payload thô dạng JSON
    raw_json_path = RAW_DIR / "worldbank_raw.json"
    save_json(raw_results, raw_json_path)

    # 2. Xử lý & Pivot thành bảng sạch
    df_clean = parse_and_pivot_records(raw_results)
    
    # 3. Lưu bảng dữ liệu Staging dạng CSV UTF-8
    staging_csv_path = STAGING_DIR / "wb_national_emissions.csv"
    save_csv(df_clean, staging_csv_path)
    
    logger.info(f"Hoan tat Phase 2: {len(df_clean)} dong du lieu phat thai va kinh te quoc gia.")
    return df_clean

if __name__ == "__main__":
    df = run_worldbank_ingestion("VNM")
    print("\n--- 5 DÒNG DỮ LIỆU ĐẦU TIÊN (PREVIEW) ---")
    print(df.head())
    print("\n--- 5 DÒNG DỮ LIỆU GẦN ĐÂY NHẤT (PREVIEW) ---")
    print(df.tail())
    print(f"\nTổng số năm dữ liệu: {len(df)} (Từ năm {df['Year'].min()} đến {df['Year'].max()})")
