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
