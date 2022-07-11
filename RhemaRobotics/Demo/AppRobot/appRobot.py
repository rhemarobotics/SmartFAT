'''-------------------------------------------------------
功能:實現 Video Streaming 影像串流伺服器
說明:可以透過手機App或是一般網頁, 連至影像串流伺服器即時觀察
    輸入: 0.0.0.0:5000
執行:直接執行程式即可(按下Ctrl+C結束程式)
----------------------------------------------------------
'''
#!/usr/bin/env python3
# encoding:utf-8

import sys
sys.path.append('/home/pi/RhemaRobotics/Robot/')
import time
from RobotControl import Robot
from flask import Flask, render_template, request

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

# 全域變數
__target_servo = ''
__target_svofun = {}
__servo_stop = True

# 建立一機器人物件
myBot = Robot()
# 機器人移動至工作點位置
print(myBot.gotoPoint((0, 15, 15), -30, -90, 0, 1500))
time.sleep(1.5)
# 夾爪旋轉頭重置並打開機器人夾爪
myBot.resetGripper()
time.sleep(1)
myBot.openGripper()
time.sleep(1)
    
# 機器人網頁控制伺服器
app = Flask(__name__)

# 機器人網頁控制伺服器首頁
@app.route('/', methods=['GET'])
def index():
    global __target_servo
    global __servo_stop
    __target_servo = request.args.get('servo')
    print(__target_servo)
    #判斷網頁上需要執行的的按鍵選項
    __target_svofun = str_to_dict(__target_servo)
    #返回值正確即執行機器人運動程式
    if __target_svofun is not None:
        if __servo_stop:
            servoCtrl(__target_svofun[0], __target_svofun[1])           
    return render_template('index.html')

def str_to_dict(strfn):
    funcs = {
        'revA1' : (1, '-'),
        'homA1' : (1, 'o'),
        'fwdA1' : (1, '+'),
        'revA2' : (2, '-'),
        'homA2' : (2, 'o'),
        'fwdA2' : (2, '+'),
        'revA3' : (3, '-'),
        'homA3' : (3, 'o'),
        'fwdA3' : (3, '+'),
        'revA4' : (4, '-'),
        'homA4' : (4, 'o'),
        'fwdA4' : (4, '+'),
        'revA5' : (5, '-'),
        'homA5' : (5, 'o'),
        'fwdA5' : (5, '+'),
        'revA6' : (6, '-'),
        'homA6' : (6, 'o'),
        'fwdA6' : (6, '+')
    }
    return funcs.get(strfn, None)

def servoCtrl(id, strFunc):
    global __servo_stop
    __servo_stop = False
    print('id:' + str(id) + ';' + 'func:' + strFunc)
    if (id == 0 or strFunc == ''):
        return
    #執行機器人運動控制    
    delPulse = 0
    curPulpos = myBot.getServoPulpos(id)
    if strFunc == '+':
        delPulse = 50
    elif strFunc == '-':
        delPulse = -50
    elif strFunc == 'o':
        curPulpos = 500
    myBot.servoMoving(id, curPulpos + delPulse)
    time.sleep(0.5)
    __servo_stop = True
    
# 開啟機器人網頁控制伺服器服務
if __name__ == '__main__':
    # 0.0.0.0可以改成自訂ip位置
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)