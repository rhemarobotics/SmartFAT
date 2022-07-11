/*****************************************************
 * TriColorLight.ino 
 * 目的:
 *  測試三色指示燈功能
 * 方法:
 *  三色指示燈
 * 步驟:
 *  直接執行程式
 * 結果:
 *  觀察指示燈的紅,綠,藍燈,是否依序亮起,熄滅(間隔1秒)
*****************************************************/

#define CLR_R_PIN A10 //定義紅色指示燈腳位連接至A10腳
#define CLR_Y_PIN A9  //定義黃色指示燈腳位連接至A9腳
#define CLR_G_PIN A8  //定義綠色指示燈腳位連接至A8腳


/************************* 初始設定 *********************/
void setup() 
{
  pinMode(CLR_R_PIN, OUTPUT); //設定CLR_R為輸出接腳
  pinMode(CLR_Y_PIN, OUTPUT); //設定CLR_Y為輸出接腳
  pinMode(CLR_G_PIN, OUTPUT); //設定CLR_G為輸出接腳
}

/************************* 主程式 ***********************/
void loop()
{
  digitalWrite(CLR_R_PIN, HIGH);// 開啟紅燈
  delay(1000);                  // 延遲1秒
  digitalWrite(CLR_R_PIN, LOW); // 關閉紅燈
  delay(1000);                  // 延遲1秒
  digitalWrite(CLR_Y_PIN, HIGH);// 開啟黃燈
  delay(1000);                  // 延遲1秒
  digitalWrite(CLR_Y_PIN, LOW); // 關閉黃燈
  delay(1000);                  // 延遲1秒
  digitalWrite(CLR_G_PIN, HIGH);// 開啟綠燈
  delay(1000);                  // 延遲1秒
  digitalWrite(CLR_G_PIN, LOW); // 關閉綠燈
  delay(1000);   
}
