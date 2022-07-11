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
