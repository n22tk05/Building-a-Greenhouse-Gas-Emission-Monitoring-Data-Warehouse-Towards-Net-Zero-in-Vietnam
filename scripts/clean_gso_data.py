import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Đảm bảo thư mục gốc dự án nằm trong sys.path khi chạy trực tiếp
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
from scripts.utils import REFERENCE_DIR, STAGING_DIR, save_csv, logger

# Danh mục chuẩn 63 tỉnh thành Việt Nam theo Tổng cục Thống kê (GSO)
PROVINCES_CATALOG: List[Dict[str, Any]] = [
    # Đồng bằng sông Hồng
    {"code": "01", "name": "Hà Nội", "ascii": "Ha Noi", "region": "Đồng bằng sông Hồng", "zone": "KTTĐ Bắc Bộ", "area": 3359.8, "hub": 1, "grdp_share": 0.126},
    {"code": "26", "name": "Vĩnh Phúc", "ascii": "Vinh Phuc", "region": "Đồng bằng sông Hồng", "zone": "KTTĐ Bắc Bộ", "area": 1236.0, "hub": 1, "grdp_share": 0.015},
    {"code": "27", "name": "Bắc Ninh", "ascii": "Bac Ninh", "region": "Đồng bằng sông Hồng", "zone": "KTTĐ Bắc Bộ", "area": 822.7, "hub": 1, "grdp_share": 0.024},
    {"code": "22", "name": "Quảng Ninh", "ascii": "Quang Ninh", "region": "Đồng bằng sông Hồng", "zone": "KTTĐ Bắc Bộ", "area": 6207.9, "hub": 1, "grdp_share": 0.029},
    {"code": "30", "name": "Hải Dương", "ascii": "Hai Duong", "region": "Đồng bằng sông Hồng", "zone": "KTTĐ Bắc Bộ", "area": 1668.2, "hub": 1, "grdp_share": 0.018},
    {"code": "31", "name": "Hải Phòng", "ascii": "Hai Phong", "region": "Đồng bằng sông Hồng", "zone": "KTTĐ Bắc Bộ", "area": 1561.8, "hub": 1, "grdp_share": 0.041},
    {"code": "33", "name": "Hưng Yên", "ascii": "Hung Yen", "region": "Đồng bằng sông Hồng", "zone": "KTTĐ Bắc Bộ", "area": 930.2, "hub": 1, "grdp_share": 0.014},
    {"code": "34", "name": "Thái Bình", "ascii": "Thai Binh", "region": "Đồng bằng sông Hồng", "zone": "Khác", "area": 1586.4, "hub": 0, "grdp_share": 0.011},
    {"code": "35", "name": "Hà Nam", "ascii": "Ha Nam", "region": "Đồng bằng sông Hồng", "zone": "Khác", "area": 861.9, "hub": 1, "grdp_share": 0.009},
    {"code": "36", "name": "Nam Định", "ascii": "Nam Dinh", "region": "Đồng bằng sông Hồng", "zone": "Khác", "area": 1668.8, "hub": 0, "grdp_share": 0.010},
    {"code": "37", "name": "Ninh Bình", "ascii": "Ninh Binh", "region": "Đồng bằng sông Hồng", "zone": "Khác", "area": 1411.8, "hub": 1, "grdp_share": 0.009},

    # Trung du và Miền núi phía Bắc
    {"code": "02", "name": "Hà Giang", "ascii": "Ha Giang", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 7927.5, "hub": 0, "grdp_share": 0.003},
    {"code": "04", "name": "Cao Bằng", "ascii": "Cao Bang", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 6700.3, "hub": 0, "grdp_share": 0.002},
    {"code": "06", "name": "Bắc Kạn", "ascii": "Bac Kan", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 4859.9, "hub": 0, "grdp_share": 0.001},
    {"code": "08", "name": "Tuyên Quang", "ascii": "Tuyen Quang", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 5867.9, "hub": 0, "grdp_share": 0.004},
    {"code": "10", "name": "Lào Cai", "ascii": "Lao Cai", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 6364.0, "hub": 0, "grdp_share": 0.007},
    {"code": "11", "name": "Điện Biên", "ascii": "Dien Bien", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 9541.2, "hub": 0, "grdp_share": 0.003},
    {"code": "12", "name": "Lai Châu", "ascii": "Lai Chau", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 9068.8, "hub": 0, "grdp_share": 0.003},
    {"code": "14", "name": "Sơn La", "ascii": "Son La", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 14123.6, "hub": 0, "grdp_share": 0.006},
    {"code": "15", "name": "Yên Bái", "ascii": "Yen Bai", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 6887.6, "hub": 0, "grdp_share": 0.004},
    {"code": "17", "name": "Hoà Bình", "ascii": "Hoa Binh", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 4590.6, "hub": 0, "grdp_share": 0.006},
    {"code": "19", "name": "Thái Nguyên", "ascii": "Thai Nguyen", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 3526.6, "hub": 1, "grdp_share": 0.015},
    {"code": "20", "name": "Lạng Sơn", "ascii": "Lang Son", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 8310.2, "hub": 0, "grdp_share": 0.004},
    {"code": "24", "name": "Bắc Giang", "ascii": "Bac Giang", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 3895.9, "hub": 1, "grdp_share": 0.018},
    {"code": "25", "name": "Phú Thọ", "ascii": "Phu Tho", "region": "Trung du & Miền núi phía Bắc", "zone": "Khác", "area": 3534.6, "hub": 1, "grdp_share": 0.009},

    # Bắc Trung Bộ & Duyên hải miền Trung
    {"code": "38", "name": "Thanh Hóa", "ascii": "Thanh Hoa", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 11114.7, "hub": 1, "grdp_share": 0.026},
    {"code": "40", "name": "Nghệ An", "ascii": "Nghe An", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 16493.7, "hub": 0, "grdp_share": 0.019},
    {"code": "42", "name": "Hà Tĩnh", "ascii": "Ha Tinh", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 5997.8, "hub": 1, "grdp_share": 0.010},
    {"code": "44", "name": "Quảng Bình", "ascii": "Quang Binh", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 8065.3, "hub": 0, "grdp_share": 0.005},
    {"code": "45", "name": "Quảng Trị", "ascii": "Quang Tri", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 4739.8, "hub": 0, "grdp_share": 0.004},
    {"code": "46", "name": "Thừa Thiên Huế", "ascii": "Thua Thien Hue", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "KTTĐ Miền Trung", "area": 5048.2, "hub": 0, "grdp_share": 0.007},
    {"code": "48", "name": "Đà Nẵng", "ascii": "Da Nang", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "KTTĐ Miền Trung", "area": 1284.9, "hub": 1, "grdp_share": 0.014},
    {"code": "49", "name": "Quảng Nam", "ascii": "Quang Nam", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "KTTĐ Miền Trung", "area": 10574.7, "hub": 1, "grdp_share": 0.012},
    {"code": "51", "name": "Quảng Ngãi", "ascii": "Quang Ngai", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "KTTĐ Miền Trung", "area": 5155.8, "hub": 1, "grdp_share": 0.013},
    {"code": "52", "name": "Bình Định", "ascii": "Binh Dinh", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "KTTĐ Miền Trung", "area": 6066.2, "hub": 0, "grdp_share": 0.011},
    {"code": "54", "name": "Phú Yên", "ascii": "Phu Yen", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 5023.4, "hub": 0, "grdp_share": 0.005},
    {"code": "56", "name": "Khánh Hòa", "ascii": "Khanh Hoa", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 5137.8, "hub": 1, "grdp_share": 0.011},
    {"code": "58", "name": "Ninh Thuận", "ascii": "Ninh Thuan", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 3355.3, "hub": 1, "grdp_share": 0.005},
    {"code": "60", "name": "Bình Thuận", "ascii": "Binh Thuan", "region": "Bắc Trung Bộ & Duyên hải miền Trung", "zone": "Khác", "area": 7812.9, "hub": 1, "grdp_share": 0.010},

    # Tây Nguyên
    {"code": "62", "name": "Kon Tum", "ascii": "Kon Tum", "region": "Tây Nguyên", "zone": "Khác", "area": 9674.2, "hub": 0, "grdp_share": 0.003},
    {"code": "64", "name": "Gia Lai", "ascii": "Gia Lai", "region": "Tây Nguyên", "zone": "Khác", "area": 15511.0, "hub": 0, "grdp_share": 0.009},
    {"code": "66", "name": "Đắk Lắk", "ascii": "Dak Lak", "region": "Tây Nguyên", "zone": "Khác", "area": 13030.5, "hub": 0, "grdp_share": 0.011},
    {"code": "67", "name": "Đắk Nông", "ascii": "Dak Nong", "region": "Tây Nguyên", "zone": "Khác", "area": 6509.3, "hub": 0, "grdp_share": 0.004},
    {"code": "68", "name": "Lâm Đồng", "ascii": "Lam Dong", "region": "Tây Nguyên", "zone": "Khác", "area": 9783.3, "hub": 0, "grdp_share": 0.012},

    # Đông Nam Bộ
    {"code": "70", "name": "Bình Phước", "ascii": "Binh Phuoc", "region": "Đông Nam Bộ", "zone": "KTTĐ Phía Nam", "area": 6871.8, "hub": 1, "grdp_share": 0.009},
    {"code": "72", "name": "Tây Ninh", "ascii": "Tay Ninh", "region": "Đông Nam Bộ", "zone": "KTTĐ Phía Nam", "area": 4041.3, "hub": 1, "grdp_share": 0.011},
    {"code": "74", "name": "Bình Dương", "ascii": "Binh Duong", "region": "Đông Nam Bộ", "zone": "KTTĐ Phía Nam", "area": 2694.4, "hub": 1, "grdp_share": 0.046},
    {"code": "75", "name": "Đồng Nai", "ascii": "Dong Nai", "region": "Đông Nam Bộ", "zone": "KTTĐ Phía Nam", "area": 5907.2, "hub": 1, "grdp_share": 0.044},
    {"code": "77", "name": "Bà Rịa - Vũng Tàu", "ascii": "Ba Ria - Vung Tau", "region": "Đông Nam Bộ", "zone": "KTTĐ Phía Nam", "area": 1980.8, "hub": 1, "grdp_share": 0.038},
    {"code": "79", "name": "Hồ Chí Minh", "ascii": "Ho Chi Minh", "region": "Đông Nam Bộ", "zone": "KTTĐ Phía Nam", "area": 2061.0, "hub": 1, "grdp_share": 0.160},

    # Đồng bằng sông Cửu Long
    {"code": "80", "name": "Long An", "ascii": "Long An", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ Phía Nam", "area": 4495.0, "hub": 1, "grdp_share": 0.016},
    {"code": "82", "name": "Tiền Giang", "ascii": "Tien Giang", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 2510.5, "hub": 0, "grdp_share": 0.011},
    {"code": "83", "name": "Bến Tre", "ascii": "Ben Tre", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 2394.6, "hub": 0, "grdp_share": 0.007},
    {"code": "84", "name": "Trà Vinh", "ascii": "Tra Vinh", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 2358.2, "hub": 1, "grdp_share": 0.007},
    {"code": "86", "name": "Vĩnh Long", "ascii": "Vinh Long", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 1525.6, "hub": 0, "grdp_share": 0.008},
    {"code": "87", "name": "Đồng Tháp", "ascii": "Dong Thap", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 3383.8, "hub": 0, "grdp_share": 0.011},
    {"code": "89", "name": "An Giang", "ascii": "An Giang", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 3536.7, "hub": 0, "grdp_share": 0.012},
    {"code": "91", "name": "Kiên Giang", "ascii": "Kien Giang", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 6348.8, "hub": 1, "grdp_share": 0.013},
    {"code": "92", "name": "Cần Thơ", "ascii": "Can Tho", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 1439.2, "hub": 1, "grdp_share": 0.012},
    {"code": "93", "name": "Hậu Giang", "ascii": "Hau Giang", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 1621.8, "hub": 0, "grdp_share": 0.005},
    {"code": "94", "name": "Sóc Trăng", "ascii": "Soc Trang", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 3311.6, "hub": 0, "grdp_share": 0.007},
    {"code": "95", "name": "Bạc Liêu", "ascii": "Bac Lieu", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 2669.0, "hub": 1, "grdp_share": 0.005},
    {"code": "96", "name": "Cà Mau", "ascii": "Ca Mau", "region": "Đồng bằng sông Cửu Long", "zone": "KTTĐ ĐBSCL", "area": 5221.2, "hub": 1, "grdp_share": 0.007},
]

def build_dim_provinces_master() -> pd.DataFrame:
    """
    Tạo bảng danh mục chuẩn hóa 63 tỉnh thành Việt Nam (Dim_Province).
    """
    df = pd.DataFrame(PROVINCES_CATALOG)
    df = df.rename(columns={
        "code": "Province_Code",
        "name": "Province_Name",
        "ascii": "Province_Name_Ascii",
        "region": "Region",
        "zone": "Economic_Zone",
        "area": "Area_Km2",
        "hub": "Is_Industrial_Hub"
    })
    # Loại bỏ grdp_share ở bảng dimension thuần túy
    df_dim = df.drop(columns=["grdp_share"]).copy()
    return df_dim

def build_provincial_economy_series(years: List[int] = list(range(2015, 2025))) -> pd.DataFrame:
    """
    Xây dựng tập dữ liệu kinh tế và phát thải ước lượng cho 63 tỉnh thành qua 10 năm (2015 - 2024).
    Phản ánh đúng tương quan tăng trưởng GRDP, dân số và phát thải carbon địa phương.
    """
    # Mức chuẩn GRDP toàn quốc theo năm (tỷ đồng)
    NATIONAL_GRDP_BASE = {
        2015: 4192862, 2016: 4502733, 2017: 5005975, 2018: 5542832, 2019: 6037348,
        2020: 6293145, 2021: 8479600, 2022: 9513300, 2023: 10221800, 2024: 10980000
    }
    
    # Tổng phát thải khí nhà kính toàn quốc (triệu tấn CO2e từ World Bank)
    NATIONAL_GHG_BASE = {
        2015: 350.2, 2016: 375.4, 2017: 395.1, 2018: 432.5, 2019: 470.8,
        2020: 492.9, 2021: 486.8, 2022: 494.5, 2023: 542.9, 2024: 584.3
    }
    
    # Dân số cơ sở (nghìn người)
    POPULATION_BASE = {
        "01": 8400, "79": 9300, "31": 2080, "74": 2600, "75": 3200, "27": 1450,
        "22": 1350, "48": 1190, "77": 1170, "38": 3700, "40": 3400, "24": 1880
    }

    rows = []
    np.random.seed(42)  # Đảm bảo tính tái lập kết quả nhất quán
    
    for year in years:
        nat_grdp = NATIONAL_GRDP_BASE.get(year, 10000000)
        nat_ghg = NATIONAL_GHG_BASE.get(year, 500.0)
        growth_factor = 1.0 + (year - 2015) * 0.065
        
        for prov in PROVINCES_CATALOG:
            code = prov["code"]
            name = prov["name"]
            share = prov["grdp_share"]
            is_hub = prov["hub"]
            
            # 1. Tính GRDP tỉnh (tỷ đồng)
            prov_grdp = round(nat_grdp * share * (1.0 + np.random.uniform(-0.02, 0.02)), 2)
            
            # 2. Dân số (người)
            base_pop_k = POPULATION_BASE.get(code, int(prov["area"] * 0.25 + 800))
            pop_actual = int(base_pop_k * 1000 * (1.0 + (year - 2015) * 0.011))
            
            # 3. Giá trị sản xuất công nghiệp (tỷ đồng)
            ind_ratio = 0.55 if is_hub else 0.30
            ind_output = round(prov_grdp * ind_ratio * (1.0 + np.random.uniform(-0.03, 0.03)), 2)
            
            # 4. Độ che phủ rừng (%)
            if prov["region"] in ["Trung du & Miền núi phía Bắc", "Tây Nguyên"]:
                forest_pct = round(np.random.uniform(52.0, 68.0), 1)
            elif prov["region"] == "Bắc Trung Bộ & Duyên hải miền Trung":
                forest_pct = round(np.random.uniform(45.0, 58.0), 1)
            else:
                forest_pct = round(np.random.uniform(5.0, 22.0), 1)
                
            # 5. Ước tính phát thải CO2e địa phương (triệu tấn CO2e)
            # Tỉnh trọng điểm công nghiệp (nhiệt điện, xi măng, thép) gánh tỷ trọng phát thải cao hơn tỷ trọng GRDP
            emission_weight = share * (1.6 if is_hub else 0.75)
            est_carbon_mt = round(nat_ghg * emission_weight * (1.0 + np.random.uniform(-0.04, 0.04)), 3)
            
            # Đổi sang Tấn CO2e (1 Mt = 1,000,000 tấn)
            est_carbon_tonnes = round(est_carbon_mt * 1_000_000, 0)
            
            # 6. Decoupling Index (Tấn CO2e / Tỷ đồng GRDP)
            decoupling_index = round(est_carbon_tonnes / prov_grdp, 2)
            
            rows.append({
                "Year": year,
                "Province_Code": code,
                "Province_Name": name,
                "GRDP_Billion_VND": prov_grdp,
                "Population": pop_actual,
                "Industrial_Output_Billion_VND": ind_output,
                "Forest_Coverage_Pct": forest_pct,
                "Estimated_Carbon_Tonnes": est_carbon_tonnes,
                "Decoupling_Index": decoupling_index
            })
            
    df_econ = pd.DataFrame(rows)
    df_econ = df_econ.sort_values(["Year", "Province_Code"]).reset_index(drop=True)
    return df_econ

def run_gso_data_preparation():
    """
    Thực thi quy trình chuẩn hóa dữ liệu 63 tỉnh thành Việt Nam.
    """
    logger.info("Bat dau khoi tao danh muc chuan 63 tinh thanh (Dim_Province)...")
    df_dim = build_dim_provinces_master()
    dim_path = REFERENCE_DIR / "dim_provinces_master.csv"
    save_csv(df_dim, dim_path)
    logger.info(f"-> Da tao {len(df_dim)} tinh thanh trong danh muc chuan.")

    logger.info("Bat dau tao chuoi so lieu kinh te va phat thai dia phuong 2015-2024...")
    df_econ = build_provincial_economy_series()
    econ_path = STAGING_DIR / "gso_provincial_economy.csv"
    save_csv(df_econ, econ_path)
    logger.info(f"-> Da tao {len(df_econ)} ban ghi kinh te dia phuong cho 63 tinh.")

    return df_dim, df_econ

if __name__ == "__main__":
    df_dim, df_econ = run_gso_data_preparation()
    print("\n--- 5 DÒNG DANH MỤC TỈNH (DIM_PROVINCE) ---")
    print(df_dim.head())
    print("\n--- 5 DÒNG KINH TẾ ĐỊA PHƯƠNG (STAGING) ---")
    print(df_econ.head())
    print(f"\nTổng số tỉnh: {len(df_dim)}")
    print(f"Tổng số bản ghi kinh tế: {len(df_econ)} (63 tỉnh x 10 năm)")
