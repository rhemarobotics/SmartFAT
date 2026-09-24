# 8.7. 機器視覺與機器人協同作業

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

## 📋 實習 8.7.1：機器視覺與機器人協同作業 (Vision-Guided Robotic Pick & Place)

> 實習目標：
整合 OpenCV 影像辨識與智慧型機器人控制技術。系統需自動檢測顏色方塊的輪廓中心點，並將計算出的世界座標傳送至機器人，實現自動化夾取並精準放置到對應顏色區域的「視覺導引分檢」任務。
> 

---

### ⚙️ 動作要求與前置作業

- **前置作業**：
    1. 確定系統中 **OpenCV** 與 **OpenCV-Python3** 環境已正確安裝。
    2. 檢查相機鏡頭蓋是否移除，確認檢測區域光線充足且均勻。
- **動作要求**：
    1. 將顏色方塊置於相機下方的檢測區域。
    2. 執行範例程式 `sudo python3 ColorSortMoving.py`。
    3. 系統將自動進行色彩辨識並定位中心點，隨後通知機器人執行夾取動作。
    4. 機器人將自動把方塊移動至對應的顏色置放區域。
    5. 按下 **【ESC 鍵】** 可隨時結束程式並重置機器人位置。

---

### 💻 範例程式碼：ColorSortMoving.py

Python

```jsx
'''-------------------------------------------------------
單位：雷瑪機器人科技有限公司 (Rhema Robotics)
功能：透過視覺辨識與定位, 實現目標物顏色分檢並機器人夾取置物控制範例
說明：把目標物放置於相機下方執行程式，相機辨識並定位後，機器人執行夾取動作。
執行：sudo python3 ColorSortMoving.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import sys
# 載入機器人運動控制、擴充板 SDK 與視覺辨識功能函式庫
sys.path.append('/home/pi/RhemaRobotics/Robot/')
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
sys.path.append('/home/pi/RhemaRobotics/Vision/')
import time
import math
import threading
import cv2
import numpy as np
import Board as board
import Transform as tf
from RobotControl import Robot
from package import opencvfunc, Camera

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# --- 全域變數定義 ---
stat_IsRunning = False    # 記錄機器人目前是否正處於運動執行狀態
stat_Stop = False         # 觸發機器人停止的旗標
stat_Count = 0            # 用於穩定位置的採樣計數器
stat_T1 = 0               # 時間戳記，用於判斷位置穩定時間
stat_StartPickUp  = False # 是否已確認目標穩定並開始執行抓取流程
stat_StartCountT1 = True  # 是否開始進行時間計量
stat_CenterList = []      # 存放連續偵測到的位置數據，用於計算平均值以濾除抖動

targ_SetColor = ''        # 使用者設定欲分檢的目標顏色
targ_DetColor = 'None'    # 當前影像偵測到的顏色結果
targ_RotatAngle = 0       # 偵測到目標物的旋轉角度 (Degree)
targ_WorldX, targ_WorldY = 0, 0 # 目標物在機器人世界座標系中的位置
targ_LastX, targ_LastY = 0, 0   # 記錄上一次偵測的位置，用於計算移動距離

# 建立機器人控制物件
myBot = Robot()

## 設置目標顏色函式
def setTargetColor(target_color):
    global targ_SetColor
    targ_SetColor = target_color
    return True, ()

## 機器人硬體初始化程序
def initRobot():
    myBot.openGripper()  # 開啟夾爪
    time.sleep(1)
    myBot.resetGripper() # 夾爪旋轉角度歸零
    time.sleep(1)
    # 移動至預設觀測點 (x=0, y=15, z=15)
    print(myBot.gotoPoint((0, 15, 15), -30, -90, 0, 500))
    time.sleep(0.5)

## 狀態機重置函式
def reset():
    global targ_SetColor, targ_DetColor, stat_Stop, stat_Count
    global stat_StartPickUp, stat_StartCountT1, stat_IsRunning, stat_CenterList
    targ_SetColor = ()
    targ_DetColor = 'None'
    stat_Stop = False
    stat_Count = 0
    stat_StartPickUp = False
    stat_StartCountT1 = True
    stat_IsRunning = False    
    stat_CenterList = []
    
def init():
    print("機器人初始化運動")
    initRobot() 

def start():
    global stat_IsRunning
    reset()
    stat_IsRunning = True
    print("機器人顏色分檢程式開始")

def stop():
    global stat_Stop, stat_IsRunning
    stat_Stop = True
    stat_IsRunning = False
    print("機器人顏色分檢程式結束")

def exit():
    global stat_Stop, stat_IsRunning
    stat_Stop = True
    stat_IsRunning = False
    print("機器人顏色分檢程式")

## 機器人夾取與放置目標物動作程序 (背景執行緒)
def robotPicknPlace():
    global stat_Stop, stat_IsRunning, stat_StartPickUp    
    global targ_DetColor, targ_RotatAngle, targ_WorldX, targ_WorldY

    unreachable = False 

    # 定義紅、綠、藍三色方塊的預設置放目標世界座標
    coordinate = {
        'red':   (-5, 17, 3),
        'green': (3,  17, 3),
        'blue':  (0,  15, 3)
    }
    
    while True:
        if stat_IsRunning:
            # 當視覺系統確認目標顏色且位置穩定 (stat_StartPickUp 為 True) 時執行
            if targ_DetColor != 'None' and stat_StartPickUp:
                myBot.openGripper()
                time.sleep(1)
                # 反饋：設置擴充板 LED 燈號與目標物顏色同步
                board.setboardRGB(targ_DetColor)
                time.sleep(0.1)
                board.setboardRGB('')
                # 步驟1：移動到目標位置上方 (高度 12cm) 進行預備
                result = myBot.gotoPoint((targ_WorldX, targ_WorldY, 12), -90, -90, 0)  
                if result == False:
                    unreachable = True
                    print('目標物位置超出機器人工作範圍，無法到達...')
                else:
                    unreachable = False
                    time.sleep(result[2]/1000) # 等待機器人移動完成
                    board.setBuzzerTimer(0.1)  # 抵達上方後蜂鳴器短響

                    if not stat_IsRunning: continue
                    
                    # 步驟2：調整夾爪 Roll 軸角度，對齊方塊旋轉角
                    rollAngle = tf.getAngle(targ_WorldX, targ_WorldY, targ_RotatAngle) 
                    myBot.rollGripper(rollAngle)
                    time.sleep(1)
                    
                    # 步驟3：下降至抓取高度 (8.5cm)
                    if not stat_IsRunning: continue
                    myBot.gotoPoint((targ_WorldX, targ_WorldY, 8.5), -90, -90, 0, 800)
                    time.sleep(0.8)

                    # 步驟4：關閉夾爪夾取目標
                    if not stat_IsRunning: continue
                    myBot.closeGripper()
                    time.sleep(1)

                    # 步驟5：抬起目標物至安全高度
                    if not stat_IsRunning: continue
                    myBot.gotoPoint((targ_WorldX, targ_WorldY, 12), -90, -90, 0, 1000)
                    time.sleep(1)
                    
                    # 步驟6：移動至對應顏色的置放點上方
                    if not stat_IsRunning: continue
                    result = myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], 10), -90, -90, 0)
                    time.sleep(result[2]/1000)
                    time.sleep(1)
                    
                    # 步驟7：重置夾爪旋轉角度並下降至置放高度
                    if not stat_IsRunning: continue                   
                    myBot.resetGripper()
                    time.sleep(1)

                    if not stat_IsRunning: continue
                    myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], coordinate[targ_DetColor][2] + 2),
                                    -90, -90, 0, 500)
                    time.sleep(1)
                    
                    # 步驟8：釋放夾爪，完成置物
                    if not stat_IsRunning: continue
                    myBot.openGripper()
                    time.sleep(1)

                    # 步驟9：抬起並返回初始位置
                    if not stat_IsRunning: continue
                    myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], 12), -90, -90, 0, 800)
                    time.sleep(0.8)

                    initRobot()  
                    time.sleep(1.5)
                    
                    # 本次分檢任務結束，重置視覺標籤以等待下一個目標
                    stat_StartPickUp = False
                    targ_DetColor = 'None'
                    board.setboardRGB('')
        else:
            # 停止狀態下的安全復位動作
            if stat_Stop:
                stat_Stop = False
                myBot.resetGripper()
                time.sleep(1)
                myBot.gotoPoint((0, 10, 10), -30, -30, -90, 1500)
                time.sleep(1.5)
            time.sleep(0.01)

# 啟動機器人運動執行緒，避免阻塞視覺辨識主程式
th = threading.Thread(target=robotPicknPlace)
th.setDaemon(True)
th.start()    

## 視覺辨識與定位計算副程式
def run(img):
    global stat_IsRunning, stat_StartPickUp, targ_SetColor, targ_DetColor
    global targ_RotatAngle, targ_LastX, targ_LastY, targ_WorldX, targ_WorldY
    global stat_Count, stat_StartCountT1, stat_T1, stat_CenterList
        
    size = (640, 480)
    cam_X, cam_Y = 0, 0

    # 繪製畫面中心十字線
    opencvfunc.drawCrossLine(img)
    
    # 基礎影像預處理：縮放、模糊化、色彩空間轉換
    img_resize = cv2.resize(img.copy(), size, interpolation=cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    
    # 當機器人處於待命狀態，尋找目標物
    if not stat_StartPickUp:
        # 進行色彩過濾與輪廓偵測
        imgcanny = opencvfunc.filterColour(img_lab, targ_SetColor)
        imgproc, cam_X, cam_Y, targ_RotatAngle = opencvfunc.getContours(imgcanny, img_resize, cam_X, cam_Y, targ_RotatAngle)
        
        # 若在畫面中偵測到物體
        if cam_X != 0 and cam_Y != 0:           
            # 座標轉換：將像素座標轉為世界座標
            targ_WorldX, targ_WorldY = tf.convertCoordinate(cam_X, cam_Y, size)
            
            # 在畫面上繪製即時定位資訊與顏色標籤
            cv2.putText(imgproc, '(' + str(targ_WorldX) + ', ' + str(targ_WorldY) + ', ' + str(targ_RotatAngle) + ')',
                        (cam_X+10, cam_Y+10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, opencvfunc.range_rgb['green'], 1)
            targ_DetColor = targ_SetColor
            cv2.putText(imgproc, "Color: " + targ_DetColor, (cam_X-10, cam_Y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                opencvfunc.range_rgb["black"], 2)
            
            # 穩定度判斷：計算物體移動距離以確保位置固定
            distance = math.sqrt(pow(targ_WorldX - targ_LastX, 2) + pow(targ_WorldY - targ_LastY, 2))
            targ_LastX, targ_LastY = targ_WorldX, targ_WorldY
            
            # 若物體靜止不動 (移動距離 < 0.5cm)
            if distance < 0.5:
                stat_CenterList.extend((targ_WorldX, targ_WorldY))
                stat_Count += 1
                if stat_StartCountT1:
                    stat_StartCountT1 = False
                    stat_T1 = time.time()
                
                # 持續靜止超過 1 秒後，鎖定平均位置並通知機器人開始夾取
                if time.time() - stat_T1 > 1.0:
                    stat_StartCountT1 = True
                    targ_WorldX, targ_WorldY = np.mean(np.array(stat_CenterList).reshape(stat_Count, 2), axis=0)
                    stat_Count = 0
                    stat_CenterList = []
                    stat_StartPickUp = True # 觸發機器人夾取任務
            else:
                # 若物體仍在移動，則重新計時
                stat_T1 = time.time()
                stat_StartCountT1 = True
                stat_CenterList = []
                stat_Count = 0
            return imgproc        
        else:
            print('找不到目標物')
    return img            

# 主程式入口
if __name__ == '__main__':
    print('主程式開始, 按下 ESC 鍵離開...')
    
    # 執行機器人初始化與程式邏輯啟動
    init()
    start()
    
    # 設定檢測目標顏色 (預設為紅色 red)
    setTargetColor('red')
    
    # 開啟相機進行即時視覺辨識
    my_camera = Camera.Camera()
    my_camera.camera_open()
    
    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            # 執行辨識與定位邏輯
            Frame = run(frame)
            cv2.imshow('Frame', Frame)
            
            key = cv2.waitKey(1)
            if key == 27: # 按下 ESC 結束
                break
                
    # 關閉資源
    my_camera.camera_close()
    cv2.destroyAllWindows()
```

---

### 📝 技術重點解析 (University Level)

1. **多執行緒架構 (Multi-threading)**：
由於視覺辨識 (`run`) 運算較快且需維持即時畫面更新，而機器人運動 (`robotPicknPlace`) 較慢且包含許多延時等待。本程式使用 `threading.Thread` 將運動控制獨立執行，確保相機畫面不會在機器人移動時卡頓。
2. **位置穩定濾波 (Stability Filtering)**：
為了避免因影像雜訊導致座標微小跳動而影響夾取精準度，程式實作了穩定度判斷：只有當物體連續靜止超過 1 秒，且移動距離在 0.5 單位（如 cm）以內時，才會計算平均座標並觸發機器人動作。
3. **座標變換與姿態對齊**：
`tf.convertCoordinate` 實現了 2D 影像平面到 3D 物理空間的映射；`tf.getAngle` 則結合了目標物的旋轉角，讓夾爪在下降前預先轉向正確的角度，確保能穩定夾持長方形或正方形方塊。

---

### 📷 實習成果紀錄

- **顏色辨識準確性**：(記錄系統是否能正確區分並標註紅、藍、綠方塊)
- **抓取精準度**：(觀察夾爪中心是否準確對準方塊中心，及旋轉角度是否一致)
- **執行截圖**：
    - [ ]  成功在畫面上顯示包含 (X, Y, Angle) 的視覺標籤。
    - [ ]  機器人成功將方塊移動至正確的顏色置放點。