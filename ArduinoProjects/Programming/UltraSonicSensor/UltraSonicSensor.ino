/*****************************************************
 * UltraSonicSensor.ino 
 * 目的:
 *  測試超音波感測器功能
 * 方法:
 *  超音波感測器
 * 步驟:
 *  放置一物件於感測器前,並任意前後移動
 * 結果:
 *  觀察序列埠監看視窗,顯示距離的變化
*****************************************************/

#define UR_TRIG_PIN   8 //定義超音波感測器發射腳位連接至8腳
#define UR_REV_PIN    9 //定義超音波感測器接收腳位連接至9腳


/************************* 初始設定 *********************/
void setup()
{
  Serial.begin(9600);
  
  pinMode(UR_TRIG_PIN, OUTPUT); //設定UR_TRIG_PIN為輸出接腳
  pinMode(UR_REV_PIN, INPUT);   //設定UR_REV_PIN 為輸入接腳
}

/************************* 主程式 ***********************/
void loop()
{
    int dis = CalculateDistUR(); //超音波距離計算函數
    Serial.println (dis);        //序列埠輸出偵測到的距離
    delay(1000);
}

/*********** 超音波距離計算函數(mm) ***********************/
int CalculateDistUR()
{
  long duration;
  
  digitalWrite(UR_TRIG_PIN, LOW);
  delayMicroseconds(5);
  digitalWrite(UR_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(UR_TRIG_PIN, LOW);
  
  duration = pulseIn(UR_REV_PIN, HIGH);
  
  return (duration/2) / 2.91;
}
