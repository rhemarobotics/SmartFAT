/*****************************************************
 * VisualData.ino 
 * 目的:
 *  大數據可視化分析
 * 方法:
 *  溫濕度感測器 + 氣體感測器 + 火焰感測器 + 光敏感測器
 * 步驟:
 *  直接執行程式
 * 結果:
 *  透過序列埠監看視窗觀察數值變化
*****************************************************/

#include "DHT.h"              //掛載溫濕度感測器函式庫 

#define dhtPin          26    //定義溫濕度感測器腳位連接至26腳
#define dhtType         DHT11 //定義溫濕度感測器型別  

#define FlameDigitalPin A7    //定義火焰感測器腳位連接至A7腳
#define MQ4AnalogPin    A4    //定義氣體感測器腳位連接至A4腳
#define lightPin        A2    //定義光敏感測器腳位連接至A2腳

const int R_0 = 945;          //定義氣體感測器RO測量值
DHT dht(dhtPin, dhtType);     //宣告溫濕度感測器物件

int delay_time = 5000;        //中斷更新時間5s                         
unsigned long delayStart = 0;
bool delayRunning = false;    //事件旗標


/************************* 初始設定 *******************/
void setup() 
{
  pinMode(FlameDigitalPin, INPUT); //設置火焰感測器接腳為輸入接腳
  pinMode(MQ4AnalogPin, INPUT);    //設置氣體感測器接腳為輸入接腳
  pinMode(lightPin, INPUT);        //設置光敏感測器腳位為輸入接腳
      
  Serial.begin(9600);
  dht.begin();                     //初始化溫濕度感測器

  delayStart = millis();           //取得當前系統時間
  delayRunning = true;    
}

/************************* 主程式 *********************/
void loop() 
{
  //每0.5秒執行中斷一次
  if (delayRunning && (millis() - delayStart) >= delay_time)
  {
    //重置delay時間
    delayStart += delay_time;
    
    //感測器數據
    String Temp  = String(dht.readTemperature(),1);         //讀取溫度(攝氏)
    String Humid = String(dht.readHumidity(),0);            //讀取濕度
    String light = String(analogRead(lightPin),DEC);        //讀取光敏感測器類比值0~1023
    String Flame = String(digitalRead(FlameDigitalPin),DEC);//讀取火焰感測器數位值0~1
    String Mq4   = String(getMethanePPM(),2);               //讀取氣體感測器類比值0~1023
  
    //資料封包格式
    String str_Payload;
    int Ndata = 6;
    str_Payload += Ndata;
    str_Payload += " " + Temp;
    str_Payload += " " + Humid;
    str_Payload += " " + light;
    str_Payload += " " + Flame;
    str_Payload += " " + Mq4;
    str_Payload += " ";
    
    //透過USB串口傳送資料至樹莓派(Node-Red)
    Serial.print(str_Payload);
  }
}

/*********** 計算甲烷濃度PPM值 **************************/
float getMethanePPM()
{
   float a0 = analogRead(MQ4AnalogPin);   
   float v_o = a0 * 5 / 1023;             
   float R_S = (5-v_o) * 1000 / v_o;      
   float PPM = pow(R_S/R_0,-2.95) * 1000;
   delay(100);
   return PPM;
}
