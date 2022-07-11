'''-------------------------------------------------------
功能:相機功能模組
說明:執行相機基本的功能
執行:直接執行此檔案程式測試或作為程式模組使用
----------------------------------------------------------
'''

#!/usr/bin/env python3 
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Vision/package/calibration/')
import cv2
import time
import threading
import numpy as np
from CalibrationConfig import * 

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

## 定義相機類別
class Camera:
    # 初始化相機
    def __init__(self, resolution=(640, 480)):
        self.cap = None
        self.width = resolution[0]
        self.height = resolution[1]
        self.frame = None
        self.opened = False
        
        # 載入相機內部校正的參數
        self.param_data = np.load(calibration_param_path + '.npz')
        self.mtx = self.param_data['mtx_array']
        self.dist = self.param_data['dist_array']
        
        # 最佳化相機
        self.newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.width, self.height), 0,
                                                               (self.width, self.height))
        # 影像不失真
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, self.newcameramtx,
                                                           (self.width, self.height), 5)
        # 建立一執行緒
        self.th = threading.Thread(target=self.camera_task, args=(), daemon=True)
        self.th.start()

    # 開啟相機
    def camera_open(self):
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_SATURATION, 40)
            self.opened = True
            print('open camera successfully.')
        except Exception as e:
            print('Fail to open camera:', e)

    # 關閉相機
    def camera_close(self):
        try:
            self.opened = False
            time.sleep(0.2)
            if self.cap is not None:
                self.cap.release()
                time.sleep(0.05)
                print('close camera successfully.')
            self.cap = None
        except Exception as e:
            print('Fail to close camera:', e)

    # 影像擷取執行緒
    def camera_task(self):
        while True:
            try:
                if self.opened and self.cap.isOpened():
                    ret, frame_tmp = self.cap.read()
                    if ret:
                        frame_resize = cv2.resize(frame_tmp, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
                        self.frame = cv2.remap(frame_resize, self.mapx, self.mapy, cv2.INTER_LINEAR)
                        # print('renew frame')
                    else:
                        print(0xff)
                        self.frame = None
                        cap = cv2.VideoCapture(0)
                        ret, _ = cap.read()
                        if ret:
                            self.cap = cap
                elif self.opened:
                    print(0xfe)
                    cap = cv2.VideoCapture(0)
                    ret, _ = cap.read()
                    if ret:
                        self.cap = cap
                else:
                    time.sleep(0.01)
            except Exception as e:
                print('Fail to capture image from the camera:', e)
                time.sleep(0.01)

## 測試相機擷取功能並按下'ESC'離開程式
if __name__ == '__main__':
    my_camera = Camera()
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            cv2.imshow('img', img)
            key = cv2.waitKey(1)
            if key == 27:
                break
    my_camera.camera_close()
    cv2.destroyAllWindows()
