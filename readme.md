# 海洋內孤立波 (ISW) 分析與視覺化專案

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

此專案為一個海洋內孤立波 (ISW) 的分析流程，能整合衛星影像與感測器數據並生成動態視覺化影片。

## 專案簡介

本專案旨在提供一個自動化的 Python 工作流程，用於分析南海地區的海洋內孤立波 (Internal Solitary Wave, ISW) 事件。它會讀取原始的海底壓力計 (BPR) 時間序列資料與對應時間的 Himawari-8 衛星影像，經過資料清洗、篩選與重採樣後，最終生成一段同步的動畫影片。

影片的視覺化儀表板可以讓研究人員直觀地比對感測器數據的變化與衛星影像上的海面特徵，輔助 ISW 事件的分析與研究。

## 功能特色

- **自動化資料處理**: 從原始資料 (`Output2.csv`) 自動篩選指定日期並進行時間重採樣。
- **同步視覺化**: 將時間序列數據圖表與對應時間點的衛星影像同步呈現在一部動畫中。
- **動態狀態儀表板**: 即時顯示當前時間、海面高程數值以及根據門檻值判斷的狀態 (Normal/ISW)。
- **模組化與可配置**: 程式碼結構清晰，所有檔案路徑、參數與圖表標題皆可在 `src/config.py` 中輕鬆設定。
- **高品質影片輸出**: 使用 `ffmpeg` 產生適用於報告或簡報的 MP4 格式影片。

## 專案結構

```
ocean_isw_analysis/
│
├── data/
│   ├── raw/
│   │   ├── Output2.csv                # 原始資料檔
│   │   └── satellite_images/          # 衛星影像資料夾
│   │
│   └── processed/                     # 存放處理後的資料
│
├── src/
│   ├── config.py                      # 存放所有設定參數
│   ├── data_processing.py             # 資料處理模組
│   ├── visualization.py              # 視覺化與動畫模組
│   └── main.py                        # 專案主執行檔
│
├── output/                            # 存放最終輸出的影片
│
├── .gitignore                         # Git 忽略清單
├── README.md                          # 專案說明文件
└── requirements.txt                   # Python 套件依賴列表
```

## 環境需求

- Python 3.8 或更高版本
- pip (Python 套件安裝工具)
- **ffmpeg**: 必須安裝於您的系統中才能儲存 MP4 影片。您可以從 [ffmpeg 官網](https://ffmpeg.org/download.html) 下載。

## 安裝與設定

1. **下載或 Clone 此專案**
   ```bash
   git clone [您的專案 Git Repo URL]
   cd ocean_isw_analysis
   ```

2. **安裝所需套件**
   ```bash
   pip install -r requirements.txt
   ```

3. **準備資料**
   - 將原始的 `Output2.csv` 檔案放置於 `data/raw/` 資料夾下。
   - 將所有衛星影像 (`.png` 格式) 放置於 `data/raw/satellite_images/` 資料夾下。

## 使用方法

1. **(可選) 調整設定**: 打開 `src/config.py` 檔案，您可以根據需求修改 `DATA_PARAMS` 中的 `target_date` 或其他視覺化參數。
2. **執行主程式**: 在專案根目錄下，執行以下指令：
   ```bash
   python src/main.py
   ```
3. **查看結果**: 程式將會開始執行。首先進行資料處理，然後生成動畫。執行完畢後，最終的 `.mp4` 影片將會儲存在 `output/` 資料夾中。

## 輸出範例

程式將生成一個 MP4 影片，畫面包含三個主要部分：
- **左側**: 顯示衛星影像，並標示出 BPR 感測器的位置。
- **右上**: 顯示當前時間、海面高程及狀態的儀表板。
- **右下**: 顯示完整的海面高程時間序列圖，並有一條垂直藍線指示當前動畫的時間點。

## 授權

本專案採用 [MIT License](https://opensource.org/licenses/MIT) 授權。