'''-------------------------------------------------------
功能:Arduino與樹梅派機器人協同作業(物件顏色分類範例,目前指針對紅色方塊)
    透過視覺辨識與定位,實現目標物顏色分類並機器人夾取置物
說明:把目標物置於輸送帶上,待超音波偵測到物件後,輸送帶停止,隨即執行物件顏色
    辨識與空間位置定位,通知機器人夾取目標物並放置於特定的顏色位置
執行:sudo python3 SmartFactoryEx2.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import sys
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
import serial
from RobotControl import Robot
from package import opencvfunc, Camera

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 全域變數
stat_IsRunning = False          #機器人是否運動中
stat_Stop = False               #機器人是否停止
stat_Count = 0
stat_T1 = 0
stat_StartPickUp  = False       #機器人是否開始抓取目標物
stat_StartCountT1 = True        #開始等待時間計算
stat_CenterList = []            #機器人位置存放區
stat_NotifyFrmArduino = False   #接收到Arduino的通知

targ_SetColor = ''              #設定要分檢的顏色
targ_DetColor = 'None'          #偵測到的顏色
targ_RotatAngle = 0             #目標物的旋轉角度  
targ_WorldX, targ_WorldY = 0, 0 #目標物世界座標
targ_LastX, targ_LastY = 0, 0   #目標物上一次世界座標


## 設置欲辨識目標物色彩
def setTargetColor(target_color):
    global targ_SetColor
    targ_SetColor = target_color
    return True, ()

# 設定與Arduino通訊的埠口
port = "/dev/ttyUSB0"

# 建立一機器人物件
myBot = Robot()

# 機器人工作座標
convyPos = (15, 0, 15)
workPos = (0, 15, 15)
stopPos = (0, 10, 10)
placePos = ((0, 20, 3),(0, 20, 6),(0, 20, 9))
objCenter = (16, 0, 10)

# 顏色方塊置放位置
coordinate = {'red':   (-5, 18, 4),
              'green': (3,  18, 4),
              'blue':  (0,  14, 4) }

# 機器人初始化設定
def initRobot():
    # 打開機器人夾爪
    myBot.openGripper()
    time.sleep(1)
    # 夾爪旋轉位置重置
    myBot.resetGripper()
    time.sleep(1)
    # 機器人移動至工作點位置
    print(myBot.gotoPoint(workPos, -30, -90, 0, 500))
    time.sleep(0.5)

# 狀態機
def reset():
    global targ_SetColor
    global targ_DetColor    
    global stat_Stop  
    global stat_Count
    global stat_StartPickUp
    global stat_StartCountT1
    global stat_Stop
    global stat_IsRunning
    global stat_CenterList
    global stat_NotifyFrmArduino
    
    targ_SetColor = ()
    targ_DetColor = 'None'
    stat_Stop = False
    stat_Count = 0
    stat_StartPickUp = False
    stat_StartCountT1 = True
    stat_Stop = False
    stat_IsRunning = False
    stat_NotifyFrmArduino = False
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
    global stat_Stop
    global stat_IsRunning
    stat_Stop = True
    stat_IsRunning = False
    print("機器人顏色分檢程式結束")

def exit():
    global stat_Stop
    global stat_IsRunning
    stat_Stop = True
    stat_IsRunning = False
    print("機器人顏色分檢程式")

## 機器人夾取與放置目標物動作程序
def robotPicknPlace():
    global stat_Stop
    global stat_IsRunning
    global stat_StartPickUp    
    global targ_DetColor
    global targ_RotatAngle
    global targ_WorldX, targ_WorldY
    global stat_NotifyFrmArduino
    unreachable = False 
   
    while True:
        if stat_IsRunning:
            if targ_DetColor != 'None' and stat_StartPickUp:
                myBot.openGripper()
                time.sleep(1)
                #設置板上燈號與目標物顏色相同
                board.setboardRGB(targ_DetColor)
                time.sleep(0.1)
                board.setboardRGB('')
                #移到目標位置上方(高度設為12cm), 計算此位置是否可以到達,如果不行則返回false
                result = myBot.gotoPoint((targ_WorldX, targ_WorldY, 12), -90, -90, 0)  
                if result == False:
                    unreachable = True
                    print('目標物無法到達...')
                else:
                    unreachable = False
                    time.sleep(result[2]/1000) #計算機器人運動時間
                    board.setBuzzerTimer(0.1)

                    # 打開夾爪並將夾爪轉至正確抓取角度
                    if not stat_IsRunning:
                        continue
                    # 計算夾爪Roll的角度
                    rollAngle = tf.getAngle(targ_WorldX, targ_WorldY, targ_RotatAngle) 
                    myBot.rollGripper(rollAngle)
                    time.sleep(1)
                    
                    # 機器人運動至目標物中心位置
                    if not stat_IsRunning:
                        continue
                    myBot.gotoPoint((targ_WorldX, targ_WorldY, 9), -90, -90, 0, 800)
                    time.sleep(0.8)

                    # 夾爪關閉
                    if not stat_IsRunning:
                        continue
                    myBot.closeGripper()
                    time.sleep(1)

                    # 抬起目標物
                    if not stat_IsRunning:
                        continue
                    myBot.gotoPoint((targ_WorldX, targ_WorldY, 12), -90, -90, 0, 800)
                    time.sleep(0.8)
                    
                     # 回到工作位置
                    if not stat_IsRunning:
                        continue
                    myBot.gotoPoint(workPos, -90, -90, 0, 1500)
                    time.sleep(1.5)                   
                    
                    # 機器人運行到置物位置
                    if not stat_IsRunning:
                        continue
                    result = myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], 10), -90, -90, 0, 1500)
                    time.sleep(1.5)
                    
                    # 把夾爪轉至正確放置角度
                    if not stat_IsRunning:
                        continue                   
                    myBot.resetGripper()
                    time.sleep(1)

                    # 機器人運行到置物的位置
                    if not stat_IsRunning:
                        continue
                    myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], coordinate[targ_DetColor][2]),
                                    -90, -90, 0, 800)
                    time.sleep(0.8)
                    
                    # 打開夾爪
                    if not stat_IsRunning:
                        continue
                    myBot.openGripper()
                    time.sleep(1)

                    # 抬起夾爪
                    if not stat_IsRunning:
                        continue
                    myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], 12), -90, -90, 0, 800)
                    time.sleep(0.8)

                    # 回到機器人初始工作位置
                    initRobot()  
                    time.sleep(1.5)
                    
                    # 處理完通知事件並結束運行程式
                    stat_NotifyFrmArduino = False
                    stat_StartPickUp = False
                    targ_DetColor = 'None'
                    board.setboardRGB('')
        else:
            if stat_Stop:
                stat_Stop = False
                myBot.resetGripper()
                time.sleep(1)
                myBot.gotoPoint(stopPos, -30, -30, -90, 1500)
                time.sleep(1.5)
            time.sleep(0.01)

# 建立一獨立的機器人運動執行緒
th = threading.Thread(target=robotPicknPlace)
th.setDaemon(True)
th.start()    


## 計算目標物中心位置的視覺辨識副程式
def run(img):
    global stat_IsRunning
    global stat_StartPickUp
    global targ_SetColor
    global targ_DetColor
    global targ_RotatAngle
    global targ_LastX, targ_LastY
    global targ_WorldX, targ_WorldY
    global stat_Count
    global stat_StartCountT1, stat_T1
    global stat_CenterList
        
    size = (640, 480)
    # 目標物相對於世界座標的中心位置
    cam_X, cam_Y = 0, 0

    # 在擷取畫面中心位置畫十字線
    opencvfunc.drawCrossLine(img)
    # 先對擷取畫面進行基礎影像處理
    img_resize = cv2.resize(img.copy(), size, interpolation=cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    # 如果機器人尚未開始運動
    if not stat_StartPickUp:
        # 找到欲辨識目標物色彩
        imgcanny = opencvfunc.filterColour(img_lab, targ_SetColor)
        # 找到欲辨識目標物輪廓
        imgproc, cam_X, cam_Y, targ_RotatAngle = opencvfunc.getContours(imgcanny, img_resize, cam_X, cam_Y, targ_RotatAngle)
        # # 計算目標物中心位置並把相機座標轉成世界座標
        if cam_X!=0 and cam_Y!=0:           
            targ_WorldX, targ_WorldY = tf.convertCoordinate(cam_X, cam_Y, size)
            # 繪製目標物世界座標與旋轉角度
            cv2.putText(imgproc, '(' + str(targ_WorldX) + ', ' + str(targ_WorldY) + ', ' + str(targ_RotatAngle) + ')',
                        (cam_X+10, cam_Y+10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, opencvfunc.range_rgb['green'], 1)
            # 繪製目標物顏色
            targ_DetColor = targ_SetColor
            cv2.putText(imgproc, "Color: " + targ_DetColor, (cam_X-10, cam_Y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                opencvfunc.range_rgb["black"], 2)
            # 比較前後的座標,是否需要移動
            distance = math.sqrt(pow(targ_WorldX - targ_LastX, 2) + pow(targ_WorldY - targ_LastY, 2))
            targ_LastX, targ_LastY = targ_WorldX, targ_WorldY
            # 移動距離累加器
            if distance < 0.5:
                # 新增一筆機器人位置
                stat_CenterList.extend((targ_WorldX, targ_WorldY))
                stat_Count += 1
                if stat_StartCountT1:
                    stat_StartCountT1 = False
                    stat_T1 = time.time()
                if time.time() - stat_T1 > 1.0:
                    stat_StartCountT1 = True
                    # 抓出最後一筆機器人位置
                    targ_WorldX, targ_WorldY = np.mean(np.array(stat_CenterList).reshape(stat_Count, 2), axis=0)
                    stat_Count = 0
                    stat_CenterList = []
                    stat_StartPickUp = True
            else:
                stat_T1 = time.time()
                stat_StartCountT1 = True
                stat_CenterList = []
                stat_Count = 0
            return imgproc        
        else:
            print('找不到目標物')
    return img            


# 主程式開始,按下ESC鍵離開
if __name__ == '__main__':   
    print('主程式開始,按下ESC鍵離開...')

    # 樹梅派串列埠口通訊設置
    print('串列通訊埠口開啟, 格式: 9600,8,N,1')
    slFrmArduino = serial.Serial(port, 9600)
    
    # 機器人狀態機
    init()
    start()
    
    # 開啟相機
    setTargetColor('red')
    my_camera = Camera.Camera()
    my_camera.camera_open()
    
    # 主程式  
    while True:
        # 讀取Arduino送來的字串
        try:
            while not stat_NotifyFrmArduino:
                data_raw = slFrmArduino.readline() #讀取一行
                cmd = data_raw.decode() # 用UTF-8解碼
                ss= cmd.split()
                if ss[0] == 'ready':
                    print('接收到Arduino通知')
                    stat_NotifyFrmArduino = True
                    time.sleep(0.5)
                    break
        except KeyboardInterrupt:
            # 接收到[Ctrl+C],中斷主程式
            my_camera.camera_close() # 清除相機物件
            cv2.destroyAllWindows()            
            slFrmArduino.close() # 清除串列通訊物件
            print('end of serial communication.')

        # 收到通知, 執行視覺辨識功能
        while stat_NotifyFrmArduino:
            img = my_camera.frame
            if img is not None:
                frame = img.copy()
                Frame = run(frame)
                cv2.imshow('Frame', Frame)
