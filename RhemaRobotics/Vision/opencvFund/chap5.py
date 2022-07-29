'''-------------------------------------------------------
功能:開啟資料夾中圖片並進行下列影像處理-->仿射變換
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

img = cv2.imread('Resource/cards.png')
wid, hgt = 400, 500
pts1 = np.float32([[591,1],[1327,192],[4,937],[971,1247]])
pts2 = np.float32([[0,0],[wid,0],[0,hgt],[wid,hgt]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOut = cv2.warpPerspective(img, matrix,(wid,hgt))

cv2.imshow('original', img)
cv2.imshow('warp', imgOut)

cv2.waitKey(0)
cv2.destroyAllWindows()