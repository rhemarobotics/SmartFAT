/*****************************************************
 * IRDetectSensor.ino 
 * 目的:
 *  測試紅外線感測器功能
 * 方法:
 *  紅外線感測器(調整感測器上的可變電阻，可改變偵測距離)
 * 步驟:
 *  把物體放置於紅外線感測器前, 動態調整距離
 * 結果:
 * 1. 當感測器偵測到物體,觀察感測器上的LED是否亮起
 * 2. 觀察序列埠監看視窗,當偵測到物件時,顯示"Object Detected"
******************************************************/

#define IR_PIN 40  //定義紅外線感測器腳位連接至40腳
uint8_t IR_value;  //紅外線感測器數位狀態


/************************* 初始設定 *******************/
void setup()
{
  Serial.begin(9600);
  pinMode(IR_PIN, INPUT); //設定IR_PIN為輸入接腳
}

/************************* 主程式 *********************/
void loop()
{
  IR_value= digitalRead(IR_PIN); //讀取紅外線感測器數位狀態(0或1)
  Serial.println(IR_value);      //序列埠輸出數位狀態
    
  if (IR_value == 1)        
  {
    Serial.println("Nothing.");        //沒有偵測到物件
  }
  else
  {
    Serial.println("Object Detected.");//有偵測到物件
  }
  
  delay(1000);
}
