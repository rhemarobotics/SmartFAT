/*****************************************************
 * FlameSensor.ino 
 * 目的:
 *  測試火焰感測器偵測功能
 * 方法:
 *  火焰感測器 + 蜂鳴器
 * 步驟:
 *  可用打火機在感測器前點火測試(感測器上的可變電阻可以調整靈敏度)
 * 結果:
 * 1. 觀察火焰感測器上的LED是否亮起
 * 2. 當偵測到火焰時,蜂鳴器會發出警報聲
*****************************************************/

#define FlameDigitalPin   A7 //定義火焰感測器腳位連接至A7腳
#define FlameAnalogPin    A6 //定義火焰感測器腳位連接至A6腳
#define BuzzerPin         36 //定義蜂鳴器腳位連接至36腳

int FlameAnalogValue  = 0;   //讀取火焰感測器類比值
int FlameDigitalValue = 0;   //讀取火焰感測器數位值


/************************* 初始設定 *********************/
void setup()
{
  Serial.begin(9600);              //設置埠口通訊速率
  
  pinMode(FlameDigitalPin, INPUT); //設置火焰感測器數位接腳為輸入
  pinMode(FlameAnalogPin,  INPUT); //設置火焰感測器類比接腳為輸入
  pinMode(BuzzerPin,       OUTPUT);//設置蜂鳴器接腳為輸出
}

/************************* 主程式 ***********************/
void loop()
{
  FlameAnalogValue = analogRead(FlameAnalogPin);    //讀取火焰感測器類比值
  FlameDigitalValue = digitalRead(FlameDigitalPin); //讀取火焰感測器數位值
  
  Serial.print("FlameAnalog Data:  ");
  Serial.println(FlameAnalogValue);  //輸出火焰感測器類比值
  Serial.print("FlameDigital Data:  ");
  Serial.println(FlameDigitalValue); //輸出火焰感測器數位值
  
  //判斷火焰感測器是否檢測到火焰，若是，則蜂鳴器發出警報聲
  if (FlameDigitalValue == 0) 
  {
    //蜂鳴器音頻由低到高 200HZ ~ 800HZ  
    for(int i = 200; i <= 800; i++)  
    {  
        tone(BuzzerPin, i);
    }  
    
    delay(1000); //延遲1秒   

    //蜂鳴器音頻由高到低 800HZ ~ 200HZ
    for(int i= 800; i >= 200; i--)   
    {  
        tone(BuzzerPin, i);  
        delay(10);  
    }  
  }
  else
  {
    noTone(BuzzerPin); //關閉蜂鳴器
    delay(10);
  }
}
