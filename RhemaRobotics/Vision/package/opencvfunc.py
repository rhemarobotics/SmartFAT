'''-------------------------------------------------------
功能:影像處理功能模組
說明:執行影像處理和識別的功能
執行:作為程式功能模組使用
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
import math
import cv2
import numpy as np

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

#LAB color space
color_range = {
    'red'  : [(0, 151, 100), (255, 255, 255)],    # lower,higher
    'green': [(0, 0, 0), (255, 115, 255)], 
    'blue' : [(0, 0, 0), (255, 145, 120)],
    'black': [(0, 0, 0), (56, 255, 255)], 
    'white': [(193, 0, 0), (255, 250, 255)], 
}

range_rgb = {
    'red'  : (0, 0, 255),
    'blue' : (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

# find the target colour in the color_range.
def filterColour(imglab, colour):
    for i in color_range:
        if i in colour:
            mask = cv2.inRange(imglab, color_range[i][0], color_range[i][1]) # morphology processing.
            opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))  # open calc.
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6, 6), np.uint8))  # close calc.
    return closed

# calculate contours via area.
def getContours(imgcanny, imgorg, cx, cy, rot):
    contours = cv2.findContours(imgcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    for cnt in contours:
        area = math.fabs(cv2.contourArea(cnt))  # Contour Area
        if area > 3000:
            peri = cv2.arcLength(cnt, True)  # Contour Perimeter
            approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)  # Contour Approximation
            objCor = len(approx)
            # object classification.
            if objCor == 3:     objectType = "Tri"
            elif objCor == 4:   objectType = "Square"
            elif objCor > 4:    objectType = "Circle"
            else:               objectType = "None"
            # bounding rectangle
            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            # draw Contours with blue color.
            cv2.drawContours(imgorg, [box], 0, (255, 0, 0), 2)
            # draw the center point.
            M = cv2.moments(box)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(imgorg, (cx, cy), 7, (255, 255, 255), -1)
            # draw text with white color.
            x, y, w, h = cv2.boundingRect(approx)
            cv2.putText(imgorg, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)
            rot = round(rect[2],2)
    return imgorg, cx, cy, rot

# draw a cross line(red) in the middle of the image.
def drawCrossLine(img):
    img_h, img_w = img.shape[:2]
    cv2.line(img, (0, int(img_h / 2)), (img_w, int(img_h / 2)), (0, 0, 200), 1)
    cv2.line(img, (int(img_w / 2), 0), (int(img_w / 2), img_h), (0, 0, 200), 1)


