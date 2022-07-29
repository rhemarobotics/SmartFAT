'''-------------------------------------------------------
功能:讀取串列式伺服馬達內部參數範例
說明:分別讀取伺服馬達內部位置,溫度,和電壓資訊
執行:sudo python3 ReadServoStatus.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import signal
import Board as board


##讀取伺服馬達內部資訊
def getBusServoStatus(id):
    Pulse = board.getBusServoPulse(id) # 讀取伺服馬達的位置資訊
    Temp = board.getBusServoTemp(id)   # 讀取伺服馬達的温度資訊
    Vin = board.getBusServoVin(id)     # 讀取伺服馬達的電壓資訊
    print('Pulse:{}, Temp:{}, Vin:{}, '.format(Pulse, Temp, Vin))
    time.sleep(0.5)

if __name__ == "__main__":
    getBusServoStatus(int(sys.argv[1]))
