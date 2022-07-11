#!/usr/bin/env python3
# encoding:utf-8
import cv2
import sys
sys.path.append('/home/pi/RhemaRobotics/Vision/package/calibration/')
import math
import numpy as np
from CalibrationConfig import *

#手臂原點(雲台中心)到相機畫面中心的距離(cm)
image_x_distance = 15
image_y_distance = 7.2

#相機內外參數.
param_data = np.load(map_param_path + '.npz')

#每個影像像素對應的實際距離.
map_param_ = 0.02025

#把數值作線性轉換(把像素範圍限制在 640,480內)
def leMap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#將影像的像素座標轉換成手臂的座標系.
#傳入影像座標及分辨率, Ex:(100, 100, (640, 480)) = (camx, camy, resolution)
def convertCoordinate(cx, cy, size):
    dx = (cx - size[0]/2) #pixels
    dy = (cy - size[1]/2)
    #Pixel值轉物理長度.
    Wx = round(image_x_distance - round(dy*map_param_, 2),2)
    Wy = round(image_y_distance - round(dx*map_param_, 2),2)
    return Wx, Wy

#取得畫面中物體的ROI區域.
def getROI(box):
    x_min = min(box[0, 0], box[1, 0], box[2, 0], box[3, 0])
    x_max = max(box[0, 0], box[1, 0], box[2, 0], box[3, 0])
    y_min = min(box[0, 1], box[1, 1], box[2, 1], box[3, 1])
    y_max = max(box[0, 1], box[1, 1], box[2, 1], box[3, 1])
    return (x_min, x_max, y_min, y_max)

#計算夾角的旋轉角度
#参数：手臂末端位置座標, 目標物的旋轉角
def getAngle(x, y, angle):
    
    #Base的旋轉角
    theta6 = round(math.degrees(math.atan2(x, y)), 1)
  
    # 若是目標物與機器人的角度趨近0度, 機器人夾爪不用轉
    if (90 - theta6) < 10:
        servo_angle = 500
        return servo_angle
    
    # 其餘角度值
    angle = 90 - theta6 - abs(angle)
    
    if angle > 0:
        angle2 = angle - 70
    else:    
        angle2 = angle + 90
        
    if abs(angle) < abs(angle2):
        servo_angle = int(500 + round(angle * 1000 / 240))
    else:
        servo_angle = int(500 + round(angle2 * 1000 / 240))
    
    return servo_angle