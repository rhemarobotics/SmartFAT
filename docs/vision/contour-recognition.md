# 8.5. 輪廓(Contour)辨識實習

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

## 📋 實習 8.5.1：方塊外觀輪廓邊緣檢測 (Shape Contour Detection)

> 實習目標：
透過 OpenCV 影像處理技術，針對相機視野內的顏色方塊進行邊緣檢測與輪廓追蹤。本實習旨在讓學生掌握如何從色彩過濾後的影像中提取幾何輪廓，並計算出目標物的中心座標與旋轉角度。
> 

---

### ⚙️ 動作要求與前置作業

- **前置作業**：
    1. 確定系統已正確安裝 **OpenCV** 與 **OpenCV-Python3** 環境。
    2. 檢查並確認相機鏡頭蓋已移除。
- **動作要求**：
    1. 放置一顏色方塊（範例預設為紅色）於相機視覺範圍內。
    2. 執行路徑下的範例程式 `/home/pi/RhemaRobotics/Vision/ShapeSorting.py`。
    3. 進行外觀輪廓邊緣檢測，觀察視窗中是否成功繪製出方塊的邊緣線條。
    4. 按下鍵盤 **【ESC 鍵】** 即可結束程式執行。

---

### 💻 範例程式碼：ShapeSorting.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：透過 opencv 實現目標物輪廓的視覺辨識
說明：放置一方塊位於相機擷取範圍內,進行輪廓辨識
    當按下 ESC 停止程式
執行：直接執行此檔案程式
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
import cv2
import numpy as np
# 載入雷瑪專用影像處理函式庫與相機驅動模組
from package import opencvfunc, Camera

# 初始化目標顏色變數
__target_color = ''
# 設定預設繪圖顏色為黑色
draw_color = opencvfunc.range_rgb["black"]

## 設置欲辨識目標物色彩
def setTargetColor(target_color):
    global __target_color
    __target_color = target_color
    return True, ()

## 分辨輪廓的視覺辨識副程式
def run(img):
    
    # 1. 宣告座標與旋轉變數 (cx, cy 為質心, rot 為旋轉角度)
    cx = cy = rot = 0
    
    # 2. 輔助標記：在影像中心繪製十字參考線
    opencvfunc.drawCrossLine(img)
    
    # 3. 影像預處理：
    # - resize: 調整影像大小至 640x480 以提升處理效能
    # - GaussianBlur: 進行高斯模糊化，去除高頻雜訊
    # - cvtColor: 將影像轉為 LAB 色彩空間，以獲得更穩定的色彩過濾效果
    img_resize = cv2.resize(img.copy(), (640, 480), interpolation = cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    
    # 4. 顏色過濾：利用 LAB 空間根據指定顏色進行過濾，取得二值化邊緣影像 (Canny)
    imgcanny = opencvfunc.filterColour(img_lab, __target_color)
    
    # 5. 輪廓偵測：
    # 呼叫雷瑪函式 getContours，從邊緣影像中提取目標物輪廓並回傳標註後的結果
    imgproc, cx, cy, rot = opencvfunc.getContours(imgcanny, img_resize, cx, cy, rot)
    return imgproc

# 主程式開始
if __name__ == '__main__':
    
    # 設定欲辨識目標物的顏色 (範例預設為紅色 'red')
    setTargetColor('red')
    
    # 宣告並初始化相機物件
    my_camera = Camera.Camera()
    
    # 開啟相機進行串流擷取
    my_camera.camera_open()

    while True:
        # 從相機物件中擷取當前一幀影像
        img = my_camera.frame
        if img is not None:
            # 複製影像以確保不影響原始緩衝區
            frame = img.copy()
            # 執行輪廓辨識運算
            Frame = run(frame)
            # 顯示處理後含有輪廓標註的影像結果
            cv2.imshow('Frame', Frame)
            
            # 偵測鍵盤按鍵，若偵測到 ESC 鍵 (ASCII 27), 則跳出無窮迴圈
            key = cv2.waitKey(1)
            if key == 27:
                break
                
    # 程式結束流程：關閉相機硬體並銷毀所有視窗資源
    my_camera.camera_close()
    cv2.destroyAllWindows()
```

---

### 📝 實習技術細節解析

1. **影像預處理流 (Pipeline)**：
本程式依序執行了 **Resize → Blur → LAB轉換**。其中 `GaussianBlur` (高斯模糊) 在輪廓檢測中至關重要，它能有效減少影像中的細微雜點，避免 `filterColour` 產生過多碎小的偽輪廓。
2. **`opencvfunc.getContours` 函式**：
此為實習 8.7 的核心，它不僅找出物體的邊緣，還執行了「最小外接矩形」運算，因此能回傳物體的中心座標 `(cx, cy)` 以及在平面上的旋轉角度 `rot`。
3. **LAB 空間與顏色過濾**：
透過 `img_lab` 進行 `filterColour`，這比傳統的 RGB 或 HSV 辨識更具魯棒性，能減少工業現場環境光源變化對輪廓偵測的干擾。

---

### 📷 實驗成果紀錄

- **檢測狀態**：(描述方塊邊緣是否被綠色或指定顏色線條完整包圍)
- **穩定度觀察**：(當旋轉方塊時，觀察視窗中的輪廓線是否能即時跟隨)
- **執行截圖**：
    - [ ]  成功在畫面上顯示紅方塊的外觀輪廓。
        
        ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%205%20%E8%BC%AA%E5%BB%93%28Contour%29%E8%BE%A8%E8%AD%98%E5%AF%A6%E7%BF%92/image.png)