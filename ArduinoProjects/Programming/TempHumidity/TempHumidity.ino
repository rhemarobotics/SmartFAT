/*****************************************************
 * TempHumidity.ino 
 * 目的:
 *  測試溫濕度感測器功能
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
