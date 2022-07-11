'''------------------------------------------
API only for rhema-robotics expansion board
Instruction: sudo python3 Board.py
---------------------------------------------

------------- Board API Lists ---------------
setBusServoID
getBusServoID

setBusServoPulse
getBusServoPulse
restBusServoPulse

setBusServoDeviation
saveBusServoDeviation
getBusServoDeviation

setBusServoAngleLimit
getBusServoAngleLimit

setBusServoVinLimit
getBusServoVinLimit
getBusServoVin

setBusServoMaxTemp
getBusServoTempLimit
getBusServoTemp

unloadBusServo
getBusServoLoadStatus
stopBusServo
-----------------------------------------------'''

#!/usr/bin/env python3
import os
import sys
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import RPi.GPIO as GPIO
from BusServoCmd import *
from smbus2 import SMBus, i2c_msg
from rpi_ws281x import PixelStrip
from rpi_ws281x import Color as PixelColor

##檢查是否為 python3版本
if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

__ADC_BAT_ADDR = 0
__SERVO_ADDR   = 21
__MOTOR_ADDR   = 31
__SERVO_ADDR_CMD  = 40

__motor_speed = [0, 0, 0, 0]
__servo_angle = [0, 0, 0, 0, 0, 0]
__servo_pulse = [0, 0, 0, 0, 0, 0]
__i2c = 1
__i2c_addr = 0x7A

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

##設置板上的RGB燈號腳位
__RGB_COUNT = 2
__RGB_PIN = 12
__RGB_FREQ_HZ = 800000
__RGB_DMA = 10
__RGB_BRIGHTNESS = 120
__RGB_CHANNEL = 0
__RGB_INVERT = False

RGB = PixelStrip(__RGB_COUNT, __RGB_PIN, __RGB_FREQ_HZ, __RGB_DMA, __RGB_INVERT, __RGB_BRIGHTNESS, __RGB_CHANNEL)
RGB.begin()
for i in range(RGB.numPixels()):
    RGB.setPixelColor(i, PixelColor(0,0,0))
    RGB.show()

##設置板上的RGB燈號
def setboardRGB(color):
    if color == "red":
        RGB.setPixelColor(0, PixelColor(255, 0, 0))
        RGB.setPixelColor(1, PixelColor(255, 0, 0))
        RGB.show()
    elif color == "green":
        RGB.setPixelColor(0, PixelColor(0, 255, 0))
        RGB.setPixelColor(1, PixelColor(0, 255, 0))
        RGB.show()
    elif color == "blue":
        RGB.setPixelColor(0, PixelColor(0, 0, 255))
        RGB.setPixelColor(1, PixelColor(0, 0, 255))
        RGB.show()
    elif color == "yellow":
        RGB.setPixelColor(0, PixelColor(255, 255, 0))
        RGB.setPixelColor(1, PixelColor(255, 255, 0))
        RGB.show()
    else:
        RGB.setPixelColor(0, PixelColor(0, 0, 0))
        RGB.setPixelColor(1, PixelColor(0, 0, 0))
        RGB.show()

##讀取電源資訊
def getBattery():
    ret = 0
    with SMBus(__i2c) as bus:
        msg = i2c_msg.write(__i2c_addr, [__ADC_BAT_ADDR,])
        bus.i2c_rdwr(msg)
        read = i2c_msg.read(__i2c_addr, 2)
        bus.i2c_rdwr(read)
        ret = int.from_bytes(bytes(list(read)), 'little')
    return ret

##致能或禁能蜂鳴器 
def setBuzzer(new_state):
    GPIO.setup(31, GPIO.OUT)
    GPIO.output(31, new_state)

##設置蜂鳴器音調時間 
def setBuzzerTimer(seconds):
    setBuzzer(0)
    setBuzzer(1)
    time.sleep(seconds)
    setBuzzer(0)

##設置伺服馬達id值,出廠值預設為1 
def setBusServoID(oldid, newid):
    serial_serro_wirte_cmd(oldid, LOBOT_SERVO_ID_WRITE, newid)

##讀取伺服馬達id值
def getBusServoID(id=None):   
    while True:
        if id is None:  # 串列總線一次只能有一個馬達
            serial_servo_read_cmd(0xfe, LOBOT_SERVO_ID_READ)
        else:
            serial_servo_read_cmd(id, LOBOT_SERVO_ID_READ)
        # 讀取内容
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ID_READ)
        if msg is not None:
            return msg

##設定伺服馬達轉到指定位置值
##use_time: 轉動需要的時間        
def setBusServoPulse(id, pulse, use_time):
    pulse = 0 if pulse < 0 else pulse
    pulse = 1000 if pulse > 1000 else pulse
    use_time = 0 if use_time < 0 else use_time
    use_time = 30000 if use_time > 30000 else use_time
    serial_serro_wirte_cmd(id, LOBOT_SERVO_MOVE_TIME_WRITE, pulse, use_time)

##讀取伺服馬達當前位置值
def getBusServoPulse(id):
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_POS_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_POS_READ)
        if msg is not None:
            return msg

##重置伺服馬達角度偏差值並回到原點位置
def restBusServoPulse(oldid):
    serial_servo_set_deviation(oldid, 0)    # 清除偏差
    time.sleep(0.1)
    serial_serro_wirte_cmd(oldid, LOBOT_SERVO_MOVE_TIME_WRITE, 500, 100)    # 中位

##設置伺服馬達角度偏差值
def setBusServoDeviation(id, d=0):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_ANGLE_OFFSET_ADJUST, d)

##儲存伺服馬達角度偏差值
##斷電保護    
def saveBusServoDeviation(id):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_ANGLE_OFFSET_WRITE)

##讀取伺服馬達角度偏差值
time_out = 50
def getBusServoDeviation(id):
    count = 0
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_ANGLE_OFFSET_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ANGLE_OFFSET_READ)
        count += 1
        if msg is not None:
            return msg
        if count > time_out:
            return None

##設置伺服馬達轉動角度範圍
def setBusServoAngleLimit(id, low, high):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_ANGLE_LIMIT_WRITE, low, high)

##讀取伺服馬達轉動角度範圍
## 返回位元組 0： 低位  1： 高位    
def getBusServoAngleLimit(id):  
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_ANGLE_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ANGLE_LIMIT_READ)
        if msg is not None:
            count = 0
            return msg

##設置伺服馬達電壓範圍
def setBusServoVinLimit(id, low, high):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_VIN_LIMIT_WRITE, low, high)

##讀取伺服馬達電壓值範圍
## 返回位元組 0： 低位  1： 高位     
def getBusServoVinLimit(id):
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_VIN_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_VIN_LIMIT_READ)
        if msg is not None:
            return msg

##讀取伺服馬達電壓值
def getBusServoVin(id):
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_VIN_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_VIN_READ)
        if msg is not None:
            return msg

##設置伺服馬達最高警報溫度
def setBusServoMaxTemp(id, m_temp):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE, m_temp)

##讀取伺服馬達溫度警報範圍
def getBusServoTempLimit(id):  
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        if msg is not None:
            return msg
        
##讀取伺服馬達温度
def getBusServoTemp(id):
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_TEMP_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_TEMP_READ)
        if msg is not None:
            return msg

##禁能伺服馬達
def unloadBusServo(id):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE, 0)

##致能伺服馬達
def loadBusServo(id):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE, 1)

##讀取伺服馬達是否致能
def getBusServoLoadStatus(id):
    while True:
        serial_servo_read_cmd(id, LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        if msg is not None:
            return msg

##停止伺服馬達
def stopBusServo(id=None):
    serial_serro_wirte_cmd(id, LOBOT_SERVO_MOVE_STOP)
