'''-------------------------------------------------------
功能:透過opencv實現目標物輪廓的視覺辨識
說明:放置一方塊位於相機擷取範圍內,進行輪廓辨識
    當按下ESC停止程式
執行:直接執行此檔案程式
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
import cv2
import numpy as np
from package import opencvfunc, Camera


__target_color = ''
draw_color = opencvfunc.range_rgb["black"]

## 設置欲辨識目標物色彩
def setTargetColor(target_color):
    global __target_color
    __target_color = target_color
    return True, ()

## 分辨輪廓的視覺辨識副程式
def run(img):
    
    # 宣告變數
    cx = cy = rot = 0
    
    # 在擷取畫面中心位置畫十字線
    opencvfunc.drawCrossLine(img)
    
    # 先對擷取畫面進行基礎影像處理
    img_resize = cv2.resize(img.copy(), (640, 480), interpolation = cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    
    # 找到欲辨識目標物色彩
    imgcanny = opencvfunc.filterColour(img_lab, __target_color)
    
    # 找到欲辨識目標物輪廓
    imgproc, cx, cy, rot = opencvfunc.getContours(imgcanny, img_resize, cx, cy, rot)
    return imgproc

# 主程式開始
if __name__ == '__main__':
    
    #設置欲辨識目標物的顏色
    setTargetColor('red')
    
    #宣告相機物件
    my_camera = Camera.Camera()
    
    #開啟相機
    my_camera.camera_open()

    while True:
        #擷取一張影像
        img = my_camera.frame
        if img is not None:
            #複製影像
            frame = img.copy()
            #影像處理
            Frame = run(frame)
            #顯示影像處理結果
            cv2.imshow('Frame', Frame)
            #若偵測到ESC鍵,跳出迴圈
            key = cv2.waitKey(1)
            if key == 27:
                break
    #關閉相機
    my_camera.camera_close()
    cv2.destroyAllWindows()
