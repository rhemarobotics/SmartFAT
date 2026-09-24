# 4.11. RGB LED燈實習

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

# **貳、RGB LED燈**

<aside>
💡

RGB LED燈是現代電子產品中常見的指示和照明元件。它的核心是由紅、綠、藍三個不同顏色的LED晶片所組成，這三種顏色可以透過不同的亮度組合，創造出豐富多彩的色彩效果。工作原理基於加色混色法，透過控制每個LED晶片的電流強度，進而調整各色的亮度，最終呈現所需的顏色。
在工業應用中，RGB LED被廣泛應用於設備狀態指示和警示系統。例如，生產線上的機器可能使用綠色表示正常運行、黃色表示需要維護、紅色表示發生故障。這種直觀的顏色指示方式，能讓操作人員快速理解設備狀態，提高工作效率。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2011%20RGB%20LED%E7%87%88%E5%AF%A6%E7%BF%92/image.png)

</aside>

## 一、實習目的

- 了解RGB LED燈的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- RGB LED燈
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2011%20RGB%20LED%E7%87%88%E5%AF%A6%E7%BF%92/image%201.png)
    
- 感測器原理
    
    可以獨立控制LED的R、G、B顏色(0~255色調)，組合成不同的七彩色調。
    
- 元件內部電路圖
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2011%20RGB%20LED%E7%87%88%E5%AF%A6%E7%BF%92/image%202.png)
    

## 三、實習步驟

- 打開Arduino IDE，載入 /ArduinoProjects/Programming/RGBLed/RGBLed.ino 檔案。

## 四、範例程式

```arduino
/*****************************************************
 * RGBLed.ino 
 * 目的:
 *  測試RGB LED模組功能
 * 方法:
 *  RGB LED模組
 * 步驟:
 *  直接執行程式
 * 結果:
 *  觀察RGB LED模組的紅,藍,綠燈,是否依序亮起,熄滅(間隔1秒)
*****************************************************/

#define BLUE_PIN   10     //定義LED模組藍色腳位連接至10腳
#define RED_PIN    11     //定義LED模組紅色腳位連接至11腳
#define GREEN_PIN  12     //定義LED模組綠色腳位連接至12腳

/************************* 初始設定 *********************/
void setup() 
{
  pinMode(RED_PIN, OUTPUT);     //設定RED_PIN為輸出接腳
  pinMode(BLUE_PIN, OUTPUT);    //設定BLUE_PIN為輸出接腳
  pinMode(GREEN_PIN, OUTPUT);   //設定GREEN_PIN為輸出接腳
}

/************************* 主程式 ***********************/
void loop() 
{
  digitalWrite(RED_PIN, HIGH);   //LED模組紅色燈亮起
  delay(1000);                   //延遲1秒
  digitalWrite(RED_PIN, LOW);    //LED模組紅色燈熄滅
  delay(1000);                   //延遲1秒
  digitalWrite(BLUE_PIN, HIGH);  //LED模組藍色燈亮起
  delay(1000);                   //延遲1秒
  digitalWrite(BLUE_PIN, LOW);   //LED模組藍色燈熄滅
  delay(1000);                   //延遲1秒 
  digitalWrite(GREEN_PIN, HIGH); //LED模組綠色燈亮起
  delay(1000);                   //延遲1秒
  digitalWrite(GREEN_PIN, LOW);  //LED模組綠色燈熄滅
  delay(1000);   
}
```

## 四、實習結果

- 觀察RGB LED模組的紅,藍,綠燈,是否依序亮起,熄滅(間隔1秒)