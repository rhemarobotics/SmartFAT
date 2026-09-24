# 8.4. 色彩辨識實習

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

## 📋 實習 8.4：目標物顏色辨識 (Color Identification)

> 實習目標：
透過 OpenCV 影像處理技術，針對生產線上的彩色方塊（紅、藍、綠）進行自動化顏色辨識與定位。本實習將整合色彩過濾與輪廓偵測技術，鎖定目標物並計算其在畫面中的座標與旋轉角度。
> 

---

### ⚙️ 動作要求與前置作業

- **前置作業**：
    1. 確定系統已安裝 **OpenCV** 與 **OpenCV-Python3** 環境。
    2. 檢查並確認相機鏡頭蓋已移除，且光線充足。
- **動作要求**：
    1. 將單一顏色方塊放置於相機擷取範圍內。
    2. 執行範例程式進行顏色搜尋與辨識。
    3. 觀察畫面中是否出現顏色標籤與中心點座標。
    4. 按下鍵盤 **【ESC 鍵】** 即可結束程式執行。

---

### 💻 範例程式碼：ColorSorting.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：透過 OpenCV 實現目標物顏色的視覺辨識
說明：放置一方塊於相機擷取範圍內進行辨識，按 ESC 停止。
執行：python3此檔案程式
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
import cv2
import numpy as np
# 引用雷瑪機器人專用影像處理函式庫
from package import opencvfunc, Camera

# 環境檢查：確保在 Python3 環境下運行
if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 儲存欲辨識目標顏色的全域變數
__target_color = ''

## 設置欲辨識目標物色彩 (如 'red', 'blue', 'green')
def setTargetColor(target_color):
    global __target_color
    __target_color = target_color
    return True, ()

## 分辨顏色的視覺辨識副程式
def run(img):
    # 宣告變數：cx, cy 為中心座標，rot 為旋轉角度
    cx = cy = rot = 0
    size = (640, 480)
    
    # 1. 輔助線繪製：在畫面中心畫十字線以便對位
    opencvfunc.drawCrossLine(img)
    
    # 2. 影像預處理：縮放大小並進行高斯模糊以減少背景雜訊
    img_resize = cv2.resize(img.copy(), size, interpolation=cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    
    # 3. 色彩空間轉換：轉換至 LAB 色彩模型進行更穩定的辨識
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    
    # 4. 顏色過濾：根據目標顏色提取特徵影像 (Canny 邊緣)
    imgcanny = opencvfunc.filterColour(img_lab, __target_color)
    
    # 5. 輪廓搜尋：從邊緣圖中提取物體的輪廓並計算其中心點 (cx, cy) 與轉角
    imgproc, cx, cy, rot = opencvfunc.getContours(imgcanny, img_resize, cx, cy, rot)
    
    # 6. 結果標註：若找到物體則在畫面上印出顏色名稱
    if cx != 0 and cy != 0:
        # 於物體中心位置繪製顏色標記文字
        cv2.putText(imgproc, '(' + __target_color + ')', (cx + 10, cy + 10),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, opencvfunc.range_rgb['green'], 1)       
    else:
        print('找不到目標物')
        
    return imgproc

# 主程式進入點
if __name__ == '__main__':
    
    # 設定辨識目標為藍色 ('blue')
    setTargetColor('blue')
    
    # 初始化並開啟相機鏡頭
    my_camera = Camera.Camera()
    my_camera.camera_open()
    
    # 進入即時影像辨識迴圈
    while True:
        img = my_camera.frame # 讀取當前相機影格
        if img is not None:
            frame = img.copy()
            # 執行辨識運算
            Frame = run(frame)
            # 顯示辨識結果視窗
            cv2.imshow('Frame', Frame)
            
            # 偵測鍵盤事件，按下 ESC (ASCII 27) 跳出迴圈
            key = cv2.waitKey(1)
            if key == 27:
                break
    
    # 資源釋放：關閉相機並銷毀所有視窗
    my_camera.camera_close()
    cv2.destroyAllWindows()
```

---

### 🔍 實習技術重點解析

1. **LAB 色彩空間**：
與常用的 RGB 不同，LAB 空間將亮度（L）與顏色資訊（A、B）分離。這使得程式在不同光影環境下，辨識顏色方塊的穩定度大幅提升。
2. **`opencvfunc.getContours`**：
此為 **Rhema Robotics** 封裝的核心函式，它不僅能找到方塊的邊界，還能透過影像矩運算出精確的中心點 `cx, cy`。
3. **十字中心線標記**：
透過 `drawCrossLine` 繪製的參考線，可協助實驗人員判斷方塊是否位於相機鏡頭的正下方，這對於後續機械手臂的抓取座標校正至關重要。

---

### 📷 實習成果紀錄

- **辨識成功測試**：
    - [ ]  紅色方塊
    - [ ]  藍色方塊
    - [ ]  綠色方塊
        
        ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%204%20%E8%89%B2%E5%BD%A9%E8%BE%A8%E8%AD%98%E5%AF%A6%E7%BF%92/image.png)
        
- **問題排除**：若辨識不穩定，請檢查環境光線是否過亮造成反射，或嘗試調整 `GaussianBlur` 的參數值。