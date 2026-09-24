# 4.2. 火焰感測器實習

Owner: 耿良 王
Tags: tutorial documents
Date: March 15, 2024

# **壹、實習前準備**

<aside>
💡 物聯網感知層實務技術，本章節介紹智慧工廠教學實驗平台各感測器的功能原理與程式開發，透過實作練習，不僅能學習到感測器的基礎知識，也能了解如何將它們應用在物聯網的感知層，幫助同學深入地掌握智慧工廠相關技術，為未來的學習打下良好基礎。

</aside>

## 一、智慧工廠感測器元件

- 智慧工廠教學實驗平台提供豐富的感測器元件，可分為三大類，環境監控、感測/控制、燈號/數據顯示元件，共計16種，如下圖。
    
    ![](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%201%20%E7%93%A6%E6%96%AF%E6%B0%A3%E9%AB%94%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image9.png)
    

## 二、連線至智慧工廠

- 請參考 🚩[**3.實驗平台開發環境**](../development/setup.md) 設置好本地端電腦與智慧工廠端之間的連線，透過VNC連線至智慧工廠，打開Arduino IDE並載入範例程式。

# **貳、火焰感測器**

<aside>
💡

火焰檢測器是一種可以檢測**火焰**存在的傳感器。這些探測器能夠識別無菸液體和可能產生明火的煙霧。例如，在鍋爐爐膛中，火焰探測器被廣泛使用，因為火焰探測器可以探測熱量、煙霧和火災。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%202%20%E7%81%AB%E7%84%B0%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image.png)

</aside>

## 一、實習目的

- 了解火焰感測器的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- 火焰感測器
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%202%20%E7%81%AB%E7%84%B0%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%201.png)
    
- 感測器原理
    
    利用紅外線對火焰非常敏感的特點，使用特製的**紅外線接收器**檢測火焰，藉由火焰的亮度變化轉化為對應的電壓信號值
    
- 元件內部電路圖
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%202%20%E7%81%AB%E7%84%B0%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%202.png)
    

## 三、實習步驟

- 打開Arduino IDE，載入/ArduinoProjects/Programming/FlameSensor/FlameSensor.ino檔案。
- 用打火機產生火焰至感測器前晃動(非接觸)。

## 四、範例程式

```arduino
/*****************************************************
 * FlameSensor.ino 
 * 目的:
 *  測試火焰感測器偵測功能
 * 方法:
 *  火焰感測器 + 蜂鳴器
 * 步驟:
 *  可用打火機在感測器前點火測試(感測器上的可變電阻可以調整靈敏度)
 * 結果:
 * 1. 觀察火焰感測器上的LED是否亮起
 * 2. 當偵測到火焰時,蜂鳴器會發出警報聲
*****************************************************/

#define FlameDigitalPin   A7 //定義火焰感測器腳位連接至A7腳
#define FlameAnalogPin    A6 //定義火焰感測器腳位連接至A6腳
#define BuzzerPin         36 //定義蜂鳴器腳位連接至36腳

int FlameAnalogValue  = 0;   //讀取火焰感測器類比值
int FlameDigitalValue = 0;   //讀取火焰感測器數位值

/************************* 初始設定 *********************/
void setup()
{
  Serial.begin(9600);              //設置埠口通訊速率
  
  pinMode(FlameDigitalPin, INPUT); //設置火焰感測器數位接腳為輸入
  pinMode(FlameAnalogPin,  INPUT); //設置火焰感測器類比接腳為輸入
  pinMode(BuzzerPin,       OUTPUT);//設置蜂鳴器接腳為輸出
}

/************************* 主程式 ***********************/
void loop()
{
  FlameAnalogValue = analogRead(FlameAnalogPin);    //讀取火焰感測器類比值
  FlameDigitalValue = digitalRead(FlameDigitalPin); //讀取火焰感測器數位值
  
  Serial.print("FlameAnalog Data:  ");
  Serial.println(FlameAnalogValue);  //輸出火焰感測器類比值
  Serial.print("FlameDigital Data:  ");
  Serial.println(FlameDigitalValue); //輸出火焰感測器數位值
  
  //判斷火焰感測器是否檢測到火焰，若是，則蜂鳴器發出警報聲
  if (FlameDigitalValue == 0) 
  {
    //蜂鳴器音頻由低到高 200HZ ~ 800HZ  
    for(int i = 200; i <= 800; i++)  
    {  
        tone(BuzzerPin, i);
    }  
    
    delay(1000); //延遲1秒   

    //蜂鳴器音頻由高到低 800HZ ~ 200HZ
    for(int i= 800; i >= 200; i--)   
    {  
        tone(BuzzerPin, i);  
        delay(10);  
    }  
  }
  else
  {
    noTone(BuzzerPin); //關閉蜂鳴器
    delay(10);
  }
}
```

## 五、實習結果

- 觀察火焰感測器上的LED是否亮起。
- 當偵測到火焰時，蜂鳴器會發出警報聲。