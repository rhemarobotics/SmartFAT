# 4.1. 瓦斯氣體感測器實習

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

# **貳、瓦斯氣體感測器**

<aside>
💡

瓦斯氣體感測器對**甲烷**的靈敏度高，對酒精等氣體也有抗干擾性，廣泛應用於家用天然氣洩漏警報器、工業可燃氣體警報器和便攜式氣體檢測儀等。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%201%20%E7%93%A6%E6%96%AF%E6%B0%A3%E9%AB%94%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image.png)

</aside>

## 一、實習目的

- 了解瓦斯氣體感測器的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- 瓦斯氣體感測器
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%201%20%E7%93%A6%E6%96%AF%E6%B0%A3%E9%AB%94%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%201.png)
    
- 感測器原理
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%201%20%E7%93%A6%E6%96%AF%E6%B0%A3%E9%AB%94%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%202.png)
    
- 元件內部電路圖
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%201%20%E7%93%A6%E6%96%AF%E6%B0%A3%E9%AB%94%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%203.png)
    

## 三、實習步驟

- 載入 **/ArduinoProjects/Programming/GasSensor/GasSensor.ino** 檔案。
- 用打火機輸入瓦斯至感測器。

## 四、範例程式

```arduino
/*****************************************************
 * GasSensor.ino 
 * 目的:
 *  測試氣體感測器偵測功能(主要是甲烷)
 * 方法:
 *  氣體感測器 + 蜂鳴器
 * 步驟:
 *  可用打火機輸出瓦斯(甲烷)至感測器測試
 * 結果:
 * 1. 觀察氣體感測器上的LED是否亮起
 * 2. 當偵測到瓦斯氣體濃度過高時,蜂鳴器會發出警報聲
*****************************************************/

#define MQ4AnalogPin  A4    //定義氣體感測器接腳
#define BuzzerPin     36    //定義無源蜂鳴器接腳

const int R_0 = 945;        //自訂義RO測量值

/************************* 初始設定 *********************/
void setup() 
{
  Serial.begin(9600);
  
  pinMode(MQ4AnalogPin, INPUT); //設置氣體感測器接腳為輸入
  pinMode(BuzzerPin,    OUTPUT);//设置無源蜂鳴器接腳為輸出
}

/************************* 主程式 ***********************/
void loop() 
{
  float mq4ppm = getMethanePPM(); //計算甲烷濃度PPM值
  Serial.println(mq4ppm);         //序列埠輸出甲烷濃度PPM值
  
  //判斷氣體感測器濃度，若大於1000ppm，則蜂鳴器發出警報聲
  if (mq4ppm > 1000) 
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

```

## 五、實習結果

- 觀察氣體感測器上的LED是否亮起。
- 當偵測到瓦斯氣體濃度過高時，蜂鳴器會發出警報聲。