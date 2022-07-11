'''-------------------------------------------------------
功能:語音合成輸出範例
說明:輸入單字或完整語句,透過TTS模組,即可輸出合成聲音
    [h0]設置單字發音方式，0為自動判斷單字發音方式，1為字母發音方式，2為單字發音方式
    [v10]設置音量，音量範圍為0-10,10為最大音量
    [m53]選擇聲音，3是女聲1，51是男聲1，52是男聲2，53是女聲2
    注意括號里的單字長度不能超過32,如果超過了請分多次來說
執行:直接執行範例程式
----------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
from TTS import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

if __name__ == '__main__':
    tts = TTS()
    tts.TTSModuleSpeak("[h0][v10][m53]","robotics")
    time.sleep(2) #延遲時間,等待說話完成
    tts.TTSModuleSpeak("[h0][v10][m53]",'雷瑪機器人')
    time.sleep(2) #延遲時間,等待說話完成