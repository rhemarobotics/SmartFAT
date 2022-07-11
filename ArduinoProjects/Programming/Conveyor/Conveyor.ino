/*****************************************************
 * Conveyor.ino 
 * 目的:
 *  測試輸送帶運轉功能
 * 方法:
 *  輸送帶
 * 步驟:
 *  直接執行程式
 * 結果:
 * 1. 觀察輸送帶是否正向運轉10S
 * 2. 隨後輸送帶停止運轉2S
 * 3. 最後輸送帶反向運轉10S
*****************************************************/

#define A_1A      2     //定義輸送帶方向控制腳位連接至2腳
#define A_1B      3     //定義輸送帶速度控制腳位連接至3腳

#define fwdSpeed  10    //設定輸送帶前進速度(0~255)
#define bkSpeed   250   //設定輸送帶後退速度(0~255)


/************************* 初始設定 *********************/
void setup() 
{
  pinMode(A_1A, OUTPUT);  //設定A_1A為輸出接腳
  pinMode(A_1B, OUTPUT);  //設定A_1B為輸出接腳
  digitalWrite(A_1A, LOW);//輸送帶反向
  digitalWrite(A_1B, LOW);//輸送帶停止
}

/************************* 主程式 ***********************/
void loop() 
{
  forward();
  delay(10000);
  
  stopConveyor();
  delay(2000);
  
  backward();
  delay(10000);
}

/*********** 輸送帶停止函數 ****************************/
void stopConveyor()
{
  digitalWrite(A_1A, LOW);
  digitalWrite(A_1B, LOW);
}

/*********** 輸送帶正向運轉函數 ****************************/
void forward()
{
  digitalWrite(A_1A, HIGH);   //輸送帶正向運轉
  analogWrite(A_1B, fwdSpeed);//輸送帶運轉速度(類比輸出)
}

/*********** 輸送帶反向運轉函數 ****************************/
void backward()
{
  digitalWrite(A_1A, LOW);   //輸送帶反向運轉
  analogWrite(A_1B, bkSpeed);//輸送帶運轉速度(類比輸出)
}
