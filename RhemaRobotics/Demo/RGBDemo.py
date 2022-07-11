'''-------------------------------------------------------
功能:RGB燈控制範例
說明:當按下鍵盤 Ctrl+C時,會觸發Stop副程式, 結束時燈號全滅;
    反之,則亮最後的黃燈
執行:sudo python3 RGBDemo.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import signal
import Board as board

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

start = True
def Stop(signum, frame):
    global start
    start = False
    print('關閉中...')

# 主程式開始
if __name__ == '__main__':
    print('按下鍵盤Ctrl+C,觸發Stop副程式...')

    #關閉板上的RGB燈號
    board.setboardRGB('')
    
    #設置鍵盤中斷訊號至Stop副程式
    signal.signal(signal.SIGINT, Stop)

    #主程式迴圈
    while True:
        #設置兩個燈為紅色,亮1秒
        board.setboardRGB('red')    
        time.sleep(1)   
        #設置兩個燈為綠色
        board.setboardRGB('green')    
        time.sleep(1)
        #設置兩個燈為藍色
        board.setboardRGB('blue')    
        time.sleep(1)
        #設置兩個燈為黃色
        board.setboardRGB('yellow')
        time.sleep(1)
        #將所有的燈關閉
        if not start:           
            board.setboardRGB('')
            time.sleep(1)
            print('已關閉')
        break
