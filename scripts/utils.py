import os
import sys
import json
import logging
from pathlib import Path
import pandas as pd

# Thiết lập stdout/stderr hỗ trợ UTF-8 trên Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thiết lập đường dẫn thư mục gốc
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
STAGING_DIR = DATA_DIR / "staging"
REFERENCE_DIR = DATA_DIR / "reference"

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("NetZero_Ingestion")

def ensure_directories():
    """Tạo tất cả các thư mục cần thiết nếu chưa tồn tại."""
    for directory in [DATA_DIR, RAW_DIR, STAGING_DIR, REFERENCE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    logger.info("Da khoi tao day du cac thu muc du lieu: raw, staging, reference.")

def save_json(data: dict | list, filepath: Path | str) -> Path:
    """Lưu dữ liệu dict/list ra file JSON định dạng UTF-8."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Da luu file JSON: {path.name} ({path.stat().st_size} bytes)")
    return path

def load_json(filepath: Path | str) -> dict | list:
    """Đọc dữ liệu từ file JSON định dạng UTF-8."""
    path = Path(filepath)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_csv(df: pd.DataFrame, filepath: Path | str) -> Path:
    """
    Lưu DataFrame ra file CSV với mã hóa UTF-8 with BOM (utf-8-sig).
    Rất quan trọng cho SQL Server SSIS và Excel hiển thị đúng tiếng Việt có dấu.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info(f"Da luu file CSV: {path.name} ({len(df)} dong)")
    return path

if __name__ == "__main__":
    ensure_directories()
    print(f"Cấu trúc thư mục dữ liệu đã sẵn sàng tại: {DATA_DIR}")
