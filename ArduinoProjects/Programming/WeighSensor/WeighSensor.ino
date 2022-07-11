/*****************************************************
 * WeighSensor.ino 
 * 目的:
 *  測試重量感測器功能
 * 方法:
 *  重量感測器 + 數字顯示器
 * 步驟:
 *  1. 打開序列埠監看視窗,等待"重量感測器校正完成!!!"
 *  2. 此時,放置物件於感測器上 
 *  3. 觀察數字顯示器上顯示的重量值或透過序列埠監看視窗
 * 結果:
 *   顯示器上顯示的重量值並序列埠監看視窗顯示重量值
*****************************************************/

#include "HX711.h"          //掛載重量感測器標頭檔
#include <Wire.h>
#include <TM1650.h>         //掛載數字顯示器標頭檔


#define WH_DT_Pin     4     //定義重量感測器WH_DT_Pin腳位連接至4腳
#define WH_SCK_Pin    5     //定義重量感測器WH_SCK_Pin腳位連接至5腳
#define WH_factor     4200  //定義重量感測器比例參數

HX711 whScale;              //宣告重量感測器物件
TM1650 disp;                //宣告數字顯示器物件


/************************* 初始設定 *******************/
void setup() 
{
  Serial.begin(9600);

  Wire.begin();
  disp.init();                            //初始化數字顯示器物件
  
  whScale.begin(WH_DT_Pin, WH_SCK_Pin);   //初始化重量感測器物件
  whScale.set_scale(WH_factor);           //設定重量感測器比例參數
  whScale.tare();                         //設定重量感測器歸零
  delay(2000);                            //延遲2秒 
  
  //等待自我校正完成，待出現ready後，才可以放置物品
  Serial.println("重量感測器校正完成!!!");
}


/************************* 主程式 ***********************/
void loop() 
{
  //讀取重量值，10的意思是取10次的平均重量
  float weight = whScale.get_units(10);
  Serial.println(weight, 1);
  delay(1000);
  
  //透過數字顯示器顯示重量值
  char line[6];               //設置一字串緩存區
  dtostrf(weight, 3, 1, line);//把浮點數轉成字串
  disp.displayString(line);   //顯示字串
}
