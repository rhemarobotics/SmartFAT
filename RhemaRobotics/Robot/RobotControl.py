'''-------------------------------------------------------
功能:透過opencv實現目標物輪廓的視覺辨識
說明:放置一方塊位於相機擷取範圍內進行輪廓辨識並按下ESC停止程式
執行:直接執行此檔案程式
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import sys
# 載入擴充板功能函式庫
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import numpy as np
from Board import *
from math import sqrt
from InverseKinematics import *


# 建立機器人功能函式庫
class Robot:
    
    # 初始化馬達旋轉角度
    servo3Range = (0, 1000, 0, 240) 
    servo4Range = (0, 1000, 0, 240)
    servo5Range = (0, 1000, 0, 240)
    servo6Range = (0, 1000, 0, 240)

    # 機器人逆運動學計算函式
    invkine = IK('arm')

    # 機器人初始化
    def __init__(self):
        self.setServoRange()

    # 把脈波寬度(ms)轉換成馬達旋轉角度角度(deg)
    def setServoRange(self, servo3_Range=servo3Range, servo4_Range=servo4Range, servo5_Range=servo5Range, servo6_Range=servo6Range):            
        self.servo3Range = servo3_Range
        self.servo4Range = servo4_Range
        self.servo5Range = servo5_Range
        self.servo6Range = servo6_Range
        self.servo3Param = (self.servo3Range[1] - self.servo3Range[0]) / (self.servo3Range[3] - self.servo3Range[2])
        self.servo4Param = (self.servo4Range[1] - self.servo4Range[0]) / (self.servo4Range[3] - self.servo4Range[2])
        self.servo5Param = (self.servo5Range[1] - self.servo5Range[0]) / (self.servo5Range[3] - self.servo5Range[2])
        self.servo6Param = (self.servo6Range[1] - self.servo6Range[0]) / (self.servo6Range[3] - self.servo6Range[2])

    # 把馬達旋轉角度(deg)轉換至相對應脈波位置(ms).
    def transformAngelAdaptArm(self, theta3, theta4, theta5, theta6):
        # 馬達3
        servo3 = int((self.servo3Range[1] + self.servo3Range[0])/2 + round(theta3 * self.servo3Param))
        if servo3 > self.servo3Range[1] or servo3 < self.servo3Range[0] + 60:
            logger.info('servo3(%s)over range(%s, %s)', servo3, self.servo3Range[0] + 60, self.servo3Range[1])
            return False
        # 馬達4
        servo4 = int((self.servo4Range[1] + self.servo4Range[0])/2 - round(theta4 * self.servo4Param))
        servo4 = servo4 - 10
        if servo4 > self.servo4Range[1] or servo4 < self.servo4Range[0]:
            logger.info('servo4(%s)over range(%s, %s)', servo4, self.servo4Range[0], self.servo4Range[1])
            return False
        # 馬達5
        servo5 = int(round((90.0-theta5) * self.servo5Param) + (self.servo5Range[1] + self.servo5Range[0])/2)
        servo5 = servo5 + 10
        if servo5 > ((self.servo5Range[1] + self.servo5Range[0])/2 + 90*self.servo5Param) or servo5 < ((self.servo5Range[1] + self.servo5Range[0])/2 - 90*self.servo5Param):
            logger.info('servo5(%s)over range(%s, %s)', servo5, self.servo5Range[0], self.servo5Range[1])
            return False
        # 馬達6
        if theta6 < -(self.servo6Range[3] - self.servo6Range[2])/2:
            servo6 = int(round(((self.servo6Range[3] - self.servo6Range[2])/2 + (90 + (180 + theta6))) * self.servo6Param))
        else:
            servo6 = int(round(((self.servo6Range[3] - self.servo6Range[2])/2 - (90 - theta6)) * self.servo6Param))
        if servo6 > self.servo6Range[1] or servo6 < self.servo6Range[0]:
            logger.info('servo6(%s)over range(%s, %s)', servo6, self.servo6Range[0], self.servo6Range[1])
            return False
        return {"servo3": servo3, "servo4": servo4, "servo5": servo5, "servo6": servo6}

    # 多軸連動至關節位置
    def simultSvoMoving(self, servos, movetime=None):
        time.sleep(0.02)
        if movetime is None:
            max_d = 0
            for i in  range(0, 4):
                d = abs(getBusServoPulse(i + 3) - servos[i])
                if d > max_d:
                    max_d = d
            movetime = int(max_d*4)
        setBusServoPulse(3, servos[0], movetime)
        setBusServoPulse(4, servos[1], movetime)
        setBusServoPulse(5, servos[2], movetime)
        setBusServoPulse(6, servos[3], movetime)
        return movetime

    # 設定手臂末端點座標位置(x,y,z)及俯仰角度範圍(alpha1，alpha2),計算適合的解
    # 無法求解,則返回false
    def tryGotoPoint(self, coordinate_data, alpha1, alpha2, da = 1):
        x, y, z = coordinate_data
        if alpha1 >= alpha2:
            da = -da
        for alpha in np.arange(alpha1, alpha2, da):#da,每一次微動量
            result = self.invkine.getRotationAngle((x, y, z), alpha)
            if result:
                theta3, theta4, theta5, theta6 = result['theta3'], result['theta4'], result['theta5'], result['theta6']
                servos = self.transformAngelAdaptArm(theta3, theta4, theta5, theta6)
                if servos != False:
                    return servos, alpha

        return False

    # 機器人運行至指定位置和角度(卡式座標系)
    # 手臂末端點座標位置(cm) coordinate_data
    # 手臂末端點俯仰角度(deg) alpha
    # 俯仰角範圍(deg) alpha1, alpha2
    # 如果無解返回false,否則返回馬達角度,俯仰角,運行時間(ms).    
    def gotoPoint(self, coordinate_data, alpha, alpha1, alpha2, movetime=None):

        x, y, z = coordinate_data
        result1 = self.tryGotoPoint((x, y, z), alpha, alpha1)
        result2 = self.tryGotoPoint((x, y, z), alpha, alpha2)
        if result1 != False:
            data = result1
            if result2 != False:
                if abs(result2[1] - alpha) < abs(result1[1] - alpha):
                    data = result2
        else:
            if result2 != False:
                data = result2
            else:
                return False
        servos, alpha = data[0], data[1]
        movetime = self.simultSvoMoving((servos["servo3"], servos["servo4"],
                                            servos["servo5"], servos["servo6"]), movetime)
        return servos, alpha, movetime

    # 直接控制各軸馬達轉至關節位置
    def servoMoving(self, id, pulpos):
        setBusServoPulse(id, pulpos, 500)

    # 讀取各軸馬達關節位置
    def getServoPulpos(self, id):
        return getBusServoPulse(id)

    # 開啟夾爪
    def openGripper(self):
        setBusServoPulse(1, 100, 1000)
        
    # 關閉夾爪
    def closeGripper(self):
        setBusServoPulse(1, 500, 1000)
        
    # 夾爪位置歸零
    def resetGripper(self):
        setBusServoPulse(2, 500, 1000)
        
    # 夾爪旋轉角度至脈波位置
    def rollGripper(self, pulpos):
        setBusServoPulse(2, pulpos, 1000)
        