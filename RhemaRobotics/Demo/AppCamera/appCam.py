'''-------------------------------------------------------
功能:實現 Video Streaming 影像串流伺服器
說明:可以透過手機App或是一般網頁, 連至影像串流伺服器即時觀察
    輸入: 0.0.0.0:5001
執行:sudo python3 appCam.py(按下Ctrl+C結束程式)
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import sys
sys.path.append('/home/pi/RhemaRobotics/Vision/')
import time
import cv2
import numpy as np
from package import opencvfunc, Camera
from flask import Flask, render_template, Response, request

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 全域變數
__target_color = ''

# mjpg影像串流伺服器
app = Flask(__name__)
   
# 建立相機物件
myCam = Camera.Camera()

# 影像串流伺服器首頁並取得相關參數
@app.route('/', methods=['GET'])
def index():
    global __target_color
    __target_color = request.args.get('color')
    print(__target_color)
    imgResolution = (myCam.width, myCam.height)
    imgFps = 30
    imgStamp = time.strftime("日期: %D, 時間: %H:%M", time.localtime())    
    return render_template('index.html', imgResolution=imgResolution, imgFps=imgFps,imgStamp=imgStamp)
           
@app.route('/video_feed')
def video_feed():
    # 自動導向至影像更新
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

## 本地相機擷取畫面並分辨顏色執行緒
def gen():
    # 打開相機,開始進行影像擷取
    if not myCam.opened:
        myCam.camera_open()
        print('本地相機開啟,準備影像串流...')        
    while True:
        img = myCam.frame
        if img is not None:
            newImg = run(img)
            ret, buffer = cv2.imencode('.jpg', newImg)
            #更新影像
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

## 分辨顏色的視覺辨識副程式
def run(img):
    global __target_color
    # 宣告變數
    cx = cy = rot = 0
    size = (640, 480)  
    # 在擷取畫面中心位置畫十字線
    opencvfunc.drawCrossLine(img)
    # 先對擷取畫面進行基礎影像處理
    img_resize = cv2.resize(img.copy(), size, interpolation=cv2.INTER_NEAREST)
    img_gb = cv2.GaussianBlur(img_resize, (11, 11), 11)
    img_lab = cv2.cvtColor(img_gb, cv2.COLOR_BGR2LAB)
    if __target_color is not None:
        # 找到欲辨識目標物色彩
        imgcanny = opencvfunc.filterColour(img_lab, __target_color)
        # 找到欲辨識目標物輪廓
        imgproc, cx, cy, rot = opencvfunc.getContours(imgcanny, img_resize, cx, cy, rot)
        # 取得畫面ROI
        if cx!=0 and cy!=0:
            # 繪製文字
            cv2.putText(imgproc, '(' + __target_color + ')', (cx+10, cy+10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, opencvfunc.range_rgb['green'], 1)       
            return imgproc
    else:
        return img  

# 開啟mjpg影像串流伺服器服務
if __name__ == '__main__':
    # 0.0.0.0可以改成自訂ip位置
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)