'''-------------------------------------------------------
功能:蜂鳴器控制範例
說明:蜂鳴器會發出長短聲響
執行:sudo python3 BuzzerDemo.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
# 載入擴充板功能函式庫
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import Board as board

if __name__ == '__main__':
    print('按下 Ctrl+C 可中斷程式！')

    board.setBuzzer(0) # 關閉
    board.setBuzzer(1) # 打開
    time.sleep(0.1)    # 延時0.1秒
    board.setBuzzer(0) # 關閉
    time.sleep(1)      # 延時1秒
    board.setBuzzer(1)
    time.sleep(0.5)    # 延時0.5秒
    board.setBuzzer(0)