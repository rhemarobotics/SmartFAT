'''-------------------------------------------------------
功能:開啟資料夾中圖片並進行下列影像處理-->畫方框/圓圈/文字
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

# empty image
img = np.zeros((512, 512, 3), np.uint8)
print(img.shape)

# convert empty image to colour blue.
#img[:] = 255,0,0

#draw a green line form the original to the image corner.
cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(0,255,0),3)

#draw a rectangle.
cv2.rectangle(img, (0,0), (300,300), (255,0,0), cv2.FILLED)

#draw a circle.
cv2.circle(img, (400,50), 50, (0,0,255), 3)

#put a text.
cv2.putText(img,"OPENCV",(300,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,200,0),2)

cv2.imshow('original', img)
cv2.waitKey(0)
cv2.destroyAllWindows()