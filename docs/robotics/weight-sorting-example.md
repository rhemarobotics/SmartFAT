# 7.7. 智慧機器人重量分檢範例

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

本實習模擬智慧工廠的自動化重量分檢流程，利用重量感測器測量生產線上產品的重量，根據設定的標準進行判定和分揀。這種應用常見於食品包裝或液體生產線，用於檢查產品是否符合要求。此實習可幫助學員理解重量感測與自動分揀系統的基本原理，適用於生產線的質量檢測與管理。

### 實習目標：

1. 啟動系統後，輸送帶開始運行，並手動放置產品（此處以木塊代替）在輸送帶上。
2. 當產品被輸送至定位點時，紅外線感測器偵測到產品，輸送帶會自動停下。
3. 此時，機器手臂移動到定位點，夾取產品並將其放置在重量感測器測量物件的重量。
4. 當產品重量符合出貨標準，判定為合格，產品被手臂放置於OK區。
5. 若重量未達標準，判定為不合格，產品會被剔除(放置於NG區)或系統報警停機。

### 前置作業：

預先載入Arduino智慧工廠範例程式

> /home/pi/ArduinoProjects/Programming/SmartFactoryEx3.ino
> 

### 範例程式碼

> /home/pi/RhemaRobotics/Demo/SmartFactoryEx3.py
> 

```python
'''-------------------------------------------------------
功能:Arduino與樹梅派機器人協同作業(重量分檢範例)
說明:把目標物放置於輸送帶上,機器人運動至輸送帶定點後,夾取目標物,
    置於稱重感測器下,讀取重量值,再依據設定的檢驗值,判定是否正確,
    再把目標物置於NG或OK區域
執行:sudo python3 SmartFactoryEx3.py
結束:CTRL+C
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import sys
sys.path.append('/home/pi/RhemaRobotics/Robot/')
import time
import serial
from RobotControl import Robot

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 建立一機器人物件
myBot = Robot()

# 設定與Arduino通訊的埠口
port = "/dev/ttyUSB0"

# 夾取物件檢測重量
objTargetWeigh = 25

# 物件檢測結果
isObjPass = False

# 機器人工作座標
convyPos = (15, 0, 15)
workPos = (0, 15, 15)
placePos = ((0, 19, 3.5),(0, 19.3, 8.5),(0, 18.5, 12))
objCenter = (15, 0, 9)

# 顏色方塊置放位置
coordinate = {'red':   (-5, 17, 5),
              'green': (3,  17, 5),
              'blue':  (0,  12, 4) }

# 主程式開始
if __name__ == '__main__':
    
    # 樹梅派串列埠口通訊設置
    print('串列通訊埠口開啟, 格式: 9600,8,N,1')
    slFrmArduino = serial.Serial(port, 9600)
    slFrmArduino.flushInput()    

    # 主迴圈程式
    while 1:
        print('機器人重量分類程式開始...')    
        # 機器人移動至工作點位置
        print(myBot.gotoPoint((0, 15, 15), -30, -90, 0, 500))
        time.sleep(0.5)
        # 打開機器人夾爪
        myBot.openGripper()
        time.sleep(1)   
       
        # 讀取Arduino送來的字串
        try:
            while True:
                data_raw = slFrmArduino.readline() #讀取一行
                cmd = data_raw.decode() # 用UTF-8解碼
                ss= cmd.split()
                print(ss)
                if ss[0] == 'ready':
                    time.sleep(0.5)
                    break
        except KeyboardInterrupt:
            slFrmArduino.close() # 清除串列通訊物件
            print('end of serial communication.')
            break
    
        # 機器人移動至輸送帶位置
        print(myBot.gotoPoint(convyPos, -30, -90, 0, 500))
        time.sleep(0.5)
        # 機器人移動至目標物中心位置
        print(myBot.gotoPoint(objCenter, -30, -90, 0, 1000))
        time.sleep(1)
        # 夾取物件
        myBot.closeGripper()
        time.sleep(1)
    
        # 機器人移動至輸送帶位置
        print(myBot.gotoPoint(convyPos, -30, -90, 0, 1500))
        time.sleep(1.5)
        # 機器人移動至稱重點位置
        myBot.gotoPoint((coordinate['blue'][0], coordinate['blue'][1], 12), -90, -90, 0, 1500)
        time.sleep(1.5)
        myBot.gotoPoint((coordinate['blue'][0], coordinate['blue'][1], 3), -90, -90, 0, 1000)
        time.sleep(1)    
        # 打開機器人夾爪
        myBot.openGripper()
        time.sleep(1)
    
         # 讀取Arduino送來的字串
        revNum = 0; 
        try:
            while True:
                data_raw = slFrmArduino.readline() #讀取一行
                cmd = data_raw.decode() # 用UTF-8解碼
                ss= cmd.split()
                print(ss)
                revNum = revNum + 1
                #前幾筆資料丟棄
                if revNum == 5:
                    if abs(int(ss[0]) - objTargetWeigh) < 1:
                        isObjPass = True
                    else:
                        isObjPass = False
                    break
        except KeyboardInterrupt:
            slFrmArduino.close() # 清除串列通訊物件
            print('end of serial communication.')
            break

        # 夾取目標物
        myBot.closeGripper()
        time.sleep(1)
        # 機器人移動至稱重點位置
        myBot.gotoPoint((coordinate['blue'][0], coordinate['blue'][1], 10), -90, -90, 0, 1000)
        time.sleep(1)

        # 機器人移動至置物區位置
        if isObjPass:
            myBot.gotoPoint((coordinate['green'][0], coordinate['green'][1], 10), -90, -90, 0, 1000)
            time.sleep(1)
            myBot.gotoPoint((coordinate['green'][0], coordinate['green'][1], 4), -90, -90, 0, 1000)
            time.sleep(1)
        else:
            myBot.gotoPoint((coordinate['red'][0], coordinate['red'][1], 10), -90, -90, 0, 1000)
            time.sleep(1)
            myBot.gotoPoint((coordinate['red'][0], coordinate['red'][1], 4), -90, -90, 0, 1000)
            time.sleep(1)
        
        # 打開機器人夾爪
        myBot.openGripper()
        time.sleep(1)
   
```