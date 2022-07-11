'''-------------------------------------------------------
功能:Arduino與樹梅派機器人協同作業(物件堆棧範例)
說明:把物件放置於輸送帶上,傳至定點位置後,停止輸送帶,透過序列埠通知
    樹梅派機器人,夾取物件並放置於對應位置.
執行:sudo python3 SmartFactoryEx1.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import sys
sys.path.append('/home/pi/RhemaRobotics/Robot/')
import time
import serial
from RobotControl import Robot

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 建立一機器人物件
myBot = Robot()

# 設定與Arduino通訊的埠口
port = "/dev/ttyUSB0"

# 夾取物件數目
objNumber = 0

# 機器人工作座標
convyPos = (15, 0, 15)
workPos = (0, 15, 15)
placePos = ((0, 18, 3),(0, 19.3, 8),(0, 18.5, 11))
objCenter = (15, 0, 11)


# 主程式開始
if __name__ == '__main__':
    
    # 是否接收到Arduino的通知
    isRevSerialCmd = False
    
    # 樹梅派串列埠口通訊設置
    print('串列通訊埠口開啟, 格式: 9600,8,N,1')
    slFrmArduino = serial.Serial(port, 9600)
    slFrmArduino.flushInput()

    # 主程式開始
    while objNumber<3:  
        print('機器人堆棧程式開始...')
        # 打開機器人夾爪
        myBot.openGripper()
        time.sleep(1)
        # 機器人移動至工作點位置
        print(myBot.gotoPoint(workPos, -30, -90, 0, 500))
        time.sleep(0.5)

        # 讀取Arduino送來的字串
        try:
            while True:
                data_raw = slFrmArduino.readline() #讀取一行
                cmd = data_raw.decode() # 用UTF-8解碼
                ss= cmd.split()
                if ss[0] == 'ready':
                    time.sleep(0.5)
                    break
        except KeyboardInterrupt:
            slFrmArduino.close() # 清除串列通訊物件
            print('end of serial communication.')
            
        print('機器人移動至輸送帶位置')        
        # 機器人移動至輸送帶位置
        print(myBot.gotoPoint(convyPos, -30, -90, 0, 500))
        time.sleep(0.5)
        # 機器人移動至目標物中心位置
        print(myBot.gotoPoint(objCenter, -30, -90, 0, 1000))
        time.sleep(1)
        # 夾取物件
        myBot.closeGripper()
        time.sleep(1)
        # 機器人移動至輸送帶位置
        print(myBot.gotoPoint(convyPos, -30, -90, 0, 1000))
        time.sleep(1)
        # 機器人移動至工作點位置
        print(myBot.gotoPoint(workPos, -30, -90, 0, 1000))
        time.sleep(1)        
        # 機器人移動至工作點位置
        print(myBot.gotoPoint(placePos[objNumber], -90, -90, 0, 2000))
        time.sleep(2)
        # 打開機器人夾爪
        myBot.openGripper()
        time.sleep(1)
        # 紀錄夾取物件
        objNumber = objNumber + 1
        
    # 機器人堆棧程式結束           
    print('機器人堆棧程式結束...')
    