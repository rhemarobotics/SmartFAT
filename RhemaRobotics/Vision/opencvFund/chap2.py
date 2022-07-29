'''-------------------------------------------------------
功能:開啟資料夾中圖片並進行下列影像處理-->灰階/模糊/輪廓/侵蝕/膨脹
說明:
執行:直接執行此檔案程式
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Vision/opencvFund/')
import cv2
import numpy as np


img = cv2.imread('Resource/lena.png')
kernel = np.ones((5,5), np.uint8)

# convert the image to gray colour.
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Image smoothing and blurring
# Averaging：cv2.blur or cv2.boxFilter
# Gaussian Filtering：cv2.GaussianBlur
# Median Filtering：cv2.medianBlur
# Bilateral Filtering：cv2.bilateralFilter
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)

# Canny edge detector algorithm.
imgCanny = cv2.Canny(imgGray, 70, 210, 3)

# image dilate
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)

# image erode
imgErode = cv2.erode(imgDialation, kernel, iterations=1)

cv2.imshow('gray', imgGray)
cv2.imshow('blur', imgBlur)
cv2.imshow('canny', imgCanny)
cv2.imshow('dilate', imgDialation)
cv2.imshow('erode', imgErode)

cv2.waitKey(0)
cv2.destroyAllWindows()
