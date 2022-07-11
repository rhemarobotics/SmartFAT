'''-------------------------------------------------
    RPi Automatic-Speech-Recognition(ASR)
----------------------------------------------------
'''
#!/usr/bin/env python3
# coding=utf8
import sys
import smbus
import time
import numpy

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class ASR:

    address = 0x0f           #ASR模組I2C地址
    bus = None  
    
    ASR_ADD_WORD_ADDR = 0x01 #字彙添加地址
    ASR_MODE_ADDR = 0x02     #識別模式設置地址，0:循環識別 1:口令模式 ,2:按键模式，預設為0
    ASR_RGB_ADDR = 0x03      #RGB燈號設置地址,第一個為燈號 1：蓝 2:红 3：绿,
                             #第二個為亮度0-255，数值越大亮度越高
    ASR_SENS_ADDR = 0x04     #識別靈敏度設置位址，範圍0x00-0x55，值越高越容易檢測但是越容易誤判，
                             #預設值为0x40                                         
    ASR_CLEAR_ADDR = 0x05    #清除資料缓存區操作地址，錄下字彙前需要清除資料缓存區
    ASR_KEY_FLAG = 0x06      #用于按键模式下，設置啟動識別模式
    ASR_VOICE_FLAG = 0x07    #用于設置是否開啟識別結果提示音
    ASR_RESULT = 0x08        #識別结果存放地址
    ASR_BUZZER = 0x09        #蜂鸣器控制寄存器地址，1為開，0為關
    ASR_NUM_CHECK = 0x0a     #字彙数目校驗地址    


    def __init__(self, bus=1):
        self.bus = smbus.SMBus(bus)
        
    def readByte(self):
        try:
            result = self.bus.read_byte(self.address)
        except:
            return None
        return result

    def writeByte(self, val):
        try:
            value = self.bus.write_byte(self.address, val)
        except:
            return False
        if value != 0:
            return False
        return True
    
    def writeData(self, reg, val):
        try:
            self.bus.write_byte(self.address, reg)
            self.bus.write_byte(self.address, val)
        except:
            pass

    def getResult(self):
        if ASR.writeByte(self, self.ASR_RESULT):
            return -1        
        try:
            value = self.bus.read_byte(self.address)
        except:
            return None
        return value

    '''
    * 添加字彙函式，
    * idNum：字彙對應的識別號碼，1~255随意设置。若是識別到該號碼對應的字彙語音時，
    *        會將識別號碼存放到ASR_RESULT_ADDR處，等待讀取，讀取後清0
    * words：要識別中文字的拼音，中文字之間用空格隔開
    '''
    def addWords(self, idNum, words):
        buf = [idNum]
        for i in range(0, len(words)):
            buf.append(eval(hex(ord(words[i]))))
        try:
            print(buf)
            self.bus.write_i2c_block_data(self.address, self.ASR_ADD_WORD_ADDR, buf)
        except:
            pass
        
    def eraseWords(self):
        try:
            result = self.bus.write_byte_data(self.address, self.ASR_CLEAR_ADDR, 0x40)
        except:
            return False
        if result != 0:
           return False
        return True
    
    def setMode(self, mode): 
        try:
            result = self.bus.write_byte_data(self.address, self.ASR_MODE_ADDR, mode)
        except:
            return False
        if result != 0:
           return False
        return True

    def setSensitivity(self, val): 
        try:
            result = self.bus.write_byte_data(self.address, self.ASR_SENS_ADDR, val)
        except:
            return False
        if result != 0:
           return False
        return True
    
    def setVoice(self, mode): 
        try:
            result = self.bus.write_byte_data(self.address, self.ASR_VOICE_FLAG, mode)
        except:
            return False
        if result != 0:
           return False
        return True    

    def setRGB(self, R,G,B):
        data = []
        data.append(R)
        data.append(G)
        data.append(B)
        self.bus.write_i2c_block_data(self.address, self.ASR_RGB_ADDR, data)
        