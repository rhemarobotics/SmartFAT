'''-------------------------------------------------------
功能:透過opencv辨識標準棋盤格,計算影像像素相對於物理世界的實際長度值
例如:pixels_per_centimeter = object_width / know_width
說明:放置一方塊位於相機擷取範圍內,進行位置計算並按下ESC停止程式
執行:直接執行此檔案程式
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import cv2
import time
import numpy as np
from CalibrationConfig import *

# import calibration parameters.
param_data = np.load(calibration_param_path + '.npz')
mtx = param_data['mtx_array']
dist = param_data['dist_array']

# camera captured chessboard image in the conveyor.
cony_chessbrd_h = 3
cony_chessbrd_w = 5

# capture one frame.
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        h, w = frame.shape[:2]
        break

# undistort
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    ret, Frame = cap.read()
    if ret:
        frame = Frame.copy()
        dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        img = dst.copy()

        # draw a red cross line in the middle of frame.
        cv2.line(dst, (0, int(h / 2)), (w, int(h / 2)), (0, 0, 255), 2)
        cv2.line(dst, (int(w / 2), 0), (int(w / 2), h), (0, 0, 255), 2)        
        cv2.imshow('dst', dst)

        # press 'SPACE' to capture one frame.
        key = cv2.waitKey(1)
        if key == 32:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret_, corners = cv2.findChessboardCorners(gray, (cony_chessbrd_h, cony_chessbrd_w), None)
            print(ret_)
            if ret_:
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                sum_ = []
                last_i = [0]
                count = 0
                for i in corners2:
                    count += 1
                    if count != 1 and (count - 1)%7 != 0:
                        a_ = (last_i[0] - i[0])**2    
                        sum_.append(np.sqrt(np.sum(a_)))
                    last_i = i
                
                map_param = np.mean(sum_)
                # Adjacent pixel length convert to the physical corners length.
                map_param = corners_length/map_param 
                np.savez(map_param_path, map_param = map_param, fmd='%d', delimiter=' ')
                print('save successful')
                print(map_param)
        if key == 27:
            break
    else:
        time.sleep(0.01)

# close camera
cap.release()
cv2.destroyAllWindows()
