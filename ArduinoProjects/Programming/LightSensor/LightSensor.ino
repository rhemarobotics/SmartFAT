/*****************************************************
 * LightSensor.ino 
 * 目的:
 *  測試光敏感測器功能
 * 方法:
 *  光敏感測器
 * 步驟:
 *  遮蔽或無遮蔽光敏感測器,觀察輸出值變化
 * 結果:
 *  當光線變暗,數值則變小, 反之光線變亮,數值則變大
*****************************************************/

#define LIGHT_PIN A2  //定義光敏感測器腳位連接至A2腳


/************************* 初始設定 *******************/
void setup() 
{
  Serial.begin(9600);
}

/************************* 主程式 *********************/
void loop() 
{
  int lightValue = analogRead(LIGHT_PIN); //讀取光敏感測器值,0~1023
  Serial.println(lightValue);             //序列埠視窗輸出
  delay(100);
}
