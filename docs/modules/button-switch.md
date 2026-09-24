# 4.8. 按鈕開關實習

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

# **貳、 按鈕開關**

<aside>
💡

按鈕開關的用途是控制電路的開啟或關閉。它是一種**機械式**的電控裝置，當用戶按下或鬆開按鈕時，按鈕內部的機構會實現電路的接通或斷開。常見用途包括電源控制、信號輸入、緊急停止、操作控制等。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%208%20%E6%8C%89%E9%88%95%E9%96%8B%E9%97%9C%E5%AF%A6%E7%BF%92/image.png)

</aside>

## 一、實習目的

- 了解按鈕開關的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- 按鈕開關
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%208%20%E6%8C%89%E9%88%95%E9%96%8B%E9%97%9C%E5%AF%A6%E7%BF%92/image%201.png)
    
- 感測器原理
    - 內部結構：按鈕開關內部通常包含一對接點——常開接點（NO，Normally Open）和常閉接點（NC，Normally Closed）。
    - 當按鈕處於未按下狀態時，常開接點是斷開的，常閉接點是接通的。
- 元件內部電路圖
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%208%20%E6%8C%89%E9%88%95%E9%96%8B%E9%97%9C%E5%AF%A6%E7%BF%92/image%202.png)
    

## 三、實習步驟

- 打開Arduino IDE，載入 /ArduinoProjects/Programming/Button/Button.ino 檔案。

## 四、範例程式

```arduino
/*****************************************************
 * Button.ino 
 * 目的:
 *  測試按鈕開關模組輸入功能
 * 方法:
 *  按鈕開關模組 + 8*8矩陣LED
 * 步驟:
 *  按住按鈕開關
 * 結果:
 * 1. 觀察控制板上的LED是否亮起
 * 2. 觀察8*8矩陣LED上是否隨機顯示剪刀/石頭/布的圖案
*****************************************************/

#include <LedControl.h> //掛載矩陣LED標頭檔

#define BTN_PIN 24      //定義按鈕開關輸入腳位連接至24腳
#define DIN_PIN 42      //定義矩陣LED_DIN腳位連接至42腳
#define CS_PIN  44      //定義矩陣LED_CS 腳位連接至44腳
#define CLK_PIN 46      //定義矩陣LED_CLK腳位連接至46腳

const uint64_t IMAGES[] = 
{
  0x1818183c66c38181,   //矩陣LED剪刀圖形
  0x3c42a59999a5423c,   //矩陣LED石頭圖形
  0x8142241818244281    //矩陣LED布圖形
};

//宣告矩陣LED物件
LedControl display = LedControl(DIN_PIN, CLK_PIN, CS_PIN);

/************************* 初始設定 *********************/
void setup()
{
  pinMode(LED_BUILTIN, OUTPUT); //設定LED_BUILTIN為輸出接腳
  pinMode(BTN_PIN,INPUT);       //設定BTN_PIN為輸入接腳
  display.clearDisplay(0);      //矩陣LED畫面清除
  display.shutdown(0, false);
  display.setIntensity(0, 5);   //設定矩陣LED亮度
}

/************************* 主程式 ***********************/
void loop()
{
  //讀取BTN_PIN輸入值
  int value = digitalRead(BTN_PIN); 
  
  if (value == HIGH) 
  {                                     //偵測到按鈕放開
      digitalWrite(LED_BUILTIN, LOW);   //板上LED燈熄滅
  }
  else 
  {                                     //偵測到按鈕壓下
      digitalWrite(LED_BUILTIN, HIGH);  //板上LED燈亮起
      
      //隨機顯示剪刀/石頭/布
      long radnum = random(300);
      if (radnum < 100)
        displayImage(IMAGES[0]);
      else if (100 < radnum && radnum < 200)
        displayImage(IMAGES[1]);
      else
        displayImage(IMAGES[2]);
      delay(100);
  }  
}

/*********** 矩陣LED顯示函數 ****************************/
void displayImage(uint64_t image) {
  for (int i = 0; i < 8; i++) {
    byte row = (image >> i * 8) & 0xFF;
    for (int j = 0; j < 8; j++) {
      display.setLed(0, i, j, bitRead(row, j));
    }
  }
}
```

## 四、實習結果

- 觀察控制板上的LED是否亮起。
- 觀察8*8矩陣LED上是否隨機顯示剪刀/石頭/布的圖案。