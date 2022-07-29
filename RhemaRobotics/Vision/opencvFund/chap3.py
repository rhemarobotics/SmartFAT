'''-------------------------------------------------------
功能:開啟資料夾中圖片並進行下列影像處理-->大小/裁切
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
print(img.shape)

# resize the image.
imgResize = cv2.resize(img, (300, 200))
print(imgResize.shape)

# crop the image via resize the matrix.
imgCropped = img[0:256, 256:512]

cv2.imshow('original', img)
cv2.imshow('resize', imgResize)
cv2.imshow('Cropped', imgCropped)

cv2.waitKey(0)
cv2.destroyAllWindows()