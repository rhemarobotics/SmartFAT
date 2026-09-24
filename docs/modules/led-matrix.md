# 4.13. LED矩陣模組實習

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

# **貳、LED矩陣模組**

<aside>
💡

LED矩陣模組是一種排列有規則的LED燈組合，用於顯示各種圖形、文字或數字。其主要用途如下：顯示文字和數字、圖形和動畫顯示、電子看板與通知系統及工業控制面板等。總之，LED矩陣模組的用途廣泛，從簡單的字符顯示到動態的圖像表現，廣泛應用於日常生活中的信息傳遞和科技項目中。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2013%20LED%E7%9F%A9%E9%99%A3%E6%A8%A1%E7%B5%84%E5%AF%A6%E7%BF%92/image.png)

</aside>

## 一、實習目的

- 了解LED矩陣模組的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- LED矩陣模組
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2013%20LED%E7%9F%A9%E9%99%A3%E6%A8%A1%E7%B5%84%E5%AF%A6%E7%BF%92/image%201.png)
    
- 感測器原理
    
    MAX7219 是一個常用的 LED 驅動晶片，專為控制數位 LED 顯示器或 LED 矩陣設計。MAX7219 可以控制最多 8 行 8 列的 LED 矩陣或 8 位數的七段顯示器。它透過 SPI 接口與微控制器通信，負責掃描和點亮 LED，進行亮度調節以及提供數字顯示功能。
    
- 元件內部電路圖
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2013%20LED%E7%9F%A9%E9%99%A3%E6%A8%A1%E7%B5%84%E5%AF%A6%E7%BF%92/image%202.png)
    

## 三、實習步驟

- 打開Arduino IDE，載入 /ArduinoProjects/Programming/MatrixLed/MatrixLed.ino 檔案。

## 四、範例程式

```arduino
/*****************************************************
 * MatrixLed.ino 
 * 目的:
 *  測試8*8矩陣LED功能(模擬輸送帶物品往復運動)
 * 方法:
 *  8*8矩陣LED
 * 步驟:
 *  直接執行程式
 * 結果:
 *  觀察8*8矩陣LED上是否有物件往復運動變化
*****************************************************/

#include <LedControl.h> //掛載矩陣LED標頭檔

#define LED_DIN    42   //定義矩陣LED資料腳位連接至42腳
#define LED_CS     44   //定義矩陣LED致能腳位連接至44腳
#define LED_CLK    46   //定義矩陣LED時序腳位連接至46腳

//矩陣LED圖形
const uint64_t IMAGES[] = {
  0xff000001010000ff, 0xff000003030000ff, 0xff000006060000ff,
  0xff00000c0c0000ff, 0xff000018180000ff, 0xff000030300000ff,
  0xff000060600000ff, 0xff0000c0c00000ff, 0xff000080800000ff,
  0xff0000c0c00000ff, 0xff000060600000ff, 0xff000018180000ff,
  0xff00000c0c0000ff, 0xff000006060000ff, 0xff000003030000ff,
  0xff000001010000ff
};
const int IMAGES_LEN = sizeof(IMAGES)/8;

//宣告矩陣LED物件
LedControl display = LedControl(LED_DIN, LED_CLK, LED_CS);
int k = 0;

/************************* 初始設定 *********************/
void setup() 
{
  display.clearDisplay(0);      //矩陣LED畫面清除
  display.shutdown(0, false);
  display.setIntensity(0, 5);   //設定矩陣LED亮度
}

/************************* 主程式 ***********************/
void loop() 
{
  displayImage(IMAGES[k]);
  
  if (++k >= IMAGES_LEN ) 
  {
    k = 0;
  }
  
  delay(100);
}

/*********** 矩陣LED顯示函數 ****************************/
void displayImage(uint64_t image) 
{
  for (int i = 0; i < 8; i++) 
  {
    byte row = (image >> i * 8) & 0xFF;
    
    for (int j = 0; j < 8; j++) 
    {
      display.setLed(0, i, j, bitRead(row, j));
    }
  }
}
```

## 四、實習結果

- 觀察8*8矩陣LED上是否有物件往復運動顯示變化。