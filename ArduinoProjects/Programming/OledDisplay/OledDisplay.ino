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
