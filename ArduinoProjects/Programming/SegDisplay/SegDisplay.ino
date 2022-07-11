/*****************************************************
 * SegDisplay.ino 
 * 目的:
 *  測試數字顯示器功能
 * 方法:
 *  數字顯示器
 * 步驟:
 *  直接執行程式
 * 結果:
 *  觀察數字顯示器是否顯示"1234",間隔2秒後,然後畫面清空
*****************************************************/

#include <Wire.h>
#include <TM1650.h> //掛載數字顯示器標頭檔

TM1650 disp;        //宣告數字顯示器物件


/************************* 初始設定 *********************/
void setup() 
{
  Wire.begin();
  disp.init();      //初始化數字顯示器物件
}

/************************* 主程式 ***********************/
void loop() 
{
  
  char line[] = "1234"; 
  disp.displayString(line);                      //設定數字1234
  disp.setBrightnessGradually(TM1650_MAX_BRIGHT);//設定最大亮度顯示
  disp.displayOn();                              //顯示數字1234  
  delay(2000);                                   //延遲2秒
  
  disp.setBrightnessGradually(TM1650_MIN_BRIGHT);//設定最小亮度顯示
  disp.displayOff();                             //清除畫面 
  delay(2000);                                   //延遲2秒 
}
