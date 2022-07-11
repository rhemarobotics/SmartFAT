'''
-------------- Finding HSV range of target object. ---------------
Adjust the track bars until only your target object is visible
and the rest is black.
------------------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
import cv2
import numpy as np
import time

# A required callback method that goes into the trackbar function.
def nothing(x):
    pass

# Initializing the webcam feed.
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    # Start reading the webcam feed frame by frame.
    ret, frame = cap.read()
    if not ret:
        break
    # Convert the BGR image to HSV image.
    Lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    l,a,b = cv2.split(Lab)
    print("L, A, B = ", l,a,b)
       
    # If the user presses ESC then exit the program
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release the camera & destroy the windows.
cap.release()
cv2.destroyAllWindows()