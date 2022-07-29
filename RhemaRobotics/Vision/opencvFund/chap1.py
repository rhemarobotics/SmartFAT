'''-------------------------------------------------------
功能:開啟資料夾中圖片
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

# read and show the image.
img = cv2.imread('Resource/lena.png')
cv2.imshow('output',img)
cv2.waitKey(0)
cv2.destroyAllWindows()