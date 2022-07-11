'''-------------------------------------------------------
功能:透過opencv視覺辨識,計算目標物中心相對於世界座標系的位置
說明:放置一方塊位於相機擷取範圍內,進行位置計算
    當按下ESC停止程式
執行:直接執行此檔案程式
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Vision/package/')
sys.path.append('/home/pi/RhemaRobotics/Sdk')
import cv2
import numpy as np
import opencvfunc, Camera
import Transform as tf
from package.calibration import CalibrationConfig


## 全域變數
__target_color = ''           # 設定欲辨識物件的顏色
cam_X, cam_Y = 0, 0           # 物件中心相對於影像座標系的位置
world_X, world_Y = 0, 0       # 物件中心相對於機器人座標系的位置
size = CalibrationConfig.size # 擷取的影像大小
sqrlength = CalibrationConfig.square_length #物件邊長

## 設置欲辨識目標物色彩
def setTargetColor(target_color):
    global __target_color
    __target_color = target_color
    return True, ()

## 計算目標物中心位置的視覺辨識副程式
def run(img):
    
    # 宣告變數
    global cam_X, cam_Y
    global world_X, world_Y
    cam_X, cam_Y, rot = 0, 0, 0
    
    # 在擷取畫面中心位置畫十字線
    opencvfunc.drawCrossLine(img)
    
    # 先對擷取畫面進行基礎影像處理
    img_resize = cv2.resize(img.copy(), size, interpolation=cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    
    # 找到欲辨識目標物色彩
    imgcanny = opencvfunc.filterColour(img_lab, __target_color)
    
    # 找到欲辨識目標物輪廓
    imgproc, cam_X, cam_Y, rot = opencvfunc.getContours(imgcanny, img_resize, cam_X, cam_Y, rot)
    
    # 取得畫面ROI
    if cam_X!=0 and cam_Y!=0:
        # 計算目標物中心位置並把相機座標轉成世界座標
        world_x, world_y = tf.convertCoordinate(cam_X, cam_Y, size)
        rot = round(rot, 2)
        # 繪製文字(目標物X,Y世界座標與旋轉角度)
        cv2.putText(imgproc, '(' + str(world_x) + ', ' + str(world_y) + ', ' + str(rot) +')', (cam_X+10, cam_Y+10),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, opencvfunc.range_rgb['black'], 1)
    else:
        print('找不到目標物')
    return imgproc

# 主程式開始
if __name__ == '__main__':
    
    # 設置欲辨識的顏色
    setTargetColor('red')
    
    # 建立相機物件
    my_camera = Camera.Camera()
    my_camera.camera_open()
    
    # 主迴圈
    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            Frame = run(frame)
            cv2.imshow('Frame', Frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
    # 迴圈結束
    
    # 關閉相機            
    my_camera.camera_close()
    cv2.destroyAllWindows()
