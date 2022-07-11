'''-------------------------------------------------
    RPi Text-To-Speech(TTS)
----------------------------------------------------
'''
#!/usr/bin/env python3
# coding=utf8
import time
import smbus

class TTS:
    address = 0x30
    bus = None

    def __init__(self, bus=1):
        self.bus = smbus.SMBus(bus)
    
    def WireReadTTSDataByte(self):
        try:
            val = self.bus.read_byte(self.address)
        except:
            return False
        return True
    
    def TTSModuleSpeak(self, sign, words):
        head = [0xFD,0x00,0x0A,0x01,0x02]           #文本播放命令
        wordslist = words.encode("BIG5")            #文本編碼格式編碼BIG5
        signdata = sign.encode("BIG5")    
        length = len(signdata) + len(wordslist) + 2
        head[1] = length >> 8
        head[2] = length
        head.extend(list(signdata))
        head.extend(list(wordslist))       
        try:
            self.bus.write_i2c_block_data(self.address, 0, head) #向從機發送數據
        except:
            pass
        time.sleep(0.05)
        