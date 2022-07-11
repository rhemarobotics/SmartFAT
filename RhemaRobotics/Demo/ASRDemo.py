'''-------------------------------------------------------
功能:自然語音辨識範例
說明:開始時,先錄製幾句自然語音並存在模組的記憶體區,
    因為python的編譯過程不支援中文,所以程式碼內的中文語句用漢語拼音代替,
    設置好,即可開始測試,辨識成功則燈號會改變顏色
執行:sudo python3 ASRDemo.py
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import signal
import Board as board
from ASRV3 import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

start = True
def Stop(signum, frame):
    global start
    start = False
    print('關閉中...')
    

if __name__ == "__main__":
    print('按下鍵盤Ctrl+C,觸發Stop副程式...')
    
    #關閉板上的RGB燈號
    board.setboardRGB('')
    
    #設置鍵盤中斷訊號至Stop副程式
    signal.signal(signal.SIGINT, Stop)
    
    #建立物件
    asr = ASR()
    checkNum = 0
    
    #新增的字彙和識別模式支援斷電保存，第一次設置完成後，可以将1改为0
    if 1:
        print('新增的字彙和識別模式')
        asr.eraseWords()
        asr.setMode(0)
        asr.addWords(1, 'jia qu hong se')#夾取紅色
        asr.addWords(2, 'jia qu lv se')  #夾取綠色
        asr.addWords(3, 'jia qu lan se') #夾取藍色
        asr.addWords(4, 'kai shi')       #開始
        asr.addWords(5, 'jie shu')       #結束

        #驗證
        checkNum = asr.checkWordNum()
        print(checkNum)
        if checkNum != 5:
            start = False
        else:            
            asr.setBuzzer(1) #蜂鳴器on
            time.sleep(1)
            asr.setBuzzer(0) #蜂鳴器off

    #基本設定    
    asr.setSensitivity(0x40)
    asr.setVoice(1)
    
    #設置燈號
    asr.setRGB(255,255,255)
    time.sleep(1)
    asr.setRGB(0,0,0)
    
    while 1:
        #顯示語音辨識結果
        print('顯示語音辨識結果...')
        data = asr.getAsrResult()
        if data != 0xff:
            print("result:", data)
        time.sleep(0.5)
            
        #如果按下[ESC+C]中斷程式
        if not start:           
            board.setboardRGB('')
            time.sleep(1)
            print('已關閉')
            break
            