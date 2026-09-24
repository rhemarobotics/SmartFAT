# 4.3. 溫/溼度感測器實習

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

# **貳、溫/溼度感測器**

<aside>
💡

溫度和濕度傳感器是最常用的環境傳感器之一。濕度傳感器有時也稱為濕度計。這些設備用於在任何給定點或任何給定地點提供空氣中的實際濕度條件。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%203%20%E6%BA%AB%20%E6%BA%BC%E5%BA%A6%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image.png)

</aside>

## 一、實習目的

- 了解溫/溼度感測器的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- 溫/溼度感測器
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%203%20%E6%BA%AB%20%E6%BA%BC%E5%BA%A6%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%201.png)
    
- 感測器原理
    - 熱敏電阻 (NTC/PTC)： 熱敏電阻的電阻值會隨溫度改變而改變，NTC（負溫度係數）表示溫度上升時電阻下降，而PTC（正溫度係數）表示溫度上升時電阻上升。透過測量電阻的變化來測定溫度。
    - 電阻型濕度感測器： 這種類型的感測器利用吸濕性材料的電阻隨濕度變化的特性。當空氣中的水分增加時，感測器的電阻會下降。通過測量電阻的變化來計算濕度。
- 元件內部電路圖
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%203%20%E6%BA%AB%20%E6%BA%BC%E5%BA%A6%E6%84%9F%E6%B8%AC%E5%99%A8%E5%AF%A6%E7%BF%92/image%202.png)
    

## 三、實習步驟

- 打開Arduino IDE，載入 /ArduinoProjects/Programming/TempHumidity/TempHumidity.ino 檔案。

## 四、範例程式

```arduino
/*****************************************************
 * TempHumidity.ino 
 * 目的:
 *  測試溫/濕度感測器功能
 * 方法:
 *  溫濕度感測器
 * 步驟:
 *  直接執行程式
 * 結果:
 *  觀察序列埠是否有輸出溫濕度值(1秒更新一次)
*****************************************************/

#include "DHT.h"          //掛載溫濕度感測器函式庫 

#define dhtPin  26        //定義溫濕度感測器腳位連接至26腳
#define dhtType DHT11     //定義溫濕度感測器型別   

DHT dht(dhtPin, dhtType); //宣告溫濕度感測器物件

/************************* 初始設定 *********************/
void setup() 
{
  Serial.begin(9600);
  dht.begin();//溫濕度感測器初始化
}

/************************* 主程式 ***********************/
void loop() {
  float h = dht.readHumidity();       //讀取濕度
  float t = dht.readTemperature();    //讀取攝氏溫度
  float f = dht.readTemperature(true);//讀取華氏溫度
  
  if (isnan(h) || isnan(t) || isnan(f)) 
  {
    Serial.println("無法從DHT傳感器讀取！");
    return;
  }
  
  Serial.print("濕度: ");
  Serial.print(h);
  Serial.print("%\t");    //序列埠輸出濕度值
  Serial.print("攝氏溫度: ");
  Serial.print(t);
  Serial.print("*C\t");   //序列埠輸出攝氏溫度值
  Serial.print("華氏溫度: ");
  Serial.print(f);
  Serial.print("*F\n");   //序列埠輸出華氏溫度值
  delay(1000);            //延遲1秒
}
```

## 四、實習結果

- 觀察序列埠是否有輸出溫濕度值(1秒更新一次)。