/*****************************************************
 * SmartFactoryEx2.ino 
 * 目的:
 *  測試智慧工廠範例二功能 - 透過機器人實現智慧工廠物件顏色分類應用 
 *  放置物件於輸送帶上,待物件被超音波感測器偵測到後,會停止輸送帶,
 *  並通知樹莓派機器人夾取物件放置於對應的顏色位置
 * 方法:
 *  8*8矩陣LED + 輸送帶模組 + 旋轉電位器 + 超音波感測器
 * 步驟:
 *  直接執行程式
 * 結果:
 *  1.剛開始,開啟輸送帶運轉
 *  2.8*8矩陣LED顯示物件在輸送帶上傳送示意圖
 *  3.但若超音波感測器偵測到輸送帶上的物件,則命輸送帶停止運轉
 *  4.8*8矩陣LED顯示一向上箭頭符號,通知樹莓派機器人,
 *  5.待機器人取走物件後,則回到步驟1
*****************************************************/
#include "pitches.h"    //掛載矩陣LED箭頭圖形
#include <LedControl.h> //掛載矩陣LED標頭檔

#define M_1A_PIN    2   //定義輸送帶方向控制腳位連接至2腳
#define M_1B_PIN    3   //定義輸送帶速度控制腳位連接至3腳

#define UR_TRIG_PIN 8   //定義超音波感測器發射腳位連接至8腳
#define UR_REV_PIN  9   //定義超音波感測器接收腳位連接至9腳

#define LED_DIN    42   //定義矩陣LED資料腳位連接至42腳
#define LED_CS     44   //定義矩陣LED致能腳位連接至44腳
#define LED_CLK    46   //定義矩陣LED時序腳位連接至46腳

#define KNOB_PIN    A0  //定義旋轉電位器腳位連接至A0腳

//矩陣LED圖形
const uint64_t IMAGES[] = {
  0xff000001010000ff, 0xff000003030000ff, 0xff000006060000ff,
  0xff00000c0c0000ff, 0xff000018180000ff, 0xff000030300000ff,
  0xff000060600000ff, 0xff0000c0c00000ff, 0xff000080800000ff,
  0x18181818ff7e3c18
};
const int IMAGES_LEN = sizeof(IMAGES)/8;

//宣告矩陣LED物件
LedControl ledctrl = LedControl(LED_DIN, LED_CLK, LED_CS);

//設定輸送帶前進速度(0~255)
int fwdSpeed = 10; 

//中斷更新時間0.5s
int delay_time = 500;                        
unsigned long delayStart = 0;

//事件旗標
bool isObjDetected = false;
bool delayRunning = false;
bool isNotify = false;
bool isObjTaken = false;


/************************* 初始設定 *********************/
void setup() 
{
  pinMode(M_1A_PIN, OUTPUT);   //設定輸送帶M_1A_PIN為輸出接腳
  pinMode(M_1B_PIN, OUTPUT);   //設定輸送帶M_1B_PIN為輸出接腳
  pinMode(KNOB_PIN, INPUT);    //設定旋轉電位器NOB_PIN為輸入接腳
  pinMode(UR_TRIG_PIN, OUTPUT);//設定UR_TRIG_PIN為輸出接腳
  pinMode(UR_REV_PIN, INPUT);  //設定UR_REV_PIN 為輸入接腳
 
  digitalWrite(M_1A_PIN, LOW); //設定輸送帶反向
  digitalWrite(M_1B_PIN, LOW); //設定輸送帶停止

  ledctrl.clearDisplay(0);     //矩陣LED畫面清除
  ledctrl.shutdown(0, false);
  ledctrl.setIntensity(0, 5);  //設定矩陣LED亮度

  Serial.begin(9600);

  delayStart = millis();       //取得當前系統時間
  delayRunning = true;    
}

/************************* 主程式 ***********************/
int i = 0;
int k = 0;
void loop() 
{
  //輸送帶速度控制
  TunningConyVel();

  //每0.5秒執行中斷一次
  if (delayRunning && (millis()- delayStart) >= delay_time)
  {
    //重置delay時間
    delayStart += delay_time;
    
    //物件偵測?
    int dis = CalculateDistUR();
    
    // 偵測到物件,距離小於 100mm
    if (dis < 100 && dis > 0)
    {
      //確定物件已經到達定位
      stopConveyor();

      if (isNotify)
      {
        //目標物取走,重置系統狀態旗標
        k=0;
        isNotify = false;
      }
      else
      {
        displayImage(IMAGES[9]);
        Serial.println("ready"); //通知手臂夾取物件,謹此一次
        isNotify = true;
      }
    }
    else
    {
      //輸送帶持續運行
      forward(); 
      
      //LED矩陣圖形輸出
      displayImage(IMAGES[i]);
      if (++i >= IMAGES_LEN-1 ) {
        i = 0;
      }
    }
  }
}

/*********** 矩陣LED顯示函數 ***************************/
void displayImage(uint64_t image) 
{
  for (int i = 0; i < 8; i++) 
  {
    byte row = (image >> i * 8) & 0xFF;
    
    for (int j = 0; j < 8; j++) 
    {
      ledctrl.setLed(0, i, j, bitRead(row, j));
    }
  }
}

/*********** 輸送帶速度調整函數 *************************/
void TunningConyVel()
{
  int data = analogRead(KNOB_PIN);
  int val = map(data, 0, 1023, 254, 0);
  fwdSpeed = 255 - val + 250; //向左調,速度變小;反之,速度變大
}

/*********** 輸送帶停止函數 ****************************/
void stopConveyor()
{
  digitalWrite(M_1A_PIN, LOW);
  digitalWrite(M_1B_PIN, LOW);
}

/*********** 輸送帶正向運轉函數 ************************/
void forward()
{
  digitalWrite(M_1A_PIN, HIGH);
  analogWrite(M_1B_PIN, fwdSpeed);
}

/*********** 超音波距離計算函數(mm) ********************/
int CalculateDistUR()
{
  long duration;
  
  digitalWrite(UR_TRIG_PIN, LOW);
  delayMicroseconds(5);
  digitalWrite(UR_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(UR_TRIG_PIN, LOW);
  
  duration = pulseIn(UR_REV_PIN, HIGH);
  
  return (duration/2) / 2.91;
}
