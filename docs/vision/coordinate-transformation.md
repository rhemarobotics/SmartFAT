# 8.6. 計算目標物中心位置與座標轉換

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

## 📋 實習 8.6.1：計算目標物中心位置與座標轉換 (Centroid & Coordinate Transform)

> 實習目標：
透過 OpenCV 影像辨識定位顏色方塊，並計算其輪廓中心點位置。本實驗的核心在於將「相機影像座標系」轉換為「機器人世界座標系」，使機械手臂能根據計算出的真實位置進行精確抓取。
> 

---

### ⚙️ 動作要求與前置作業

- **前置作業**：
    1. 確定系統中 **OpenCV** 與 **OpenCV-Python3** 環境已正確安裝。
    2. 確認相機鏡頭蓋已移除，並確保工作區域光線穩定。
- **動作要求**：
    1. 將一顏色方塊放置於相機視覺擷取範圍內。
    2. 執行範例程式 `/home/pi/RhemaRobotics/Vision/CalcCenterPosition.py`。
    3. 程式將自動搜尋目標顏色、計算中心點，並將座標轉換為相對於機器人原點的世界座標。
    4. 按下鍵盤 **【ESC 鍵】** 結束程式。

---

### 💻 範例程式碼：CalcCenterPosition.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：透過 opencv 視覺辨識, 計算目標物中心相對於世界座標系的位置
說明：放置一方塊位於相機擷取範圍內, 進行位置計算
    當按下 ESC 停止程式
執行：直接執行此檔案程式
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
# 加入雷瑪專用套件與 SDK 路徑
sys.path.append('/home/pi/RhemaRobotics/Vision/package/')
sys.path.append('/home/pi/RhemaRobotics/Sdk')
import cv2
import numpy as np
import opencvfunc, Camera
import Transform as tf
from package.calibration import CalibrationConfig

## 全域變數定義
__target_color = ''           # 設定欲辨識物件的顏色字串 (如 'red', 'blue')
cam_X, cam_Y = 0, 0           # 儲存物件中心在影像像素座標系 (Pixel) 中的位置
world_X, world_Y = 0, 0       # 儲存物件中心轉換後在機器人世界座標系 (mm) 中的位置
size = CalibrationConfig.size # 從校正設定檔讀取擷取的影像解析度大小
sqrlength = CalibrationConfig.square_length # 讀取物件實際邊長設定

## 設置欲辨識目標物色彩
def setTargetColor(target_color):
    global __target_color
    __target_color = target_color
    return True, ()

## 計算目標物中心位置的視覺辨識副程式
def run(img):
    
    # 宣告全域變數以供更新座標數據
    global cam_X, cam_Y
    global world_X, world_Y
    cam_X, cam_Y, rot = 0, 0, 0
    
    # 1. 輔助繪製：在影像中心畫十字參考線
    opencvfunc.drawCrossLine(img)
    
    # 2. 影像預處理：
    # - resize: 調整影像尺寸至校正設定大小
    # - GaussianBlur: 高斯模糊濾除影像噪點
    # - cvtColor: 轉換至 LAB 色彩空間提升顏色過濾穩定性
    img_resize = cv2.resize(img.copy(), size, interpolation=cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    
    # 3. 顏色辨識：根據目標顏色提取特徵
    imgcanny = opencvfunc.filterColour(img_lab, __target_color)
    
    # 4. 輪廓搜尋：計算目標物的像素中心位置 (cam_X, cam_Y) 與旋轉角度 (rot)
    imgproc, cam_X, cam_Y, rot = opencvfunc.getContours(imgcanny, img_resize, cam_X, cam_Y, rot)
    
    # 5. 座標轉換與顯示結果
    if cam_X != 0 and cam_Y != 0:
        # 關鍵步驟：調用 Transform 套件將影像像素座標轉換為實際世界座標
        world_x, world_y = tf.convertCoordinate(cam_X, cam_Y, size)
        # 將旋轉角度四捨五入至小數點後兩位
        rot = round(rot, 2)
        
        # 於影像畫面上繪製目標物資訊 (顯示格式：世界座標 X, Y 與 旋轉角)
        cv2.putText(imgproc, '(' + str(world_x) + ', ' + str(world_y) + ', ' + str(rot) +')', (cam_X+10, cam_Y+10),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, opencvfunc.range_rgb['black'], 1)
    else:
        print('找不到目標物')
    
    return imgproc

# 主程式進入點
if __name__ == '__main__':
    
    # 設置欲辨識的顏色為紅色 ('red')
    setTargetColor('red')
    
    # 建立相機驅動物件
    my_camera = Camera.Camera()
    # 開啟相機鏡頭
    my_camera.camera_open()
    
    # 進入視覺辨識主迴圈
    while True:
        # 獲取當前相機影格
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            # 執行座標計算與轉換副程式
            Frame = run(frame)
            # 顯示處理結果視窗
            cv2.imshow('Frame', Frame)
            
            # 偵測 ESC 鍵按下跳出迴圈
            key = cv2.waitKey(1)
            if key == 27:
                break
    
    # 關閉資源
    my_camera.camera_close()
    cv2.destroyAllWindows()
```

---

### 📝 技術重點深度解析

1. **影像座標與世界座標 (Coordinate Transformation)**：
影像中的座標是以像素 (Pixel) 為單位，而機械手臂需要的是以毫米 (mm) 為單位的世界座標。透過 `tf.convertCoordinate` 函式，程式能根據校正參數計算出物體相對於手臂原點的真實距離。
2. **CalibrationConfig 的作用**：
此腳本引用了 `CalibrationConfig`，這意味著轉換的準確性取決於相機校正的結果。如果實際抓取有偏移，需重新檢視相機與手臂的標定關係。
3. **LAB 色彩過濾**：
採用 LAB 空間而非 RGB 空間，可以有效分離亮度與顏色資訊，確保在不同室內光照強度下，系統仍能準確鎖定目標顏色方塊。

---

### 📷 實習成果紀錄

- **像素座標 (cam_X, cam_Y)**：(記錄在視窗中方塊移動時的像素變化)
- **世界座標 (world_x, world_y)**：(測量方塊在輸送帶上的實際距離，與程式顯示數值進行對比)
- **執行截圖**：
    - [ ]  成功在畫面上看到帶有 (X, Y, Rotation) 數值的目標標記。
        
        ![image.png](../assets/8%20%E6%A9%9F%E5%99%A8%E8%A6%96%E8%A6%BA%E5%AF%A6%E5%8B%99%E6%8A%80%E8%A1%93/8%206%20%E8%A8%88%E7%AE%97%E7%9B%AE%E6%A8%99%E7%89%A9%E4%B8%AD%E5%BF%83%E4%BD%8D%E7%BD%AE%E8%88%87%E5%BA%A7%E6%A8%99%E8%BD%89%E6%8F%9B/image.png)