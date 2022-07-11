'''-------------------------------------------------------
功能:透過opencv實現目標物顏色的視覺辨識
說明:放置一方塊,位於相機擷取範圍內,進行顏色辨識
    當按下ESC鍵停止程式
執行:直接執行此檔案程式
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
import cv2
import numpy as np
from package import opencvfunc, Camera

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

__target_color = ''

## 設置欲辨識目標物色彩
def setTargetColor(target_color):
    global __target_color
    __target_color = target_color
    return True, ()

## 分辨顏色的視覺辨識副程式
def run(img):
    
    # 宣告變數
    cx = cy = rot = 0
    size = (640, 480)
    
    # 在擷取畫面中心位置畫十字線
    opencvfunc.drawCrossLine(img)
    
    # 先對擷取畫面進行基礎影像處理
    img_resize = cv2.resize(img.copy(), size, interpolation=cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    
    # 找到欲辨識目標物色彩
    imgcanny = opencvfunc.filterColour(img_lab, __target_color)
    
    # 找到欲辨識目標物輪廓
    imgproc, cx, cy, rot = opencvfunc.getContours(imgcanny, img_resize, cx, cy, rot)
    
    # 取得畫面ROI
    if cx!=0 and cy!=0:
        # 繪製文字
        cv2.putText(imgproc, '(' + __target_color + ')', (cx+10, cy+10),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, opencvfunc.range_rgb['green'], 1)       
    else:
        print('找不到目標物')
    return imgproc

# 主程式開始
if __name__ == '__main__':
    
    # 設置欲辨識的顏色
    setTargetColor('blue')
    
    # 建立相機物件
    my_camera = Camera.Camera()
    # 開啟相機
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
