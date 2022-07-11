'''-------------------------------------------------------
功能:讀取串列式伺服馬達內部參數範例
說明:分別讀取伺服馬達內部位置,溫度,和電壓資訊
執行:sudo python3 BusServoReadStatus.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
# 載入擴充板功能函式庫
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import signal
import Board as board

# 設定要讀取的伺服馬達id
servo_id = 6

# 讀取伺服馬達內部資訊
def getBusServoStatus():
    Pulse = board.getBusServoPulse(servo_id) # 讀取伺服馬達的位置資訊
    Temp = board.getBusServoTemp(servo_id)   # 讀取伺服馬達的温度資訊
    Vin = board.getBusServoVin(servo_id)     # 讀取伺服馬達的電壓資訊
    print('Pulse: {}\nTemp:  {}\nVin:   {}\n'.format(Pulse, Temp, Vin))
    time.sleep(0.5)

# 機器人持續運動到指定位置並讀回目前伺服馬達資訊
while True:   
    board.setBusServoPulse(servo_id, 500, 1000) #伺服馬達轉到角度位置'500'
    time.sleep(1)
    getBusServoStatus()
    board.setBusServoPulse(servo_id, 650, 1000) #伺服馬達轉到角度位置'650'
    time.sleep(1)
    getBusServoStatus()
    board.setBusServoPulse(servo_id, 500, 1000) #伺服馬達轉到角度位置'500'
    time.sleep(1)
    getBusServoStatus()    
    break