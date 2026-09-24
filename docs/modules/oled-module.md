# 4.12. OLED模組實習

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

# **貳、OLED模組**

<aside>
💡

OLED（Organic Light-Emitting Diode，有機發光二極體）模組在各種應用中具有廣泛的用途，主要因為其高對比度、節能、輕薄和自發光特性。以下是OLED模組的幾個主要用途 : 智能手機與平板電腦、智能手錶與健身追蹤器、儀表盤與控制面板等。OLED模組的靈活性和高效能使其在多種設備中廣泛應用，尤其是需要高畫質、節能和薄型化的應用場景。

![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2012%20OLED%E6%A8%A1%E7%B5%84%E5%AF%A6%E7%BF%92/e2222b14-40a4-4ff7-b3c1-9c2256ddd4f1.png)

</aside>

## 一、實習目的

- 了解OLED模組的原理和電路接線圖
- 透過Arduino程式，讀取並分析感測器數據

## 二、實習設備與材料

- OLED模組
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2012%20OLED%E6%A8%A1%E7%B5%84%E5%AF%A6%E7%BF%92/image.png)
    
- 感測器原理
    
    內部驅動晶片為SSD1306，是CMOS OLED / PLED驅動控制器。透過I2C串列傳輸介面，與單晶片處理器作雙向的資料轉換與傳輸。
    
- 元件內部電路圖
    
    ![image.png](../assets/4%20%E7%89%A9%E8%81%AF%E7%B6%B2%E7%B0%A1%E4%BB%8B/4%2012%20OLED%E6%A8%A1%E7%B5%84%E5%AF%A6%E7%BF%92/image%201.png)
    

## 三、實習步驟

- 打開Arduino IDE，載入 /ArduinoProjects/Programming/OledDisplay/OledDisplay.ino 檔案。
- 把顏色方塊放置於重量感測器上面。

## 四、範例程式

```arduino
/*****************************************************
 * OledDisplay.ino 
 * 目的:
 *  測試OLED顯示模組功能
 * 方法:
 *  OLED顯示模組 + 溫濕度感測器
 * 步驟:
 *  直接執行程式
 * 結果:
 *  觀察OLED顯示模組的溫溼度值(每1.5秒更新一次)
*****************************************************/

//掛載OLED顯示模組函式庫
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>             
#include <Adafruit_SSD1306.h>
#include <Fonts/FreeMonoBold18pt7b.h>

//掛載預先轉換好的溫溼度圖形
#include "logobmp.h"  

//掛載溫濕度感測器函式庫 
#include "DHT.h"      

#define dhtPin  26          //定義溫濕度感測器腳位連接至26腳
#define dhtType DHT11       //定義溫濕度感測器型別

#define OLED_RESET     4    //定義OLED顯示模組重置腳位連接至4腳
#define SCREEN_ADDRESS 0x3C //定義OLED顯示模組位址
#define SCREEN_WIDTH 128    //定義OLED顯示模組畫面寬度(pixels)
#define SCREEN_HEIGHT 64    //定義OLED顯示模組畫面高度(pixels)

//宣告OLED物件
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

//宣告溫濕度感測器物件
DHT dht(dhtPin, dhtType); 

/************************* 初始設定 *********************/
void setup() 
{
  Serial.begin(9600);
  
  dht.begin();//溫濕度感測器初始化

  //OLED顯示模組初始化
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) 
  {    
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  
  display.clearDisplay();//清除OLED顯示模組畫面 
  printText();           //OLED模組顯示文字
  delay(1500);           //延遲1.5秒
}

/************************* 主程式 ***********************/
float h,t;
void loop() 
{
  h = dht.readHumidity();   //讀取濕度值
  t = dht.readTemperature();//讀取溫度值(攝氏)
  
  //若溫度濕度值,其中一個為無效值,則輸出錯誤訊息
  if (isnan(h) || isnan(t)) 
  {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  //OLED模組動態更新溫度濕度值        
  showBitmap();          //OLED模組顯示溫濕度圖形
  printText();           //OLED模組顯示文字(溫濕度值)
  display.display();     //OLED模組顯示畫面
  delay(500);            //延遲0.5秒
  display.clearDisplay();//OLED模組清除畫面
}

/*********** OLED模組文字顯示函數 ****************************/
void printText() 
{
  display.setFont(&FreeMonoBold18pt7b);
  display.setTextColor(WHITE);
  display.setCursor(45, 28); 
  display.print(t);
  display.setCursor(100, 27);
  display.drawCircle(92, 8, 3, WHITE);
  display.setCursor(45, 62);
  display.print(h);
  display.print("%");
}

/*********** OLED模組圖形顯示函數 ****************************/
void showBitmap(void) 
{
  display.drawBitmap(0, 0, logo_bmp, bitmap_height, bitmap_width, WHITE);
}
```

## 四、實習結果

- 觀察OLED顯示模組的溫溼度值(每1.5秒更新一次)