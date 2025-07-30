# src/visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
from PIL import Image
import os

def create_isw_animation(resampled_df: pd.DataFrame, config: dict):
    """
    建立並儲存內孤立波分析動畫。
    """
    image_folder = config['PATHS']['image_folder']
    isw_threshold = config['VIZ_PARAMS']['isw_threshold']
    
    # --- 圖表版面配置 ---
    fig = plt.figure(figsize=config['VIZ_PARAMS']['figure_size'])
    gs = plt.GridSpec(9, 9, figure=fig)
    ax_main = fig.add_subplot(gs[0:8, 0:6])
    status_panel = fig.add_subplot(gs[0:2, 6:9])
    ax_graph = fig.add_subplot(gs[2:6, 6:9])
    
    # --- 初始化衛星影像圖 ---
    initial_img = np.ones((200, 200, 3), dtype=np.uint8) * 255
    satellite_img = ax_main.imshow(initial_img, extent=[119, 120, 20, 21])
    ax_main.set_xlabel('Longitude (°E)', fontsize=12)
    ax_main.set_ylabel('Latitude (°N)', fontsize=12)
    ax_main.set_title(config['VIZ_PARAMS']['plot_titles']['satellite'], fontsize=16, pad=10)

    sensor_lon = config['VIZ_PARAMS']['sensor_coords']['lon']
    sensor_lat = config['VIZ_PARAMS']['sensor_coords']['lat']
    ax_main.plot(sensor_lon, sensor_lat, 'y*', markersize=18, markeredgecolor='black')
    ax_main.annotate('BPR System', xy=(sensor_lon, sensor_lat), xytext=(sensor_lon+0.05, sensor_lat+0.05),
                     color='yellow', fontweight='bold', fontsize=12,
                     bbox=dict(boxstyle="round,pad=0.3", fc='black', alpha=0.7))
    
    # --- 狀態面板 ---
    status_panel.axis('off')
    status_panel.set_title(config['VIZ_PARAMS']['plot_titles']['status'], fontsize=16, pad=10)
    time_text = status_panel.text(0.05, 0.75, 'Time: ...', fontsize=13)
    elevation_text = status_panel.text(0.05, 0.5, 'Elevation: ...', fontsize=13)
    status_text = status_panel.text(0.05, 0.25, 'Status: ...', fontsize=15, fontweight='bold')
    
    # --- 時間序列圖 ---
    ax_graph.plot(resampled_df['Time'], resampled_df['Elevation'], '-o', color='black', markersize=5)
    ax_graph.axhline(y=isw_threshold, color='red', linestyle='--', label='ISW Threshold')
    ax_graph.set_ylabel('Elevation', fontsize=12)
    ax_graph.set_xlabel('Time', fontsize=12)
    ax_graph.grid(True, alpha=0.3)
    ax_graph.legend(loc='upper right')
    ax_graph.set_title(config['VIZ_PARAMS']['plot_titles']['timeseries'], fontsize=16, pad=10)
    time_line = ax_graph.axvline(x=resampled_df['Time'].iloc[0], color='blue', linestyle='-', linewidth=2)
    
    # 預先標示出超過門檻值的區域
    for i in range(len(resampled_df)-1):
        if not np.isnan(resampled_df['Elevation'].iloc[i]) and resampled_df['Elevation'].iloc[i] > isw_threshold:
            ax_graph.axvspan(resampled_df['Time'].iloc[i], resampled_df['Time'].iloc[i+1], alpha=0.3, color='red')

    # --- 動畫更新函式 (巢狀函式) ---
    def get_image_filename(timestamp):
        return f"{timestamp.strftime('%Y%m%d%H%M')}.png"

    def update(frame_idx):
        current_time = resampled_df['Time'].iloc[frame_idx]
        current_elevation = resampled_df['Elevation'].iloc[frame_idx]
        
        # 更新衛星影像
        filename = get_image_filename(current_time)
        full_path = os.path.join(image_folder, filename)
        if os.path.exists(full_path):
            try:
                img = np.array(Image.open(full_path))
                satellite_img.set_array(img)
            except Exception as e:
                print(f"Cannot read image {filename}: {e}")
        
        # 更新時間線、文字與狀態
        time_line.set_xdata([current_time])
        time_text.set_text(f'Time: {current_time.strftime("%Y-%m-%d %H:%M")}')
        
        if np.isnan(current_elevation):
            elevation_text.set_text('Elevation: No data')
            status_text.set_text('Status: Undetermined')
            elevation_text.set_color('gray')
            status_text.set_color('gray')
        else:
            elevation_text.set_text(f'Elevation: {current_elevation:.4f}')
            if current_elevation > isw_threshold:
                status = 'ISW'
                color = 'red'
            else:
                status = 'Normal'
                color = 'blue'
            status_text.set_text(f'Status: {status}')
            elevation_text.set_color(color)
            status_text.set_color(color)

        return satellite_img, time_line, time_text, elevation_text, status_text

    # --- 建立與儲存動畫 ---
    ani = animation.FuncAnimation(fig, update, frames=len(resampled_df),
                                  interval=config['VIZ_PARAMS']['animation']['interval'], blit=True)
    
    plt.suptitle(config['VIZ_PARAMS']['plot_titles']['super_title'], fontsize=20, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    output_video_path = str(config['PATHS']['output_video'])
    try:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=config['VIZ_PARAMS']['animation']['fps'], metadata=dict(artist='AI Assistant'), 
                        bitrate=1800, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])
        ani.save(output_video_path, writer=writer, dpi=100)
        print(f"Successfully saved video to: {output_video_path}")
    except Exception as e:
        print(f"Error saving video with ffmpeg: {e}")
        print("Video saving failed. Consider saving as frames or installing ffmpeg.")

    # plt.show() # 如果需要在腳本執行後顯示動畫，可以取消此行註解