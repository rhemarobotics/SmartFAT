# 7.4. 伺服馬達控制範例

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

### 實習目標：

1. 建立伺服馬達驅動擴展板與智慧型伺服馬達的序列通訊。
2. 控制單一伺服馬達的位置和速度，實現精確的運動。
3. 進行多伺服馬達的協調控制，實現簡單的機械手臂運動。

### 前置作業：

1. 確定是否有安裝 /home/pi/RhemaRobotics/Sdk/BusServoCmd.py。
2. 確定馬達擴充板與伺服馬達連線是否正確。

### 範例程式碼

> /home/pi/RhemaRobotics/Demo/BusServoMove.py
> 

```python
'''-------------------------------------------------------
功能:串列式伺服馬達控制範例
說明:透過串列埠控制各軸伺服馬達位置,當運行到指定位置時,馬達停止轉動;
     當按下鍵盤Ctrl+C時,禁能(Disable)各軸伺服馬達
執行:sudo python3 BusServoMove.py
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/RhemaRobotics/Sdk/')
import time
import signal
import Board as board

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
start = True
def Stop(signum, frame):
    global start
    start = False
    print('關閉中...')

# 主程式開始
if __name__ == '__main__':
    print('按下鍵盤Ctrl+C,中斷程式...')
    
    #設置鍵盤中斷訊號至Stop副程式
    signal.signal(signal.SIGINT, Stop)
    
    #致能(Enable)所有的伺服馬達運動
    board.loadBusServo(1)
    board.loadBusServo(2)
    board.loadBusServo(3)
    board.loadBusServo(4)
    board.loadBusServo(5)
    board.loadBusServo(6)   
    
    #主程式迴圈
    # 参数：(馬達id,脈波位置,運行時間)
    board.setBusServoPulse(6, 500, 1000)
    time.sleep(1)
    board.setBusServoPulse(5, 360, 1000)
    time.sleep(1)
    board.setBusServoPulse(4, 230, 1000)
    time.sleep(1)
    board.setBusServoPulse(3, 100, 1000)
    time.sleep(1)
    board.setBusServoPulse(2, 500, 1000)
    time.sleep(1)
    board.setBusServoPulse(2, 200, 1000)
    time.sleep(1)
    board.setBusServoPulse(2, 500, 1000)
    time.sleep(1)
    
    #停止所有的伺服馬達運動
    board.stopBusServo(0)
    time.sleep(1)
    
    while True:
        if not start:
            #禁能所有的伺服馬達運動
            board.unloadBusServo(1)
            time.sleep(0.5)
            board.unloadBusServo(2)
            time.sleep(0.5)
            board.unloadBusServo(3)
            time.sleep(0.5)
            board.unloadBusServo(4)
            time.sleep(0.5)
            board.unloadBusServo(5)
            time.sleep(0.5)
            board.unloadBusServo(6)
            time.sleep(0.5)                    
            print('已關閉')
            break;
```