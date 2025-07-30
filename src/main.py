# src/main.py

import pandas as pd
from config import PATHS, DATA_PARAMS, VIZ_PARAMS
from data_processing import filter_by_date, resample_to_10min
from visualization import create_isw_animation

def main():
    """
    專案主執行流程
    """
    target_date = DATA_PARAMS['target_date']
    
    # --- 步驟 1: 資料處理 ---
    print("--- Starting Data Processing ---")
    
    # 格式化檔案路徑字串
    daily_path = str(PATHS['processed_data_daily']).format(date=target_date)
    resampled_path = str(PATHS['processed_data_resampled']).format(date=target_date)
    video_path = str(PATHS['output_video']).format(date=target_date)

    # 執行資料篩選與重採樣
    filter_by_date(
        raw_path=PATHS['raw_data'],
        output_path=daily_path,
        target_date=target_date
    )
    
    resampled_df = resample_to_10min(
        daily_data_path=daily_path,
        output_path=resampled_path
    )
    
    print("\n--- Data Processing Complete ---")
    
    # --- 步驟 2: 視覺化 ---
    print("--- Starting Visualization ---")
    
    # 將更新後的影片路徑放回 config 字典中傳遞
    config = {
        "PATHS": {**PATHS, "output_video": video_path},
        "VIZ_PARAMS": VIZ_PARAMS
    }
    
    create_isw_animation(
        resampled_df=resampled_df,
        config=config
    )
    
    print("\n--- Process Finished ---")


if __name__ == "__main__":
    main()