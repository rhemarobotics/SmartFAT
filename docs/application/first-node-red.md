# 6.1. 第一個 Node-RED 程式

Owner: 耿良 王
Tags: tutorial documents
Date: March 1, 2024

# Node-RED 與 Arduino 通訊實習

## 一、實習目標：

- 透過 Node-RED 與 Arduino 建立序列通訊連線
- 實現基本的數據傳輸與設備控制

## 二、實驗步驟：

### 1. Arduino 端配置

撰寫 Arduino 程式碼，設定串口通信 (Serial Communication)，並建立分時多工執行緒 (thread) 以同時管理多個感測器的數據擷取。系統會定時從各感測器（如溫度、光線、濕度）讀取數據，並通過串口有序地傳送這些數據至指定設備。

- 每1秒更新溫/濕度感測器數據一次
- 每0.8秒更新氣體感測器數據一次
- 每0.3秒更新光敏感測器數據一次
- 每0.3秒更新火焰感測器數據一次
- 每0.2秒更新按鍵狀態一次
- 每0.2秒更新紅外線偵測狀態一次
- 每0.2秒更新旋轉電位計值一次
- 每0.5秒上傳數據一次。

```arduino
/* 
 * VisualData_pthread.ino
 * 目的:
 *  多感測器數據收集(透過分時多工處理)
 * 方法:
 *  每1秒更新溫/濕度感測器數據一次
 *  每0.8秒更新氣體感測器數據一次 
 *  每0.3秒更新光敏感測器數據一次 
 *  每0.3秒更新火焰感測器數據一次  
 *  每0.2秒更新按鍵狀態一次
 *  每0.2秒更新紅外線偵測狀態一次
 *  每0.2秒更新旋轉電位計值一次
 *  每0.5秒上傳數據一次
 * 步驟:
 *  直接執行程式
 * 結果:
 *  透過序列埠監看視窗觀察數值變化
 */
 
#include "DHT.h"              //掛載溫/濕度感測器函式庫
#include "protothreads.h"     //多執行緒函式庫

#define buttonPin       24    //定義按鍵腳位連接至24腳
#define dhtPin          26    //定義溫/濕度感測器腳位連接至26腳
#define IR_PIN          40    //定義紅外線感測器腳位連接至40腳
#define dhtType         DHT11 //定義溫/濕度感測器型別

#define flameDigitalPin A7    //定義火焰感測器腳位連接至A7腳
#define mq4AnalogPin    A4    //定義氣體感測器腳位連接至A4腳
#define lightPin        A2    //定義光敏感測器腳位連接至A2腳
#define KNOB_PIN        A0    //定義旋轉電位計腳位連接至A0腳

/* protothreads結構變數 */
static struct pt ptTempH;     //溫濕度感測器執行緒
static struct pt ptMQ4;       //氣體感測器執行緒
static struct pt ptLux;       //光敏感測器執行緒
static struct pt ptFlame;     //火焰感測器執行緒
static struct pt ptButton;    //按鍵偵測執行緒
static struct pt ptKnob;      //旋轉電位計執行緒
static struct pt ptIRdet;     //紅外線偵測執行緒
static struct pt ptSendDat;   //數據上傳執行緒

const int R_0 = 945;          //定義氣體感測器RO測量值
DHT dht(dhtPin, dhtType);     //宣告溫濕度感測器物件

/* 感測器數據變數 */
float dhtHumid = 0.0;         //濕度值
float dhtTemp = 0.0;          //溫度值
float lux = 0.0;              //光敏感測器類比量測值
float mq4 = 0.0;              //氣體感測器值
float ohm = 0.0;              //讀取旋轉電位計類比輸出值 
int flameStat = 0;            //火焰感測器狀態
int buttonStat = 0;           //按鍵狀態
int ir_value = 0;             //紅外線狀態
```

- 程式初始化

```arduino
void setup() 
{
  //初始化功能腳位
  pinMode(flameDigitalPin, INPUT); //設置火焰感測器接腳為輸入接腳
  pinMode(mq4AnalogPin, INPUT);    //設置氣體感測器接腳為輸入接腳
  pinMode(lightPin, INPUT);        //設置光敏感測器腳位為輸入接腳
  pinMode(buttonPin, INPUT);       //設置按鍵腳位為輸入接腳
  pinMode(KNOB_PIN, INPUT);        //設定KNOB_PIN為輸入接腳
  pinMode(IR_PIN, INPUT);          //設定IR_PIN為輸入接腳
          
  Serial.begin(9600);
  dht.begin();                     //初始化溫濕度感測器

  /* 執行緒的初始化 */
  PT_INIT(&ptTempH);
  PT_INIT(&ptMQ4);
  PT_INIT(&ptFlame);
  PT_INIT(&ptLux);
  PT_INIT(&ptButton);
  PT_INIT(&ptKnob);
  PT_INIT(&ptIRdet);
  PT_INIT(&ptSendDat);
}
```

- 感測器數據擷取功能副程式

```arduino
/* 溫/濕度感測器數據更新執行緒 */
static int GetTempHumThread(struct pt *pt, int interval)
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis(); // take a new timestamp
    dhtHumid = dht.readHumidity();  //更新濕度值
    dhtTemp = dht.readTemperature();//更新溫度值
  }
  PT_END(pt);
}

/* 光敏感測器數據更新執行緒 */
static int GetLuxThread(struct pt *pt, int interval) 
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis();
    lux = analogRead(lightPin); //更新光敏感測器數據
  }
  PT_END(pt);
}

/* 火焰感測器數據更新執行緒 */
static int GetFlameThread(struct pt *pt, int interval) 
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis();
    flameStat = !digitalRead(flameDigitalPin); //更新火焰感測器狀態,反向輸出
  }
  PT_END(pt);
}

/* 計算甲烷濃度PPM值 */
float getMethanePPM()
{
   float a0 = analogRead(mq4AnalogPin);   
   float v_o = a0 * 5 / 1023;             
   float R_S = (5-v_o) * 1000 / v_o;
   float PPM = pow(R_S/R_0,-2.95) * 1000;
   return PPM;
}

/* 氣體感測器數據更新執行緒 */
static int GetMq4Thread(struct pt *pt, int interval) 
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis();
    mq4 = getMethanePPM(); //更新MQ4值
  }
  PT_END(pt);
}

/* 按鍵偵測執行緒 */
static int GetBtnStatThread(struct pt *pt, int interval) 
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis();
    buttonStat = !digitalRead(buttonPin); //更新按鍵目前狀態,反向輸出
  }
  PT_END(pt);
}

/* 旋轉電位計執行緒 */
static int GetKnobThread(struct pt *pt, int interval) 
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis();
    ohm = 1023 - analogRead(KNOB_PIN);//更新電位計值
  }
  PT_END(pt);
}

/* 紅外線數據更新執行緒 */
static int GetIRdetThread(struct pt *pt, int interval) 
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis();
    ir_value = !digitalRead(IR_PIN); //讀取紅外線感測器數位狀態(0或1),反向輸出
  }
  PT_END(pt);
}

/* 資料封包格式 */
void transmission()
{
  String str_Payload;
  int Ndata = 9;
  str_Payload += Ndata;
  str_Payload += " " + String(dhtTemp,1);
  str_Payload += " " + String(dhtHumid,0);
  str_Payload += " " + String(lux,0);
  str_Payload += " " + String(flameStat,DEC);
  str_Payload += " " + String(mq4,2);
  str_Payload += " " + String(buttonStat,DEC);
  str_Payload += " " + String(ohm,0);
  str_Payload += " " + String(ir_value,DEC);
  str_Payload += " ";
  /* 透過USB串口傳送資料至樹莓派(Node-Red) */
  Serial.print(str_Payload);  
}

/* 數據上傳執行緒 */
static int SendDataThread(struct pt *pt, int interval) 
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) 
  { 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis();
    transmission();
  }
  PT_END(pt);
}
```

- 主程式執行

```arduino
void loop() 
{
  /* 規劃啟動執行緒 */
  GetTempHumThread(&ptTempH, 1000); //do once in every 1000ms.
  GetMq4Thread(&ptMQ4, 1000);
  GetLuxThread(&ptLux, 200);
  GetFlameThread(&ptFlame, 200);
  GetBtnStatThread(&ptButton, 100);
  GetKnobThread(&ptKnob,100);
  GetIRdetThread(&ptIRdet,100);
  SendDataThread(&ptSendDat, 500);
}
```

- 透過序列埠監控視窗觀察執行結果，數據每0.5秒更新一次。

![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image5.png)

### 2. Node-RED 端配置(樹莓派)

- 使用 Serial-in、Serial-out 節點設置通訊
- 設計基本的 Node-RED 流程，將從 Arduino 接收的數據顯示在 Dashboard 上
- 增加簡單的控制節點，例如開關 LED
1. Node-RED 安裝『node-red-node-serialport』功能節點。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image6.png)
    
    接著可以找到新增了三個序列通訊用的功能節點(Nodes)。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image14.png)
    
2. 於Node-RED新建一個『serialin』節點並命名為『ArduinoMega』，設置內部的序列埠口與鮑率(Baud Rate)。序列通訊鮑率需與Arduino程式設定一樣，雙方才能正確通信。
    
    ![2024-03-14-054429_453x216_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/2024-03-14-054429_453x216_scrot.png)
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image.png)
    
3. 於Node-RED新建一個『function』節點並命名為『BinToString』。因為Arduino傳輸的資訊是二進制(Binary)數據模式，透過此功能節點可以把二進制轉成字串模式，方便之後的字串解析。
    
    ```jsx
    var newMsg = {payload: msg.payload.toString()};
    return newMsg;
    ```
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image%201.png)
    
4. 於Node-RED新建一個『split』節點，用『空白符號』把數據字串分開。
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image%202.png)
    
    ![image.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image%203.png)
    
5. 於Node-RED新建一個『function』節點並命名為『Payload Object Sensor』，把數據字串分配到對應的感測器，之後可以在 Dashboard 顯示元件。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image2.png)
    
    ```jsx
    var newMsg = {};
    var Sensor = {
        NData:0, 
        Temp:0,
        Humid:0,
        Light:0,
        Flame:0,
        Mq4:0,
        Btn:0,
        Ohm:0,
        Irdet:0,
        Time: new Date().toString()
    };
    
    context.data = context.data || {};
    switch(msg.parts.index)
    {
        case 0:
            context.data.NData = parseFloat(msg.payload);
            msg = null;
            break;
        case 1:
            context.data.Temp = parseFloat(msg.payload);
            msg = null;
            break;
        case 2:
            context.data.Humid = parseFloat(msg.payload);
            msg = null;
            break;
        case 3:
            context.data.Light = parseFloat(msg.payload);
            msg = null;
            break;
        case 4:
            context.data.Flame = parseFloat(msg.payload);
            msg = null;
            break;
        case 5:
            context.data.Mq4 = parseFloat(msg.payload);
            msg = null;
            break;    
        case 6:
            context.data.Btn = parseFloat(msg.payload);
            msg = null;
            break;  
        case 7:
            context.data.Ohm = parseFloat(msg.payload);
            msg = null;
            break;    
        case 8:
            context.data.Irdet = parseFloat(msg.payload);
            msg = null;
            break;         
        default:
            msg = null;
            break;
    }
    
    Alldata = context.data.Temp && context.data.Humid;
    if(Alldata)
    {
        var time = Date();
        context.data.Time = time.toString();
        Sensor = context.data;
        newMsg = { payload: context.data, topic: 'Bigdata' };
        context.data = null;
        return newMsg;
    }
    else
        return msg;
    ```
    
6. 於Node-RED新建一個『file』節點並命名為『SaveTo_SensorFile』，收集到的感測器數據會存放於此。
    
    ![2024-03-14-054632_462x356_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/2024-03-14-054632_462x356_scrot.png)
    
7. 完整的感測器數據交換Node-RED程式。
    
    ![2024-03-14-072318_972x125_scrot.png](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/2024-03-14-072318_972x125_scrot.png)
    
8. 部署Node-RED訂閱/發布程式，點選右上角的【部署】按鈕，即可完成通訊協定的連線測試。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image13.png)
    

## 三、實驗結果

1. 觀察執行結果。當執行Node-RED程式後，觀察『serialin』節點是否有出現【**已連接**】的文字。若是有，則代表Arduino控制器與Node-RED主機間的序列通訊是正常的。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image7.png)
    
2. 當序列通訊正常後，打開『**Sensor DataBase.txt**』文字檔，以觀察數據的即時更新情況。如果結果正常，下一步便是進行數據的可視化分析，以更清晰地呈現數據趨勢與變化。
    
    ![](../assets/6%20%E7%89%A9%E8%81%AF%E7%B6%B2%E6%87%89%E7%94%A8%E5%B1%A4/6%201%20%E7%AC%AC%E4%B8%80%E5%80%8B%20Node-RED%20%E7%A8%8B%E5%BC%8F/image11.png)