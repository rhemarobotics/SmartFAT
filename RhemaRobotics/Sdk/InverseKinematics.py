'''
-------------------------------------------------------------
機械手臂的逆運動學
給定一空間座標位置(x,y,z)和夾爪角度基於世界座標並計算每個伺服馬達轉動角度
-------------------------------------------------------------
'''

#!/usr/bin/env python3
# encoding: utf-8

import logging
from math import *

# CRITICAL, ERROR, WARNING, INFO, DEBUG
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class IK:
    # 連桿參數(Unit:cm)
    d0 = 6.8
    a1 = 1.05
    a2 = 10.4
    a3 = 9.8
    a4 = 18.0

    def __init__(self, arm_type):
        arm_type='arm'
        
    def setLinkLength(self, D0=d0, A1=a1, A2=a2, A3=a3, A4=a4):
        self.d0 = D0
        self.a1 = A1
        self.a2 = A2
        self.a3 = A3
        self.a4 = A4

    def getLinkLength(self):
        return {"D0":self.d0, "A1":self.a1, "A2":self.a2, "A3":self.a3, "A4":self.a4}

    # 輸入手臂末端點(X,Y,Z)位置, 單位:cm, Ex:(0, 5, 10) 
    # 輸入手臂Alpha角, 單位:deg.
    # 計算解 theta3,theta4,theta5,theta6, 若找不到解,則返回false.
    def getRotationAngle(self, coordinate_data, Alpha):
        
        X, Y, Z = coordinate_data
        # theat6
        theta6 = degrees(atan2(Y, X))
 
        P_O = sqrt(X*X + Y*Y)
        CD = self.a4 * cos(radians(Alpha))
        PD = self.a4 * sin(radians(Alpha))
        AF = P_O - CD - self.a1
        CF = Z - self.d0 - PD
        AC = sqrt(pow(AF, 2) + pow(CF, 2))
        
        if round(CF, 4) < -self.d0:
            logger.debug('高度低於0, CF(%s)<d0(%s)', CF, -self.d0)
            return False
        if self.a2 + self.a3 < round(AC, 4):
            logger.debug('不滿足幾何餘弦定理, a2(%s) + a3(%s) < AC(%s)', self.a2, self.a3, AC)
            return False

        # theat4
        cos_ABC = round((pow(self.a2,2)+pow(self.a3,2)-pow(AC,2))/(2*self.a2*self.a3), 4)
        if abs(cos_ABC) > 1:
            logger.debug('不滿足幾何餘弦定理, abs(cos_ABC(%s)) > 1', cos_ABC)
            return False
        ABC = acos(cos_ABC)
        theta4 = 180.0 - degrees(ABC)

        # theta5
        CAF = acos(AF/AC)
        cos_BAC = round((pow(self.a2,2)+pow(AC,2)-pow(self.a3,2))/(2*self.a2*AC), 4)
        if abs(cos_BAC) > 1:
            logger.debug('不滿足幾何餘弦定理, abs(cos_BAC(%s)) > 1', cos_BAC)
            return False
        if CF < 0:
            zf_flag = -1
        else:
            zf_flag = 1
        theta5 = degrees(CAF * zf_flag + acos(cos_BAC))

        # theta3(reverse)
        theta3 = Alpha - theta5 + theta4

        return {"theta3":theta3, "theta4":theta4, "theta5":theta5, "theta6":theta6}

# 給一個位置座標, 計算IK值
if __name__ == '__main__':
    ik = IK('arm')
    print('連桿長度：', ik.getLinkLength())
    #print(ik.getRotationAngle((0, 0, ik.d0 + ik.a2 + ik.a3 + ik.a4), 90))
    print(ik.getRotationAngle((0, 15, 15), -30))
