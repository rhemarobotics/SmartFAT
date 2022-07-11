'''-------------------------------------------------------
功能:利用ASR語言辨識模組和TTS自然語音播報模組,實現目標物顏色分檢並
    機器人夾取置物控制範例
說明:把目標物放置於相機下方(紅,綠,藍),執行程式,說出目標物的顏色,
    透過語音辨識模組識別聲音,再透過語音播報模組重複一次,機器人進行夾取,
    再回到機器人工作原點後,打開夾爪把目標物置下
執行:sudo python3 VoiceColorSortMoving.py
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
from ASRV3 import *
from TTS import *
from RobotControl import Robot
from package import opencvfunc, Camera
from package.calibration import CalibrationConfig


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 全域變數
stat_IsRunning = False    #機器人是否運動中
stat_Stop = False         #機器人是否停止
stat_Count = 0
stat_T1 = 0
stat_StartPickUp  = False #機器人是否開始抓取目標物
stat_StartCountT1 = True  #開始等待時間計算
stat_CenterList = []      #機器人位置存放區

stat_isAsrReceived = False #ASR是否收到指令
stat_isTtsSpoken = False   #TTS是否重複指令

targ_SetColor = ''         #設定要分檢的顏色
targ_DetColor = 'None'     #偵測到的顏色
targ_RotatAngle = 0        #目標物的旋轉角度  
targ_WorldX, targ_WorldY = 0, 0 #目標物世界座標
targ_LastX, targ_LastY = 0, 0   #目標物上一次世界座標

#建立語音辨識物件
asr = ASR()
#建立語音播報物件
tts = TTS()
# 建立一機器人物件
myBot = Robot()

# 機器人初始化設定
def initRobot():
    
    # 打開機器人夾爪
    myBot.openGripper()
    time.sleep(1)
    # 夾爪旋轉位置重置
    myBot.resetGripper()
    time.sleep(1)
    # 機器人移動至工作點位置
    print(myBot.gotoPoint((0, 15, 15), -30, -90, 0, 500))
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
    global stat_isAsrReceived
    global stat_isTtsSpoken  
    
    targ_SetColor = ()
    targ_DetColor = 'None'
    stat_Stop = False
    stat_Count = 0
    stat_StartPickUp = False
    stat_StartCountT1 = True
    stat_Stop = False
    stat_IsRunning = False    
    stat_CenterList = []
    stat_isAsrReceived = False
    stat_isTtsSpoken = False  

    #ASR基本設定    
    asr.setSensitivity(0x40)
    asr.setVoice(1)
    
    #設置燈號
    asr.setRGB(255, 255, 255)
    time.sleep(1)
    asr.setRGB(0,0,0)

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
    global stat_isAsrReceived
    global stat_isTtsSpoken

    unreachable = False 

    # 顏色方塊置放位置
    coordinate = {
        'red':   (-5, 17, 3),
        'green': (3,  17, 3),
        'blue':  (0,  12, 3)
    }
    
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
                    rollAngle = tf.getAngle(targ_WorldX, targ_WorldY, targ_RotatAngle) #計算夾爪Roll的角度
                    myBot.rollGripper(rollAngle)
                    time.sleep(1)
                    
                    # 機器人運動至目標物中心位置
                    if not stat_IsRunning:
                        continue
                    myBot.gotoPoint((targ_WorldX, targ_WorldY, 9.5), -90, -90, 0, 800)
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
                    
                    # 機器人運行到置物位置
                    if not stat_IsRunning:
                        continue
                    result = myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], 10), -90, -90, 0)
                    time.sleep(result[2]/1000)
                    time.sleep(1)
                    
                    # 把夾爪轉至正確放置角度
                    if not stat_IsRunning:
                        continue                   
                    myBot.resetGripper()
                    time.sleep(1)

                    # 機器人運行到置物的位置
                    if not stat_IsRunning:
                        continue
                    myBot.gotoPoint((coordinate[targ_DetColor][0], coordinate[targ_DetColor][1], coordinate[targ_DetColor][2] + 2),
                                    -90, -90, 0, 500)
                    time.sleep(1)
                    
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
                    
                    # 結束運行程式
                    stat_StartPickUp = False
                    targ_DetColor = 'None'
                    board.setboardRGB('')
                    
                    # 重新新的語音指令
                    stat_isAsrReceived = False
                    stat_isTtsSpoken = False
                    tts.TTSModuleSpeak("[h0][v10][m53]",'執行完畢')
                    time.sleep(2) #延遲時間,等待說話完成                    
        else:
            if stat_Stop:
                stat_Stop = False
                myBot.resetGripper()
                time.sleep(1)
                myBot.gotoPoint((0, 10, 10), -30, -30, -90, 1500)
                time.sleep(1.5)
            time.sleep(0.01)

# 機器人運動執行緒
th = threading.Thread(target=robotPicknPlace)
th.setDaemon(True)
th.start()


## 設置欲辨識目標物色彩
def setTargetColor(target_color):
    global targ_SetColor
    targ_SetColor = target_color
    return True, ()

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
                    # 執行機器人抓取置放執行緒
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
    #機器人狀態機
    init()
    start()
    
    #開啟相機視覺辨識功能    
    my_camera = Camera.Camera()
    my_camera.camera_open()
    
    print('語音辨識程式開啟, 按下ESC鍵關閉程式...')
    print('每句語音指令前,請先加上"開始"')
    print('第一語音指令,"夾取紅色"')
    print('第二語音指令,"夾取綠色"')
    print('第三語音指令,"夾取藍色"')
    print('第四語音指令,"開始"')
    print('第五語音指令,"結束"')
    # 主迴圈
    while True:
        #按下ESC鍵離開
        key = cv2.waitKey(1)
        if key == 27:
            break
        #取得語音辨識結果        
        asrdata = asr.getAsrResult()
        #判斷語音辨識結果
        if asrdata != 0xff:
            if asrdata == 4:
                tts.TTSModuleSpeak("[h0][v10][m53]",'開始')
                time.sleep(1) #延遲時間,等待說話完成
                stat_isAsrReceived = True
            elif asrdata == 1 and stat_isAsrReceived:
                tts.TTSModuleSpeak("[h0][v10][m53]",'夾取紅色')
                time.sleep(2) #延遲時間,等待說話完成
                stat_isTtsSpoken = True
                setTargetColor('red')
            elif asrdata == 2 and stat_isAsrReceived:
                tts.TTSModuleSpeak("[h0][v10][m53]",'夾取綠色')
                time.sleep(2) #延遲時間,等待說話完成
                stat_isTtsSpoken = True
                setTargetColor('green')
            elif asrdata == 3 and stat_isAsrReceived:
                tts.TTSModuleSpeak("[h0][v10][m53]",'夾取藍色')
                time.sleep(2) #延遲時間,等待說話完成
                stat_isTtsSpoken = True
                setTargetColor('blue')
            else:
                tts.TTSModuleSpeak("[h0][v10][m51]",'無法辨識')
                time.sleep(2) #延遲時間,等待說話完成
                tts.TTSModuleSpeak("[h0][v10][m51]",'再說一次')
                time.sleep(2) #延遲時間,等待說話完成
                
        # 當收到並重複完指令後,執行影像顏色與定位辨識
        if stat_isAsrReceived and stat_isTtsSpoken:
            img = my_camera.frame
            if img is not None:
                frame = img.copy()
                Frame = run(frame)
                cv2.imshow('Frame', Frame)
    # end loop
    my_camera.camera_close()
    cv2.destroyAllWindows()

