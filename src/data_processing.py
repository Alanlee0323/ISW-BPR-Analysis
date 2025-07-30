# src/data_processing.py

import pandas as pd

def filter_by_date(raw_path: str, output_path: str, target_date: str) -> pd.DataFrame:
    """
    從原始 CSV 中篩選出指定日期的資料並儲存。
    """
    print(f"Reading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)
    df['Time'] = pd.to_datetime(df['Time'])
    
    year, month, day = int(target_date[0:4]), int(target_date[4:6]), int(target_date[6:8])
    
    filtered_df = df[
        (df['Time'].dt.year == year) & 
        (df['Time'].dt.month == month) & 
        (df['Time'].dt.day == day)
    ]
    
    result_df = filtered_df.sort_values(by='Time')[['Time', 'Elevation']]
    
    result_df.to_csv(output_path, index=False)
    print(f"Filtered data for {target_date} saved to: {output_path}")
    return result_df

def resample_to_10min(daily_data_path: str, output_path: str) -> pd.DataFrame:
    """
    將每日資料重採樣為 10 分鐘間隔。
    """
    print(f"Reading daily data from: {daily_data_path}")
    df = pd.read_csv(daily_data_path)
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)
    
    # 'min' 是 pandas 建議的新寫法，取代 'T'
    resampled_df = df.resample('10min').mean().reset_index()
    
    if 'Elevation' in resampled_df.columns:
        resampled_df['Elevation'] = resampled_df['Elevation'].round(4)
    
    resampled_df.to_csv(output_path, index=False)
    print(f"Resampled data saved to: {output_path}")
    return resampled_df