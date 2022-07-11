'''-------------------------------------------------------
功能:透過視覺校正,計算相機內外參數功能模組
說明:透過openCv執行相機標定與畸變校正並輸出結果至檔案
 步驟1:輸入30張不同角度或距離的相機擷取影像 
 步驟2:透過openCv進行相機內外參數校正計算
 步驟3:計算相機外部參數
 步驟4:計算相機內部參數
 步驟5:結果輸出至檔案 calibration_param.npz
執行:直接執行此檔案程式測試
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import numpy as np
import cv2
import glob
from CalibrationConfig import *

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((calibration_size[1]*calibration_size[0], 3), np.float32)
objp[:, :2] = np.mgrid[0:calibration_size[1], 0:calibration_size[0]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob(save_path + '*.jpg')
found = 0

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (calibration_size[1],calibration_size[0]), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (calibration_size[1],calibration_size[0]), corners2, ret)
        found += 1
        cv2.imshow('img', img)
        cv2.waitKey(1)
    else:
        print('Not find object points:', fname)

print("Number of images used for calibration: ", found)
cv2.destroyAllWindows()

# calibration parameters
# mtx = camera intrinsic matrix
# dist = distortion coefficient matrix [k1 k2 p1 p2 k3]
# rvecs, tvecs = rotation and translation vector
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print('mtx', mtx)
print('dist', dist)

# Reprojection error
total_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    total_error += error

print("total error: ", total_error / len(objpoints))

# save them to a npz file.
np.savez(calibration_param_path, dist_array=dist, mtx_array=mtx, fmt="%d", delimiter=" ")
print('save successful:' + calibration_param_path)

# read the 10th image to test the optimize calibration parameter.
img = cv2.imread(save_path + '10.jpg')
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

cv2.imshow('calibration', dst)
cv2.imshow('original', img)
key = cv2.waitKey(0)
if key != -1:
    cv2.destroyAllWindows()
