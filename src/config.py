# src/config.py

from pathlib import Path

# --- 專案根目錄 ---
# Path(__file__) 會取得目前檔案的路徑
# .parent.parent 會往上兩層，到達專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 路徑設定 ---
PATHS = {
    "raw_data": BASE_DIR / "data" / "raw" / "Output2.csv",
    "image_folder": BASE_DIR / "data" / "raw" / "himawari_images/",
    "processed_data_daily": BASE_DIR / "data" / "processed" / "elevation_data_{date}.csv",
    "processed_data_resampled": BASE_DIR / "data" / "processed" / "elevation_data_{date}_10min.csv",
    "output_video": BASE_DIR / "output" / "Ocean_ISW_Analysis_{date}_widescreen.mp4"
}

# --- 資料處理參數 ---
DATA_PARAMS = {
    "target_date": "20190607"
}

# --- 視覺化參數 ---
VIZ_PARAMS = {
    "figure_size": (14, 7),
    "sensor_coords": {
        "lon": 119 + (14.4 / 60),
        "lat": 20 + (36 / 60)
    },
    "isw_threshold": 0.01,
    "plot_titles": {
        "super_title": "Ocean ISW Analysis - South China Sea",
        "satellite": "Satellite Image",
        "status": "Current Status",
        "timeseries": "Elevation Time Series"
    },
    "animation": {
        "interval": 500,  # 每幀之間的毫秒數
        "fps": 2          # 輸出影片的幀率
    }
}